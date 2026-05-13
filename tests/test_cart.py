# import os
# import sys
# import unittest
# import time

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from src.app import create_app


# class TestCart(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.app = create_app()
#         cls.app.config["TESTING"] = True
#         cls.client = cls.app.test_client()

#         s = str(int(time.time()))
#         cls.username = f"cart_{s}"
#         cls.password = "Test1234!"

#         # Register
#         cls.client.post("/api/auth/register", json={
#             "username": cls.username,
#             "password": cls.password,
#             "phone_number": f"780-{s[-7:]}",
#             "city": "Edmonton",
#             "street_address": "123 Main St",
#             "province": "AB"
#         })

#         # Login
#         res = cls.client.post("/api/auth/login", json={
#             "username": cls.username,
#             "password": cls.password
#         })

#         assert res.status_code == 200, f"Login failed: {res.get_json()}"
#         cls.token = res.get_json()["access_token"]
#         cls.headers = {"Authorization": f"Bearer {cls.token}"}

#         # Get models
#         models_res = cls.client.get("/api/models/")
#         assert models_res.status_code == 200

#         models_data = models_res.get_json()

#         cls.model_id = None
#         cls.filament_id = None

#         for m in models_data:
#             if "filaments" in m and m["filaments"]:
#                 cls.model_id = m["model_id"]
#                 cls.filament_id = m["filaments"][0]["filament_id"]
#                 break

#         assert cls.model_id is not None, "No model with filaments found"


#     def test_01_get_empty_cart(self):
#         res = self.client.get("/api/cart/", headers=self.headers)
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.get_json()["items"], [])

#     def test_02_get_cart_no_token(self):
#         res = self.client.get("/api/cart/")
#         self.assertEqual(res.status_code, 401)

#     def test_03_add_missing_fields(self):
#         res = self.client.post("/api/cart/", headers=self.headers, json={
#             "model_id": self.model_id
#         })
#         self.assertEqual(res.status_code, 400)

#     def test_04_invalid_scale(self):
#         res = self.client.post("/api/cart/", headers=self.headers, json={
#             "model_id": self.model_id,
#             "filament_id": self.filament_id,
#             "scale": 999,
#             "infill_percent": 50,
#             "color_count": 1,
#             "quantity": 1
#         })
#         self.assertEqual(res.status_code, 400)

#     def test_05_invalid_infill(self):
#         res = self.client.post("/api/cart/", headers=self.headers, json={
#             "model_id": self.model_id,
#             "filament_id": self.filament_id,
#             "scale": 100,
#             "infill_percent": 150,
#             "color_count": 1,
#             "quantity": 1
#         })
#         self.assertEqual(res.status_code, 400)

#     def test_06_model_not_found(self):
#         res = self.client.post("/api/cart/", headers=self.headers, json={
#             "model_id": 999999,
#             "filament_id": self.filament_id,
#             "scale": 100,
#             "infill_percent": 50,
#             "color_count": 1,
#             "quantity": 1
#         })
#         self.assertEqual(res.status_code, 400)

#     def test_07_add_success(self):
#         res = self.client.post("/api/cart/", headers=self.headers, json={
#             "model_id": self.model_id,
#             "filament_id": self.filament_id,
#             "scale": 100,
#             "infill_percent": 50,
#             "color_count": 2,
#             "quantity": 1
#         })

#         self.assertEqual(res.status_code, 201)
#         self.assertEqual(len(res.get_json()["items"]), 1)
#         self.__class__.detail_id = res.get_json()["items"][0]["order_detail_id"]

#     def test_08_cart_not_empty(self):
#         res = self.client.get("/api/cart/", headers=self.headers)
#         self.assertGreater(len(res.get_json()["items"]), 0)

#     def test_09_duplicate_increases_qty(self):
#         res = self.client.post("/api/cart/", headers=self.headers, json={
#             "model_id": self.model_id,
#             "filament_id": self.filament_id,
#             "scale": 100,
#             "infill_percent": 50,
#             "color_count": 2,
#             "quantity": 1
#         })

#         self.assertEqual(res.status_code, 201)

#     def test_10_remove_item(self):
#         if not hasattr(self.__class__, "detail_id"):
#             self.skipTest("No item to remove")

#         res = self.client.delete(
#             f"/api/cart/{self.detail_id}",
#             headers=self.headers
#         )
#         self.assertEqual(res.status_code, 200)

#     def test_11_remove_invalid(self):
#         res = self.client.delete("/api/cart/99999", headers=self.headers)
#         self.assertEqual(res.status_code, 404)

#     def test_12_clear_cart(self):
#         self.client.post("/api/cart/", headers=self.headers, json={
#             "model_id": self.model_id,
#             "filament_id": self.filament_id,
#             "scale": 100,
#             "infill_percent": 50,
#             "color_count": 1,
#             "quantity": 1
#         })

#         res = self.client.delete("/api/cart/", headers=self.headers)
#         self.assertEqual(res.status_code, 200)

#     def test_13_cart_empty(self):
#         res = self.client.get("/api/cart/", headers=self.headers)
#         self.assertEqual(res.get_json()["items"], [])


# if __name__ == "__main__":
#     unittest.main()