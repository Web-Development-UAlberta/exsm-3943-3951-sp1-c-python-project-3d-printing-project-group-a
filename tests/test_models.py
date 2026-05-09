import os
import sys
import unittest
from datetime import date

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app.models import (Base, User, Filament, PrinterType, Printer,Tag, Model, ModelFilament, OrderHeader, OrderDetail)


class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)

    def test_connection(self):
        result = self.session.execute(text("SELECT 1")).scalar()
        self.assertEqual(result, 1)

    # User
    def test_user_creation(self):
        user = User(
            username="john_doe",
            full_name="John Doe",
            email="john@test.com",
            phone_number="123456",
            city="Toronto",
            street_address="Main Street",
            province="ON",
        )

        self.session.add(user)
        self.session.commit()

        saved_user = self.session.query(User).filter_by(username="john_doe").one()

        self.assertEqual(saved_user.username, "john_doe")
        self.assertEqual(saved_user.email, "john@test.com")

    # Filament
    def test_filament(self):
        filament = Filament(
            material_name="PLA",
            color_hex="#FFFFFF",
            filament_price=20.0
        )

        self.session.add(filament)
        self.session.commit()

        result = self.session.query(Filament).first()

        self.assertEqual(result.material_name, "PLA")
        self.assertEqual(result.filament_price, 20.0)

    # Printer Type 
    def test_printer_relationship(self):
        filament = Filament(material_name="PLA", filament_price=10)
        printer_type = PrinterType(printer_name="MK4", max_size=300)

        printer = Printer(
            filament=filament,
            printer_type=printer_type
        )

        self.session.add(printer)
        self.session.commit()

        result = self.session.query(Printer).first()

        self.assertEqual(result.printer_type.printer_name, "MK4")
        self.assertEqual(result.filament.material_name, "PLA")

    # Model and Tag
    def test_model_and_tag(self):
        tag = Tag(tag_name="Gaming")
        filament = Filament(material_name="PLA", filament_price=15)
        printer_type = PrinterType(printer_name="Ender", max_size=220)

        printer = Printer(
            filament=filament,
            printer_type=printer_type
        )

        model = Model(
            model_name="Iron Man",
            model_length=10,
            model_width=10,
            model_height=10,
            tag=tag,
            printer=printer
        )

        self.session.add(model)
        self.session.commit()

        saved = self.session.query(Model).first()

        self.assertEqual(saved.model_name, "Iron Man")
        self.assertEqual(saved.tag.tag_name, "Gaming")

    # Model-Filament Link (many to many)
    def test_model_filament(self):
        filament = Filament(material_name="PLA", filament_price=10)
        tag = Tag(tag_name="Test")
        printer_type = PrinterType(printer_name="MK4", max_size=300)

        printer = Printer(
            filament=filament,
            printer_type=printer_type
        )

        model = Model(
            model_name="Desk Organizer",
            tag=tag,
            printer=printer
        )

        self.session.add_all([filament, tag, printer_type, printer, model])
        self.session.commit()

        link = ModelFilament(model=model, filament=filament)
        self.session.add(link)
        self.session.commit()

        result = self.session.query(Model).filter_by(model_name="Desk Organizer").one()

        self.assertEqual(result.filament_links[0].filament.material_name, "PLA")

    # Order Flow
    def test_order_flow(self):
        user = User(
            username="order_user",
            phone_number="999",
            city="Kingston",
            street_address="Street",
            province="ON",
        )

        filament = Filament(material_name="PETG", filament_price=25)
        tag = Tag(tag_name="Games")

        printer_type = PrinterType(printer_name="Prusa", max_size=300)

        printer = Printer(
            filament=filament,
            printer_type=printer_type
        )

        model = Model(
            model_name="Phone Stand",
            tag=tag,
            printer=printer
        )

        order = OrderHeader(
            order_date=date.today(),
            shipping_price=10,
            extra_fee=2,
            total_price=60,
            order_tracking_number="TRK123",
            order_status="Pending",
            payment_status="Pending",
            user=user,
        )

        detail = OrderDetail(
            order_quantity=2,
            infill_percent=50,
            scale=100,
            unit_price=30,
            model=model,
            order_header=order,
            filament=filament,
        )

        self.session.add(detail)
        self.session.commit()

        saved_order = self.session.query(OrderHeader).first()

        self.assertEqual(len(saved_order.details), 1)
        self.assertEqual(saved_order.details[0].model.model_name, "Phone Stand")

    # Unique Username
    def test_unique_username(self):
        user1 = User(
            username="same",
            phone_number="111",
            city="C",
            street_address="S",
            province="ON"
        )

        user2 = User(
            username="same",
            phone_number="222",
            city="C",
            street_address="S",
            province="ON"
        )

        self.session.add(user1)
        self.session.commit()

        self.session.add(user2)

        with self.assertRaises(Exception):
            self.session.commit()

    # edge case 
    def test_user_missing_username(self):
        user = User(
            username=None,
            phone_number="123",
            city="C",
            street_address="S",
            province="ON"
        )

        self.session.add(user)

        with self.assertRaises(Exception):
            self.session.commit()

    # empty string edge case
    def test_user_empty_username(self):
        user = User(
            username="",
            phone_number="123",
            city="C",
            street_address="S",
            province="ON"
        )

        self.session.add(user)

        with self.assertRaises(Exception):
            self.session.commit()

    # Invalid data 
    def test_negative_filament_price(self):
        filament = Filament(
            material_name="PLA",
            filament_price=-10
        )

        self.session.add(filament)

        with self.assertRaises(Exception):
            self.session.commit()

    # Invalid dimensions 
    def test_negative_model_dimensions(self):
        tag = Tag(tag_name="Test")
        filament = Filament(material_name="PLA", filament_price=10)
        printer_type = PrinterType(printer_name="MK4", max_size=300)

        printer = Printer(filament=filament, printer_type=printer_type)

        model = Model(
            model_name="Bad Model",
            model_length=-5,
            model_width=10,
            model_height=10,
            tag=tag,
            printer=printer
        )

        self.session.add(model)

        with self.assertRaises(Exception):
            self.session.commit()

    # Update test
    def test_update_user(self):
        user = User(
            username="old_name",
            phone_number="123",
            city="C",
            street_address="S",
            province="ON"
        )

        self.session.add(user)
        self.session.commit()

        user.username = "new_name"
        self.session.commit()

        updated = self.session.query(User).filter_by(username="new_name").one()

        self.assertEqual(updated.username, "new_name")

    # delete test
    def test_delete_user(self):
        user = User(
            username="delete_me",
            phone_number="123",
            city="C",
            street_address="S",
            province="ON"
        )

        self.session.add(user)
        self.session.commit()

        self.session.delete(user)
        self.session.commit()

        result = self.session.query(User).filter_by(username="delete_me").all()

        self.assertEqual(len(result), 0)

    # multiple records test
    def test_multiple_users(self):
        users = [
            User(username="u1", phone_number="1", city="C", street_address="S", province="ON"),
            User(username="u2", phone_number="2", city="C", street_address="S", province="ON"),
            User(username="u3", phone_number="3", city="C", street_address="S", province="ON"),
        ]

        self.session.add_all(users)
        self.session.commit()

        result = self.session.query(User).all()

        self.assertEqual(len(result), 3)


if __name__ == "__main__":
    unittest.main()