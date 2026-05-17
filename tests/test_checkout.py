import os
import sys
import unittest
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import create_app


class TestCheckout(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

        # unique user
        s = str(int(time.time()))
        cls.username = f"checkout_{s}"
        cls.password = "Test1234!"

        reg_res = cls.client.post("/api/auth/register", json={
            "username": cls.username,
            "password": cls.password,
            "phone_number": f"780-{s[-7:]}",
            "city": "Edmonton",
            "street_address": "123 Main St",
            "province": "AB"
        })

        if reg_res.status_code not in [200, 201]:
            raise Exception(
                f"Register failed: {reg_res.status_code}, {reg_res.get_json()}"
            )

        res = cls.client.post("/api/auth/login", json={
            "username": cls.username,
            "password": cls.password
        })

        if res.status_code != 200:
            raise Exception(f"Login failed: {res.status_code}, {res.get_json()}")

        data = res.get_json()

        if "access_token" not in data:
            raise Exception(f"No token returned from login: {data}")

        cls.token = data["access_token"]
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

        models_res = cls.client.get("/api/models/")

        if models_res.status_code != 200:
            raise Exception(f"Models fetch failed: {models_res.status_code}, {models_res.get_json()}")

        models_data = models_res.get_json()

        if not models_data:
            raise Exception("No models found — run seed.py first")

        cls.model_id = models_data[0]["model_id"]

        if not models_data[0].get("filaments"):
            raise Exception("Model has no filaments")

        cls.filament_id = models_data[0]["filaments"][0]["filament_id"]

    def _add_item_to_cart(self):
        return self.client.post("/api/cart/", headers=self.headers, json={
            "model_id": self.model_id,
            "filament_id": self.filament_id,
            "scale": 100,
            "infill_percent": 50,
            "color_count": 2,
            "quantity": 1
        })

    def _clear_cart(self):
        self.client.delete("/api/cart/", headers=self.headers)

    def test_01_create_intent_empty_cart(self):
        self._clear_cart()
        res = self.client.post("/api/checkout/create-intent", headers=self.headers)
        self.assertEqual(res.status_code, 400)
        self.assertIn("error", res.get_json())

    def test_02_create_intent_no_token(self):
        res = self.client.post("/api/checkout/create-intent")
        self.assertEqual(res.status_code, 401)

    def test_03_create_intent_success(self):
        self._clear_cart()
        self._add_item_to_cart()
        res = self.client.post("/api/checkout/create-intent", headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_04_confirm_missing_payment_intent(self):
        res = self.client.post("/api/checkout/confirm", headers=self.headers, json={})
        self.assertEqual(res.status_code, 400)
        self.assertIn("error", res.get_json())

    def test_05_confirm_no_token(self):
        res = self.client.post("/api/checkout/confirm", json={
            "payment_intent_id": "pi_test_dummy_1"
        })
        self.assertEqual(res.status_code, 401)

    def test_06_confirm_empty_cart(self):
        self._clear_cart()
        res = self.client.post("/api/checkout/confirm", headers=self.headers, json={
            "payment_intent_id": "pi_test_dummy_1"
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("error", res.get_json())

    def test_07_confirm_success(self):
        self._clear_cart()
        self._add_item_to_cart()

        intent_res = self.client.post("/api/checkout/create-intent", headers=self.headers)
        self.assertEqual(intent_res.status_code, 200)

        intent_data = intent_res.get_json()
        payment_intent_id = intent_data.get("payment_intent_id", "pi_test_dummy_77")

        confirm_res = self.client.post("/api/checkout/confirm", headers=self.headers, json={
            "payment_intent_id": payment_intent_id
        })

        self.assertEqual(confirm_res.status_code, 201)

        confirm_data = confirm_res.get_json()
        self.assertIn("order_id", confirm_data)

        self.__class__.order_id = confirm_data["order_id"]

    def test_08_cart_empty_after_checkout(self):
        res = self.client.get("/api/cart/", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["items"], [])

    def test_09_order_exists_after_checkout(self):
        order_id = getattr(self.__class__, "order_id", None)

        if not order_id:
            self.skipTest("No order_id available")

        res = self.client.get(f"/api/orders/{order_id}", headers=self.headers)
        self.assertEqual(res.status_code, 200)

        data = res.get_json()
        self.assertEqual(data["order_status"], "Pending")
        self.assertEqual(data["payment_status"], "Succeeded")
        self.assertIsNotNone(data["stripe_payment_id"])

    def test_10_cannot_checkout_twice(self):
        self._clear_cart()
        res = self.client.post("/api/checkout/confirm", headers=self.headers, json={
            "payment_intent_id": "pi_test_dummy_99"
        })
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()