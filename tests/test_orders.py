import os
import sys
import unittest
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import create_app


class TestOrders(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

        s = str(int(time.time()))
        cls.username = f"order_{s}"
        cls.password = "Test1234!"

        cls.client.post("/api/auth/register", json={
            "username": cls.username,
            "password": cls.password,
            "phone_number": f"780-{s[-7:]}",
            "city": "Edmonton",
            "street_address": "123 Main St",
            "province": "AB"
        })

        res = cls.client.post("/api/auth/login", json={
            "username": cls.username,
            "password": cls.password
        })

        if res.status_code != 200:
            raise Exception(f"Login failed: {res.get_json()}")

        cls.token = res.get_json()["access_token"]
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    def test_01_get_orders_empty(self):
        res = self.client.get("/api/orders/", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), [])

    def test_02_get_orders_no_token(self):
        res = self.client.get("/api/orders/")
        self.assertEqual(res.status_code, 401)

    def test_03_get_order_not_found(self):
        res = self.client.get("/api/orders/99999", headers=self.headers)
        self.assertEqual(res.status_code, 404)

    def test_04_cancel_order_not_found(self):
        res = self.client.put("/api/orders/99999/cancel", headers=self.headers)
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()