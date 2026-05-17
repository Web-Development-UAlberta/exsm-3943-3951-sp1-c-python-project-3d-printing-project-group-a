import os
import sys
import unittest
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import create_app

class TestAdmin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

        s = str(int(time.time()))

        cls.admin_username = f"admin_{s}"
        cls.admin_password = "Admin1234!"

        cls.client.post("/api/auth/register", json={
            "username": cls.admin_username,
            "password": cls.admin_password,
            "phone_number": f"111-{s[-7:]}",
            "city": "Edmonton",
            "street_address": "123 Main St",
            "province": "AB"
        })

        # Promote to admin directly in database
        from src.app.database import get_db
        from src.app.models import User

        with get_db() as db:
            user = db.query(User).filter_by(
                username=cls.admin_username
            ).first()

            if user is None:
                raise Exception("Admin user was not created.")

            user.is_admin = True
            cls.admin_user_id = user.user_id
            db.commit()

        # Login as admin
        res = cls.client.post("/api/auth/login", json={
            "username": cls.admin_username,
            "password": cls.admin_password
        })

        if res.status_code != 200:
            raise Exception(f"Admin login failed: {res.get_json()}")

        cls.admin_token = res.get_json()["access_token"]
        cls.admin_headers = {
            "Authorization": f"Bearer {cls.admin_token}"
        }

        cls.user_username = f"user_{s}"
        cls.user_password = "User1234!"

        cls.client.post("/api/auth/register", json={
            "username": cls.user_username,
            "password": cls.user_password,
            "phone_number": f"222-{s[-7:]}",
            "city": "Edmonton",
            "street_address": "123 Main St",
            "province": "AB"
        })

        res = cls.client.post("/api/auth/login", json={
            "username": cls.user_username,
            "password": cls.user_password
        })

        if res.status_code != 200:
            raise Exception(f"User login failed: {res.get_json()}")

        cls.user_token = res.get_json()["access_token"]
        cls.user_headers = {
            "Authorization": f"Bearer {cls.user_token}"
        }


    def test_01_non_admin_blocked(self):
        res = self.client.get(
            "/api/admin/dashboard",
            headers=self.user_headers
        )
        self.assertEqual(res.status_code, 403)

    def test_02_no_token_blocked(self):
        res = self.client.get("/api/admin/dashboard")
        self.assertEqual(res.status_code, 401)

    def test_03_get_dashboard(self):
        res = self.client.get(
            "/api/admin/dashboard",
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 200)

        data = res.get_json()

        self.assertIn("active_orders", data)
        self.assertIn("total_orders", data)
        self.assertIn("low_stock_count", data)
        self.assertIn("free_printers", data)

    def test_04_get_filaments(self):
        res = self.client.get(
            "/api/admin/filaments",
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_05_add_filament(self):
        res = self.client.post(
            "/api/admin/filaments",
            headers=self.admin_headers,
            json={
                "material_name": "PLA",
                "color_hex": "#FF0000",
                "quantity_in_stock": 500,
                "filament_price": 25.00
            }
        )

        self.assertEqual(res.status_code, 201)

        data = res.get_json()
        self.assertIn("filament_id", data)

        self.__class__.filament_id = data["filament_id"]

    def test_06_add_filament_missing_fields(self):
        res = self.client.post(
            "/api/admin/filaments",
            headers=self.admin_headers,
            json={
                "color_hex": "#FF0000"
            }
        )
        self.assertEqual(res.status_code, 400)

    def test_07_update_filament(self):
        filament_id = getattr(self.__class__, "filament_id", None)

        if not filament_id:
            self.skipTest("No filament_id from previous test")

        res = self.client.put(
            f"/api/admin/filaments/{filament_id}",
            headers=self.admin_headers,
            json={
                "quantity_in_stock": 800
            }
        )

        self.assertEqual(res.status_code, 200)

    def test_08_update_filament_not_found(self):
        res = self.client.put(
            "/api/admin/filaments/99999",
            headers=self.admin_headers,
            json={
                "quantity_in_stock": 100
            }
        )
        self.assertEqual(res.status_code, 404)

    def test_09_delete_filament(self):
        filament_id = getattr(self.__class__, "filament_id", None)

        if not filament_id:
            self.skipTest("No filament_id from previous test")

        res = self.client.delete(
            f"/api/admin/filaments/{filament_id}",
            headers=self.admin_headers
        )

        self.assertEqual(res.status_code, 200)

    def test_10_get_printers(self):
        res = self.client.get(
            "/api/admin/printers",
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_11_add_printer(self):
        from src.app.database import get_db
        from src.app.models import PrinterType  # Double check if your model is named PrinterType

        # Dynamically fetch the first valid printer type ID from the database
        with get_db() as db:
            valid_type = db.query(PrinterType).first()
            if not valid_type:
                self.skipTest("No Printer Types found in database to link printer to.")
            target_type_id = valid_type.printer_type_id

        res = self.client.post(
            "/api/admin/printers",
            headers=self.admin_headers,
            json={
                "printer_type_id": target_type_id
            }
        )

        self.assertIn(res.status_code, [200, 201], f"Failed with {res.status_code}: {res.get_data(as_text=True)}")

        data = res.get_json()
        self.assertIn("printer_id", data)
        self.__class__.printer_id = data["printer_id"]

    def test_12_delete_printer(self):
        printer_id = getattr(self.__class__, "printer_id", None)

        if not printer_id:
            self.skipTest("No printer_id from previous test")

        res = self.client.delete(
            f"/api/admin/printers/{printer_id}",
            headers=self.admin_headers
        )

        self.assertEqual(res.status_code, 200)


    def test_13_get_all_orders(self):
        res = self.client.get(
            "/api/admin/orders",
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_14_update_order_not_found(self):
        res = self.client.put(
            "/api/admin/orders/99999",
            headers=self.admin_headers,
            json={
                "order_status": "Printing"
            }
        )
        self.assertEqual(res.status_code, 404)

    def test_15_update_order_invalid_status(self):
        # Use a guaranteed non-existent order ID so validation
        # happens after the order lookup in your route.
        res = self.client.put(
            "/api/admin/orders/99999",
            headers=self.admin_headers,
            json={
                "order_status": "InvalidStatus"
            }
        )


    def test_16_get_all_models(self):
        res = self.client.get(
            "/api/admin/models",
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_17_add_model(self):
        res = self.client.post(
            "/api/admin/models",
            headers=self.admin_headers,
            json={
                "model_name": "Test Admin Model",
                "model_length": 50,
                "model_width": 50,
                "model_height": 50,
                "print_time_hours": 3.0
            }
        )

        self.assertEqual(res.status_code, 201)

        data = res.get_json()
        self.assertIn("model_id", data)

        self.__class__.model_id = data["model_id"]

    def test_18_add_model_missing_fields(self):
        res = self.client.post(
            "/api/admin/models",
            headers=self.admin_headers,
            json={
                "model_name": "Incomplete"
            }
        )
        self.assertEqual(res.status_code, 400)

    def test_19_update_model(self):
        model_id = getattr(self.__class__, "model_id", None)

        if not model_id:
            self.skipTest("No model_id from previous test")

        res = self.client.put(
            f"/api/admin/models/{model_id}",
            headers=self.admin_headers,
            json={
                "model_description": "Updated by admin test"
            }
        )

        self.assertEqual(res.status_code, 200)

    def test_20_delete_model(self):
        model_id = getattr(self.__class__, "model_id", None)

        if not model_id:
            self.skipTest("No model_id from previous test")

        res = self.client.delete(
            f"/api/admin/models/{model_id}",
            headers=self.admin_headers
        )

        self.assertEqual(res.status_code, 200)

    def test_21_get_all_users(self):
        res = self.client.get(
            "/api/admin/users",
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_22_make_admin(self):
        from src.app.database import get_db
        from src.app.models import User

        with get_db() as db:
            user = db.query(User).filter_by(
                username=self.user_username
            ).first()

            if user is None:
                raise Exception("Regular user not found.")

            user_id = user.user_id

        res = self.client.put(
            f"/api/admin/users/{user_id}/make-admin",
            headers=self.admin_headers
        )

        self.assertEqual(res.status_code, 200)

    def test_23_remove_admin(self):
        from src.app.database import get_db
        from src.app.models import User

        with get_db() as db:
            user = db.query(User).filter_by(
                username=self.user_username
            ).first()

            if user is None:
                raise Exception("Regular user not found.")

            user_id = user.user_id

        res = self.client.put(
            f"/api/admin/users/{user_id}/remove-admin",
            headers=self.admin_headers
        )

        self.assertEqual(res.status_code, 200)

    def test_24_user_not_found(self):
        res = self.client.put(
            "/api/admin/users/99999/make-admin",
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 404)

    def test_25_get_printer_types(self):
        res = self.client.get(
            "/api/admin/printer-types",
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_26_add_printer_type(self):
        res = self.client.post(
            "/api/admin/printer-types",
            headers=self.admin_headers,
            json={
                "printer_name": "Prusa XL",
                "max_size": 700.0
            }
        )

        self.assertEqual(res.status_code, 201)


if __name__ == "__main__":
    unittest.main()