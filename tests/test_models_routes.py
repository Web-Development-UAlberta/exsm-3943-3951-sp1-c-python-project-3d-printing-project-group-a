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

    # Validates missing json for quote calculations
    def test_quote_missing_fields(self):
        res = self.client.post("/api/models/quote", json={
        })
        self.assertEqual(res.status_code, 400)

    # Validates missing model_id field for quote calculations
    def test_quote_missing_model(self):
        res = self.client.post("/api/models/quote", json={
            "filament_id": 2,
            "scale": 50,
            "infill_percent": 50,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 400)

    # Validates missing filament_id field for quote calculations
    def test_quote_missing_filament(self):
        res = self.client.post("/api/models/quote", json={
            "model_id": 2,
            "scale": 50,
            "infill_percent": 50,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 400)

    # Validates missing scale field for quote calculations
    def test_quote_missing_scale(self):
        res = self.client.post("/api/models/quote", json={
            "model_id":2,
            "filament_id": 2,
            "infill_percent": 50,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 400)

    # Validates missing infill field for quote calculations
    def test_quote_missing_infill(self):
        res = self.client.post("/api/models/quote", json={
            "model_id":2,
            "filament_id": 2,
            "scale": 50,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 400)       

    # Validates missing color count field for quote calculations
    def test_quote_missing_color_count(self):
        res = self.client.post("/api/models/quote", json={
            "model_id":2,
            "filament_id": 2,
            "scale": 50,
            "infill_percent": 50
        })
        self.assertEqual(res.status_code, 400)    

    # Validates require fields exists for quote calculations
    def test_quote_required_fields(self):
        res = self.client.post("/api/models/quote", json={
            "model_id":2,
            "filament_id": 2,
            "scale": 50,
            "infill_percent": 50,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 200)

    # Validates invalid model input for quote caluclations
    def test_quote_invalid_model(self):
        res = self.client.post("/api/models/quote", json={
            "model_id": 99999,
            "filament_id": 2,
            "scale": 50,
            "infill_percent": 50,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 404)

    # Validates invalid filament input for quote caluclations
    def test_quote_invalid_filament(self):
        res = self.client.post("/api/models/quote", json={
            "model_id": 2,
            "filament_id": 999999,
            "scale": 50,
            "infill_percent": 50,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 404)

    # Validates invalid scale input for quote caluclations
    def test_quote_invalid_scale(self):
        res = self.client.post("/api/models/quote", json={
            "model_id":2,
            "filament_id": 2,
            "scale": 999,
            "infill_percent": 50,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 400)

    # Validates invalid infill input for quote calculations
    def test_quote_invalid_infill(self):
        res = self.client.post("/api/models/quote", json={
            "model_id": 2,
            "filament_id": 2,
            "scale": 50,
            "infill_percent": 150,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 400)

    # Validates no surcharge applied for single color printing
    def test_quote_surcharge_single(self):
        res = self.client.post("/api/models/quote", json={
            "model_id": 2,
            "filament_id": 2,
            "scale": 50,
            "infill_percent": 50,
            "color_count": 1
        })
        self.assertEqual(res.status_code, 200)
        json_list = res.get_json()
        json_first_record = json_list['multicolor_surcharge']
        self.assertEqual(json_first_record, 0) 

    # Validates surcharge applied for multicolor printing
    def test_quote_surcharge_multi(self):
        res = self.client.post("/api/models/quote", json={
            "model_id": 2,
            "filament_id": 2,
            "scale": 50,
            "infill_percent": 50,
            "color_count": 2
        })
        self.assertEqual(res.status_code, 200)
        json_list = res.get_json()
        json_first_record = json_list['multicolor_surcharge']
        self.assertGreater(json_first_record, 0)

    # Validates a file upload file is present
    def test_file_upload_missing_file(self):
        res = self.client.post("/api/models/upload", data={}, content_type='multipart/form-data')
        self.assertEqual(res.status_code, 400)

    # Validates a file upload filename is not blank
    def test_file_upload_blank_filename(self):
        filename = ""
        file_content = b"Test"
        data = {'file': (io.BytesIO(file_content), filename)}
        res = self.client.post("/api/models/upload", data=data, content_type='multipart/form-data')
        self.assertEqual(res.status_code, 400)

    # Validates a file upload file extension is valid
    def test_file_upload_success(self):
        file_content = b"3D model of Super Man"
        filename = "super_man_3d_model.jpg"
        upload = {'file': (io.BytesIO(file_content), filename)}
        res = self.client.post("/api/models/upload", data=upload, content_type='multipart/form-data')
        self.assertEqual(res.status_code, 200)

    # Validates a file upload is successful
    def test_file_upload_success(self):
        file_content = b"3D model of Super Man"
        filename = "super_man_3d_model.3tl"
        upload = {'file': (io.BytesIO(file_content), filename)}
        res = self.client.post("/api/models/upload", data=upload, content_type='multipart/form-data')
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
