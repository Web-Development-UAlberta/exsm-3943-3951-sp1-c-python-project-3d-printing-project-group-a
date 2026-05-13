import os
import sys
import unittest
import json

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

    def test_get_model_filter_tag_found(self):
        res = self.client.get("/api/models/?tag_id=1")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertGreater(len(res.get_json()), 0)
        json_list = res.get_json()[:1]
        json_first_record = json_list[0]['tags'][0]['tag_name']
        self.assertEqual(json_first_record.lower(), 'Gaming'.lower())
    
    def test_get_model_filter_tag_notfound(self):
        res = self.client.get("/api/models/?tag_id=999999")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertEqual(len(res.get_json()), 0)

    def test_get_model_filter_filament_found(self):
        res = self.client.get("/api/models/?filament_id=1")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertGreater(len(res.get_json()), 0)

    def test_get_model_filter_filament_notfound(self):
        res = self.client.get("/api/models/?filament_id=999999")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertEqual(len(res.get_json()), 0)

    def test_get_model_filter_order_asc(self):
        res = self.client.get("/api/models/?order=asc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()[:2]
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertGreater(json_second_record, json_first_record)

    def test_get_model_filter_order_desc(self):
        res = self.client.get("/api/models/?order=desc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()[:2]
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertGreater(json_first_record, json_second_record)

    def test_get_model_search(self):
        res = self.client.get("/api/models/?search=airplane")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()[:1]
        json_first_record = json_list[0]['model_name']
        self.assertEqual(json_first_record.lower(), 'Airplane'.lower())

    def test_get_model_search_order_asc(self):
        res = self.client.get("/api/models/?search=man&order=asc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()[:2]
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertIn('man', json_first_record.lower())
        self.assertIn('man', json_second_record.lower())
        self.assertGreater(json_second_record, json_first_record)
    
    def test_get_model_search_order_desc(self):
        res = self.client.get("/api/models/?search=man&order=desc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()[:2]
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertIn('man', json_first_record.lower())
        self.assertIn('man', json_second_record.lower())
        self.assertGreater(json_first_record, json_second_record)

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