import unittest
from src.app import create_app
from src.app.database import get_db
from src.app.models import Filament


class TestFilaments(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

        with get_db() as db:
            cls.filament = db.query(Filament).first()

        assert cls.filament is not None, "No filaments found in DB"

    def test_get_all_filaments(self):
        res = self.client.get("/api/filaments/")

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertGreater(len(res.get_json()), 0)

    def test_filter_by_material(self):
        res = self.client.get("/api/filaments/?material=PLA")

        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        for f in data:
            self.assertEqual(f["material_name"], "PLA")

    def test_filter_by_manufacturer(self):
        res = self.client.get("/api/filaments/?manufacturer=Hatchbox")

        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        for f in data:
            self.assertEqual(f["manufacturer"], "Hatchbox")

    def test_in_stock_filter(self):
        res = self.client.get("/api/filaments/?in_stock=true")

        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        for f in data:
            self.assertTrue(f["quantity_in_stock"] > 0)


if __name__ == "__main__":
    unittest.main()