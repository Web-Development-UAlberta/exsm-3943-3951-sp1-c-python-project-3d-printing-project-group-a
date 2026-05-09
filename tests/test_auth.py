import os
import sys
import unittest
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import create_app


class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()
        cls.s = str(int(time.time()))

    def test_register_success(self):
        res = self.client.post("/api/auth/register", json={
            "username":       f"reg_{self.s}",
            "password":       "Test1234!",
            "phone_number":   f"111-{self.s[-7:]}",
            "city":           "Edmonton",
            "street_address": "123 Main St",
            "province":       "AB"
        })
        self.assertEqual(res.status_code, 201)

    def test_register_missing_fields(self):
        res = self.client.post("/api/auth/register", json={
            "username": "incomplete_user"
        })
        self.assertEqual(res.status_code, 400)

    def test_register_duplicate_username(self):
        data = {
            "username":       f"dup_{self.s}",
            "password":       "Test1234!",
            "phone_number":   f"222-{self.s[-7:]}",
            "city":           "Edmonton",
            "street_address": "123 Main St",
            "province":       "AB"
        }
        self.client.post("/api/auth/register", json=data)
        res = self.client.post("/api/auth/register", json=data)
        self.assertEqual(res.status_code, 409)

    def test_login_success(self):
        username = f"log_{self.s}"
        self.client.post("/api/auth/register", json={
            "username":       username,
            "password":       "Test1234!",
            "phone_number":   f"333-{self.s[-7:]}",
            "city":           "Edmonton",
            "street_address": "123 Main St",
            "province":       "AB"
        })
        res = self.client.post("/api/auth/login", json={
            "username": username,
            "password": "Test1234!"
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn("access_token", res.get_json())

    def test_login_wrong_password(self):
        res = self.client.post("/api/auth/login", json={
            "username": f"log_{self.s}",
            "password": "WrongPass!"
        })
        self.assertEqual(res.status_code, 401)

    def test_login_missing_fields(self):
        res = self.client.post("/api/auth/login", json={})
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()