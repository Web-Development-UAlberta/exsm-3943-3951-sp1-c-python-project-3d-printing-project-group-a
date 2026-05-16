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

    # Pulls a list of all Models
    def test_get_all_models(self):
        res = self.client.get("/api/models/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    # Pulls a specific Model
    def test_get_specific_models(self):
        res = self.client.get("/api/models/2")
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.get_json()), 0)
        json_list = res.get_json()
        json_first_record = json_list['model_name']
        self.assertEqual(json_first_record.lower(), 'Desk Vase'.lower())

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
        res = self.client.get("/api/models/?tag_id=2")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertGreater(len(res.get_json()), 0)
        json_list = res.get_json()[:1]
        json_first_record = json_list[0]['tags'][0]['tag_name']
        self.assertEqual(json_first_record.lower(), 'Gaming'.lower())
    
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
        res = self.client.get("/api/models/?filament_id=2")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertGreater(len(res.get_json()), 0)
        json_list = res.get_json()[:1]
        json_first_record = json_list[0]['filaments'][0]['material_name']
        self.assertEqual(json_first_record.lower(), 'PLA'.lower())

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
        json_list = res.get_json()[:2]
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertGreater(json_second_record, json_first_record)

    # Pulls a list of Models in descending order
    def test_get_model_order_desc(self):
        res = self.client.get("/api/models/?order=desc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()[:2]
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertGreater(json_first_record, json_second_record)

    # Pulls a list of all Models on empty search
    def test_get_model_search_all(self):
        res = self.client.get("/api/models/?search=")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    # Pulls a list of Models with matching search words
    def test_get_model_search_found(self):
        res = self.client.get("/api/models/?search=hammer")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()[:1]
        json_first_record = json_list[0]['model_name']
        self.assertEqual(json_first_record.lower(), 'Hammer'.lower())

    # Pulls a list of Models with ummatched search words
    def test_get_model_search_not_found(self):
        res = self.client.get("/api/models/?search=lexus")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertEqual(len(res.get_json()), 0)

    # Pulls a list of Models with matched Search words filtered by Tag & Filament, in ascending order
    def test_get_model_search_filament_tag_asc(self):
        res = self.client.get("/api/models/?search=man&tag_id=4&filament_id=2&order=asc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertIn('man', json_first_record.lower())
        self.assertIn('man', json_second_record.lower())
        self.assertGreater(json_second_record, json_first_record)

    # Pulls a list of Models with matched Search words filtered by Tag & Filament, in descending order
    def test_get_model_search_filament_tag_desc(self):
        res = self.client.get("/api/models/?search=man&tag_id=4&filament_id=2&order=desc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertIn('man', json_first_record.lower())
        self.assertIn('man', json_second_record.lower())
        self.assertGreater(json_first_record, json_second_record)

    # Pulls a list of Models with matched Search words filtered by Tag, in ascending order
    def test_get_model_search_tag_asc(self):
        res = self.client.get("/api/models/?search=man&tag_id=4&order=asc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertIn('man', json_first_record.lower())
        self.assertIn('man', json_second_record.lower())
        self.assertGreater(json_second_record, json_first_record)

    # Pulls a list of Models with matched Search words filtered by Tag, in descending order
    def test_get_model_search_tag_desc(self):
        res = self.client.get("/api/models/?search=man&tag_id=4&order=desc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertIn('man', json_first_record.lower())
        self.assertIn('man', json_second_record.lower())
        self.assertGreater(json_first_record, json_second_record)

    # Pulls a list of Models with matched Search words in ascending order
    def test_get_model_search_asc(self):
        res = self.client.get("/api/models/?search=man&order=asc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertIn('man', json_first_record.lower())
        self.assertIn('man', json_second_record.lower())
        self.assertGreater(json_second_record, json_first_record)

    # Pulls a list of Models with matched Search words in descending order
    def test_get_model_search_desc(self):
        res = self.client.get("/api/models/?search=man&order=desc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()
        json_first_record = json_list[0]['model_name']
        json_second_record = json_list[1]['model_name']
        self.assertIn('man', json_first_record.lower())
        self.assertIn('man', json_second_record.lower())
        self.assertGreater(json_first_record, json_second_record)

    # Pulls a list of Models filtered by Tag & Filament, in ascending order
    def test_get_model_filament_tag_asc(self):
        res = self.client.get("/api/models/?tag_id=4&filament_id=2&order=asc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()
        json_first_record = json_list[0]['tags'][0]['tag_name']
        json_second_record = json_list[1]['tags'][0]['tag_name']
        self.assertEqual(json_first_record, json_second_record) 

    # Pulls a list of Models filtered by Tag & Filament, in ascending order
    def test_get_model_filament_tag_desc(self):
        res = self.client.get("/api/models/?tag_id=4&filament_id=2&order=desc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()
        json_first_record = json_list[0]['tags'][0]['tag_name']
        json_second_record = json_list[1]['tags'][0]['tag_name']
        self.assertEqual(json_first_record, json_second_record)

    # Pulls a list of Models filtered by Filament, in ascending order
    def test_get_model_filament_asc(self):
        res = self.client.get("/api/models/?filament_id=2&order=asc")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        json_list = res.get_json()
        json_first_record = json_list[0]['filaments'][0]['material_name']
        json_second_record = json_list[1]['filaments'][0]['material_name']
        self.assertEqual(json_second_record, json_first_record) 

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

    # Validates a file upload is successful
    def test_file_upload_success(self):
        file_content = b"3D model of Super Man"
        filename = "super_man_3d_model.3tl"
        upload = {'file': (io.BytesIO(file_content), filename)}
        res = self.client.post("/api/models/upload", data=upload, content_type='multipart/form-data')
        self.assertEqual(res.status_code, 200)

    # Validates a file upload file extension is valid
    def test_file_upload_success(self):
        file_content = b"3D model of Super Man"
        filename = "super_man_3d_model.jpg"
        upload = {'file': (io.BytesIO(file_content), filename)}
        res = self.client.post("/api/models/upload", data=upload, content_type='multipart/form-data')
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()