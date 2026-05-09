import os
import sys
import unittest
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import create_app


class TestUsers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

        s = str(int(time.time()))
        cls.username = f"profile_{s}"
        cls.password = "Test1234!"

        # register fresh user
        reg = cls.client.post("/api/auth/register", json={
            "username":       cls.username,
            "password":       cls.password,
            "phone_number":   f"444-{s[-7:]}",
            "city":           "Edmonton",
            "street_address": "123 Main St",
            "province":       "AB"
        })

        if reg.status_code != 201:
            raise Exception(f"Setup register failed: {reg.get_json()}")

        res = cls.client.post("/api/auth/login", json={
            "username": cls.username,
            "password": cls.password
        })

        if res.status_code != 200:
            raise Exception(f"Setup login failed: {res.get_json()}")

        cls.token   = res.get_json()["access_token"]
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    def test_get_profile(self):
        res = self.client.get("/api/users/me", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["username"], self.username)

    def test_get_profile_no_token(self):
        res = self.client.get("/api/users/me")
        self.assertEqual(res.status_code, 401)

    def test_update_profile(self):
        res = self.client.put("/api/users/me", headers=self.headers, json={
            "full_name": "Profile User",
            "city":      "Calgary"
        })
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/api/users/me", headers=self.headers)
        data = res.get_json()
        self.assertEqual(data["full_name"], "Profile User")
        self.assertEqual(data["city"],      "Calgary")

    def test_change_password_wrong_current(self):
        res = self.client.put("/api/users/me/password", headers=self.headers, json={
            "current_password": "WrongPass!",
            "new_password":     "NewPass5678!"
        })
        self.assertEqual(res.status_code, 401)

    def test_change_password_too_short(self):
        res = self.client.put("/api/users/me/password", headers=self.headers, json={
            "current_password": self.password,
            "new_password":     "short"
        })
        self.assertEqual(res.status_code, 400)

    def test_change_password_success(self):
        # run last — changes the password
        res = self.client.put("/api/users/me/password", headers=self.headers, json={
            "current_password": self.password,
            "new_password":     "NewPass5678!"
        })
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()