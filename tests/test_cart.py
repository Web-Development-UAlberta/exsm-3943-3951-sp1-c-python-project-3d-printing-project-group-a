import os
import sys
import unittest
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import create_app


class TestCart(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

        # Create a unique test user
        s = str(int(time.time()))
        cls.username = f"cart_{s}"
        cls.password = "Test1234!"

        # Register user
        register_res = cls.client.post("/api/auth/register", json={
            "username": cls.username,
            "password": cls.password,
            "phone_number": f"780-{s[-7:]}",
            "city": "Edmonton",
            "street_address": "123 Main St",
            "province": "AB"
        })

        if register_res.status_code not in (200, 201):
            raise Exception(f"Registration failed: {register_res.get_json()}")

        # Login
        login_res = cls.client.post("/api/auth/login", json={
            "username": cls.username,
            "password": cls.password
        })

        if login_res.status_code != 200:
            raise Exception(f"Login failed: {login_res.get_json()}")

        cls.token = login_res.get_json()["access_token"]
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

        cls.model_id = 5
        cls.filament_id = 7

        print(
            f"Using seeded IDs: model_id={cls.model_id}, "
            f"filament_id={cls.filament_id}"
        )

    def test_01_get_empty_cart(self):
        res = self.client.get("/api/cart/", headers=self.headers)
        self.assertEqual(res.status_code, 200)

        data = res.get_json()
        self.assertEqual(data["items"], [])

    def test_02_get_cart_no_token(self):
        res = self.client.get("/api/cart/")
        self.assertEqual(res.status_code, 401)

    def test_03_add_to_cart_missing_fields(self):
        res = self.client.post("/api/cart/", headers=self.headers, json={
            "model_id": self.model_id
        })
        self.assertEqual(res.status_code, 400)

    def test_04_add_to_cart_invalid_scale(self):
        res = self.client.post("/api/cart/", headers=self.headers, json={
            "model_id": self.model_id,
            "filament_id": self.filament_id,
            "scale": 999,
            "infill_percent": 50,
            "color_count": 1,
            "quantity": 1
        })
        self.assertEqual(res.status_code, 400)

    def test_05_add_to_cart_invalid_infill(self):
        res = self.client.post("/api/cart/", headers=self.headers, json={
            "model_id": self.model_id,
            "filament_id": self.filament_id,
            "scale": 100,
            "infill_percent": 150,
            "color_count": 1,
            "quantity": 1
        })
        self.assertEqual(res.status_code, 400)

    def test_06_add_to_cart_model_not_found(self):
        res = self.client.post("/api/cart/", headers=self.headers, json={
            "model_id": 99999,
            "filament_id": self.filament_id,
            "scale": 100,
            "infill_percent": 50,
            "color_count": 1,
            "quantity": 1
        })
        self.assertEqual(res.status_code, 400)

    def test_07_add_to_cart_success(self):
        res = self.client.post("/api/cart/", headers=self.headers, json={
            "model_id": self.model_id,
            "filament_id": self.filament_id,
            "scale": 100,
            "infill_percent": 50,
            "color_count": 1,
            "quantity": 1
        })

        # Show the real error if the request fails
        self.assertEqual(
            res.status_code,
            201,
            f"Expected 201 but got {res.status_code}: {res.get_json()}"
        )

        data = res.get_json()
        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 1)

        # Save detail_id for later tests
        self.__class__.detail_id = data["items"][0]["order_detail_id"]

    def test_08_get_cart_with_item(self):
        res = self.client.get("/api/cart/", headers=self.headers)
        self.assertEqual(res.status_code, 200)

        data = res.get_json()
        self.assertGreater(
            len(data["items"]),
            0,
            f"Cart is empty: {data}"
        )
        self.assertGreater(data["total_price"], 0)

    def test_09_add_same_item_increases_quantity(self):
        res = self.client.post("/api/cart/", headers=self.headers, json={
            "model_id": self.model_id,
            "filament_id": self.filament_id,
            "scale": 100,
            "infill_percent": 50,
            "color_count": 1,
            "quantity": 1
        })

        self.assertEqual(
            res.status_code,
            201,
            f"Expected 201 but got {res.status_code}: {res.get_json()}"
        )

        data = res.get_json()
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["order_quantity"], 2)

    def test_10_remove_item_from_cart(self):
        detail_id = getattr(self.__class__, "detail_id", None)

        if not detail_id:
            self.skipTest("No detail_id from previous test")

        res = self.client.delete(
            f"/api/cart/{detail_id}",
            headers=self.headers
        )

        self.assertEqual(res.status_code, 200)

    def test_11_remove_nonexistent_item(self):
        res = self.client.delete("/api/cart/99999", headers=self.headers)
        self.assertEqual(res.status_code, 404)

    def test_12_clear_cart(self):
        # Add an item first so the cart exists
        add_res = self.client.post("/api/cart/", headers=self.headers, json={
            "model_id": self.model_id,
            "filament_id": self.filament_id,
            "scale": 100,
            "infill_percent": 50,
            "color_count": 1,
            "quantity": 1
        })

        self.assertEqual(
            add_res.status_code,
            201,
            f"Could not add item before clearing cart: {add_res.get_json()}"
        )

        # Clear the cart
        res = self.client.delete("/api/cart/", headers=self.headers)

        # Some implementations return 200, others 204
        self.assertIn(
            res.status_code,
            [200, 204],
            f"Unexpected status code: {res.status_code}"
        )

        if res.status_code == 200:
            data = res.get_json()
            if data and "message" in data:
                self.assertEqual(data["message"], "Cart cleared")

    def test_13_cart_empty_after_clear(self):
        res = self.client.get("/api/cart/", headers=self.headers)
        self.assertEqual(res.status_code, 200)

        data = res.get_json()
        self.assertEqual(data["items"], [])


if __name__ == "__main__":
    unittest.main()