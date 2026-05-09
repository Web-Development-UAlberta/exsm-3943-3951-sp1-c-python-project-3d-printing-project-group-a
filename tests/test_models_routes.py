import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import create_app


class TestModelsRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

    def test_get_all_models(self):
        res = self.client.get("/api/models/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_get_model_not_found(self):
        res = self.client.get("/api/models/99999")
        self.assertEqual(res.status_code, 404)

    def test_quote_missing_fields(self):
        res = self.client.post("/api/models/quote", json={
            "model_id": 1
        })
        self.assertEqual(res.status_code, 400)

    def test_quote_invalid_scale(self):
        res = self.client.post("/api/models/quote", json={
            "model_id":1,
            "filament_id": 1,
            "scale": 999,
            "infill_percent": 50,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 400)

    def test_quote_invalid_infill(self):
        res = self.client.post("/api/models/quote", json={
            "model_id": 1,
            "filament_id": 1,
            "scale": 100,
            "infill_percent": 150,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()