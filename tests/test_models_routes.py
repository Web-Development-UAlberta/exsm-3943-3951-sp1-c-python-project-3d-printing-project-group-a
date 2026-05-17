import os
import sys
import unittest
import json
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import create_app


class TestModelsRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

        # Get real IDs from database
        res = cls.client.get("/api/models/")
        models = res.get_json()
        if not models:
            raise Exception("No models found in the database. Please run seed.py first.")

        # Find a model that actively contains both filaments and tags to prevent None values
        target_model = None
        for m in models:
            if m.get("filaments") and m.get("tags"):
                target_model = m
                break
        
        if not target_model:
            target_model = models[0]

        cls.model_id    = target_model["model_id"]
        cls.filament_id = target_model["filaments"][0]["filament_id"] if target_model.get("filaments") else None
        cls.tag_id      = target_model["tags"][0]["tag_id"] if target_model.get("tags") else None

    # Pulls a list of all Models
    def test_get_all_models(self):
        res = self.client.get("/api/models/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    # Pulls a specific Model
    def test_get_specific_models(self):
        res = self.client.get(f"/api/models/{self.model_id}")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("model_name", data)

    # Pulls a non-existent Model
    def test_get_model_not_found(self):
        res = self.client.get("/api/models/999999")
        self.assertEqual(res.status_code, 404)

    # Pulls a list of all Tags
    def test_get_all_model_tags(self):
        res = self.client.get("/api/models/?tag_id=")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertGreater(len(res.get_json()), 0)

    # Pulls a specific Tag
    def test_get_model_tag_found(self):
        self.assertIsNotNone(self.tag_id, "Cannot run test: No valid tag_id found in seed data.")
        res = self.client.get(f"/api/models/?tag_id={self.tag_id}")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertGreater(len(res.get_json()), 0, f"API returned an empty list for tag_id: {self.tag_id}")
    
    # Pulls a non-existent Tag
    def test_get_model_tag_not_found(self):
        res = self.client.get("/api/models/?tag_id=999999")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertEqual(len(res.get_json()), 0)

    # Pulls a list of all Filaments
    def test_get_model_all_filament(self):
        res = self.client.get("/api/models/?filament_id=")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertGreater(len(res.get_json()), 0)

    # Pulls a specific Filament
    def test_get_model_filament_found(self):
        self.assertIsNotNone(self.filament_id, "Cannot run test: No valid filament_id found in seed data.")
        res = self.client.get(f"/api/models/?filament_id={self.filament_id}")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertGreater(len(res.get_json()), 0, f"API returned an empty list for filament_id: {self.filament_id}")

    # Pulls a non-existent Filament
    def test_get_model_filter_filament_not_found(self):
        res = self.client.get("/api/models/?filament_id=999999")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertEqual(len(res.get_json()), 0)

    # Pulls a list of Models unordered
    def test_get_model_all_unordered(self):
        res = self.client.get("/api/models/?order=")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    # Pulls a list of Models in ascending order
    def test_get_model_order_asc(self):
        res = self.client.get("/api/models/?order=asc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()
        self.assertGreaterEqual(len(json_list), 2, "API returned fewer than 2 models; cannot verify sorting order.")
        
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertGreaterEqual(json_second_record, json_first_record)

    # Pulls a list of Models in descending order
    def test_get_model_order_desc(self):
        res = self.client.get("/api/models/?order=desc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()
        self.assertGreaterEqual(len(json_list), 2, "API returned fewer than 2 models; cannot verify sorting order.")
        
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertLessEqual(json_second_record, json_first_record)

    # New & Restructured tests to prevent previous IndexError crashes
    def test_get_model_filament_asc(self):
        res = self.client.get("/api/models/?order=asc")
        self.assertEqual(res.status_code, 200)
        json_list = res.get_json()
        self.assertGreater(len(json_list), 0, "API returned an empty list of models.")
        self.assertTrue(json_list[0].get('filaments'), "The first model record contains an empty 'filaments' array.")
        
        json_first_record = json_list[0]['filaments'][0]['material_name']
        self.assertIsInstance(json_first_record, str)

    def test_get_model_filament_tag_asc(self):
        res = self.client.get("/api/models/?order=asc")
        self.assertEqual(res.status_code, 200)
        json_list = res.get_json()
        self.assertGreater(len(json_list), 0, "API returned an empty list of models.")
        self.assertTrue(json_list[0].get('tags'), "The first model record contains an empty 'tags' array.")
        
        json_first_record = json_list[0]['tags'][0]['tag_name']
        self.assertIsInstance(json_first_record, str)

    def test_get_model_filament_tag_desc(self):
        res = self.client.get("/api/models/?order=desc")
        self.assertEqual(res.status_code, 200)
        json_list = res.get_json()
        self.assertGreater(len(json_list), 0, "API returned an empty list of models.")
        self.assertTrue(json_list[0].get('tags'), "The first model record contains an empty 'tags' array.")
        
        json_first_record = json_list[0]['tags'][0]['tag_name']
        self.assertIsInstance(json_first_record, str)

    def test_get_model_search_filament_tag_asc(self):
        # Explicit search criteria to find items safely
        res = self.client.get("/api/models/?order=asc&search=")
        self.assertEqual(res.status_code, 200)
        json_list = res.get_json()
        self.assertGreater(len(json_list), 0, "API search filter returned an empty list.")
        
        json_first_record = json_list[0]['model_name']
        self.assertIsInstance(json_first_record, str)

    def test_get_model_search_filament_tag_desc(self):
        res = self.client.get("/api/models/?order=desc&search=")
        self.assertEqual(res.status_code, 200)
        json_list = res.get_json()
        self.assertGreater(len(json_list), 0, "API search filter returned an empty list.")
        
        json_first_record = json_list[0]['model_name']
        self.assertIsInstance(json_first_record, str)

    def test_get_model_search_tag_asc(self):
        res = self.client.get("/api/models/?order=asc&search=")
        self.assertEqual(res.status_code, 200)
        json_list = res.get_json()
        self.assertGreater(len(json_list), 0, "API search filter returned an empty list.")
        
        json_first_record = json_list[0]['model_name']
        self.assertIsInstance(json_first_record, str)

    def test_get_model_search_tag_desc(self):
        res = self.client.get("/api/models/?order=desc&search=")
        self.assertEqual(res.status_code, 200)
        json_list = res.get_json()
        self.assertGreater(len(json_list), 0, "API search filter returned an empty list.")
        
        json_first_record = json_list[0]['model_name']
        self.assertIsInstance(json_first_record, str)


if __name__ == '__main__':
    unittest.main()
