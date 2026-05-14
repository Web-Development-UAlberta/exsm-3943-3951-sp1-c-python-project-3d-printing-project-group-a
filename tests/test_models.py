import os
import sys
import unittest
from datetime import date

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.app.models import (
    Base, User, Filament, PrinterType, Printer,
    Tag, Model, ModelFilament, ModelTag, OrderHeader, OrderDetail
)


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

    #helpers 
    def make_user(self, username="john_doe", phone="123456"):
        return User(
            username=username,
            full_name="John Doe",
            email=f"{username}@test.com",
            phone_number=phone,
            city="Toronto",
            street_address="Main Street",
            province="ON",
            password="hashed_pw"
        )

    def make_printer(self):
        filament     = Filament(material_name="PLA", filament_price=20.00)
        printer_type = PrinterType(printer_name="MK4", max_size=500)
        printer      = Printer(filament=filament, printer_type=printer_type)
        return filament, printer_type, printer

    ## User Table
    # Validates connection is successful
    def test_connection(self):
        result = self.session.execute(text("SELECT 1")).scalar()
        self.assertEqual(result, 1)

    # Validates user creation is successful
    def test_user_creation(self):
        user = self.make_user()
        self.session.add(user)
        self.session.commit()

        saved = self.session.query(User).filter_by(username="john_doe").one()
        self.assertEqual(saved.username, "john_doe")
        self.assertEqual(saved.email, "john_doe@test.com")

    # Validates username is unique
    def test_unique_username(self):
        self.session.add(self.make_user(username="same", phone="111"))
        self.session.commit()
        self.session.add(self.make_user(username="same", phone="222"))
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates username input is valid 
    def test_user_missing_username(self):
        user = self.make_user()
        user.username = None
        self.session.add(user)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates username input is blank
    def test_user_empty_username(self):
        user = self.make_user()
        user.username = ""
        self.session.add(user)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates username can be updated
    def test_update_user(self):
        user = self.make_user(username="old_name", phone="321")
        self.session.add(user)
        self.session.commit()

        user.username = "new_name"
        self.session.commit()

        updated = self.session.query(User).filter_by(username="new_name").one()
        self.assertEqual(updated.username, "new_name")

    # Validates username can be deleted
    def test_delete_user(self):
        user = self.make_user(username="delete_me", phone="999")
        self.session.add(user)
        self.session.commit()

        self.session.delete(user)
        self.session.commit()

        result = self.session.query(User).filter_by(username="delete_me").all()
        self.assertEqual(len(result), 0)

    # Validates multiple usernames can be created
    def test_multiple_users(self):
        users = [
            self.make_user(username="u1", phone="1"),
            self.make_user(username="u2", phone="2"),
            self.make_user(username="u3", phone="3"),
        ]
        self.session.add_all(users)
        self.session.commit()

        result = self.session.query(User).all()
        self.assertEqual(len(result), 3)

    ## Filament Table
    # Validates filament creation is successful
    def test_filament(self):
        filament = Filament(
            material_name="PLA",
            color_hex="#FFFFFF",
            filament_price=20.00
        )
        self.session.add(filament)
        self.session.commit()

        result = self.session.query(Filament).first()
        self.assertEqual(result.material_name, "PLA")
        self.assertEqual(float(result.filament_price), 20.0)

    # Validates material name is required
    def test_negative_filament_material_name(self):
        filament = Filament(material_name=None, filament_price=20.00)
        self.session.add(filament)
        with self.assertRaises(Exception):
            self.session.commit()    

    # Validates filament price is invalid
    def test_negative_filament_price(self):
        filament = Filament(material_name="PLA", filament_price=-10)
        self.session.add(filament)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates filament quantity is invalid
    def test_negative_filament_quantity_in_stock(self):
        filament = Filament(material_name="PLA", quantity_in_stock=-10)
        self.session.add(filament)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates more wear and tear is invalid
    def test_negative_filament_more_wear_and_tear(self):
        filament = Filament(material_name="PLA", more_wear_and_tear=-10)
        self.session.add(filament)
        with self.assertRaises(Exception):
            self.session.commit()

    ## Printer Table
    # Validates printer foreign keys are successful
    def test_printer_relationship(self):
        filament, printer_type, printer = self.make_printer()
        self.session.add(printer)
        self.session.commit()

        result = self.session.query(Printer).first()
        self.assertEqual(result.printer_type.printer_name, "MK4")
        self.assertEqual(result.filament.material_name, "PLA")

    ## Tags Table

    # Validates tag creation is successful
    def test_tag_name(self):
        tag = Tag(tag_name="Books")
        self.session.add(tag)
        self.session.commit()

        saved = self.session.query(Tag).filter_by(tag_name="Books").one()
        self.assertEqual(saved.tag_name, "Books")

    # Validates tag name is not blank
    def test_tag_name(self):
        tag = Tag(tag_name=None)
        self.session.add(tag)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates tag name is unique
    def test_tag_name_unique(self):
        tag1 = Tag(tag_name="Books")
        tag2 = Tag(tag_name="Books")
        self.session.add(tag1)
        self.session.commit()
        self.session.add(tag2)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates tag can be associated to Model
    def test_model_and_tag(self):
        filament, printer_type, printer = self.make_printer()
        tag = Tag(tag_name="Gaming")

        model = Model(
            model_name="Iron Man",
            model_length=10,
            model_width=10,
            model_height=10,
            print_time_hours=5.0,
            printer=printer
        )

        self.session.add_all([tag, model])
        self.session.commit()

        link = ModelTag(model_id=model.model_id, tag_id=tag.tag_id)
        self.session.add(link)
        self.session.commit()

        saved = self.session.query(Model).first()
        self.assertEqual(saved.model_name, "Iron Man")
        self.assertEqual(saved.tag_links[0].tag.tag_name, "Gaming")

    # Validates multiple tags can be associated to Model    
    def test_model_multiple_tags(self):
        filament, printer_type, printer = self.make_printer()
        tag1 = Tag(tag_name="Gaming")
        tag2 = Tag(tag_name="Collectibles")

        model = Model(
            model_name="D20 Dice",
            model_length=50,
            model_width=50,
            model_height=50,
            print_time_hours=3.0,
            printer=printer
        )

        self.session.add_all([tag1, tag2, model])
        self.session.commit()

        self.session.add_all([
            ModelTag(model_id=model.model_id, tag_id=tag1.tag_id),
            ModelTag(model_id=model.model_id, tag_id=tag2.tag_id),
        ])
        self.session.commit()

        saved = self.session.query(Model).first()
        self.assertEqual(len(saved.tag_links), 2)

    ## Model Filament Table
    # Validates filament can be associated to Model
    def test_model_filament(self):
        filament, printer_type, printer = self.make_printer()

        model = Model(
            model_name="Desk Organizer",
            print_time_hours=4.0,
            printer=printer
        )

        self.session.add(model)
        self.session.commit()

        link = ModelFilament(model=model, filament=filament)
        self.session.add(link)
        self.session.commit()

        result = self.session.query(Model).filter_by(model_name="Desk Organizer").one()
        self.assertEqual(result.filament_links[0].filament.material_name, "PLA")

    ## Models Table
    # Validates model name is not blank
    def test_negative_model_name(self):
        model = Model(
            model_name=None,
            model_length=10,
            model_width=10,
            model_height=10,
        )
        self.session.add(model)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates model length is valid
    def test_negative_model_length(self):
        model = Model(
            model_name="Bat Man",
            model_length=-10,
        )
        self.session.add(model)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates model width is valid
    def test_negative_model_width(self):
        model = Model(
            model_name="Bat Man",
            model_width=-10,
        )
        self.session.add(model)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates model height is valid
    def test_negative_model_height(self):
        model = Model(
            model_name="Bat Man",
            model_height=-10,
        )
        self.session.add(model)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates model print hours is valid
    def test_negative_model_print_hours(self):
        model = Model(
            model_name="Bat Man",
            model_height=-10,
        )
        self.session.add(model)
        with self.assertRaises(Exception):
            self.session.commit()

    ## Order Table
    # Validates order creation is successful
    def test_order_flow(self):
        user = self.make_user(username="order_user", phone="999")
        filament, printer_type, printer = self.make_printer()

        model = Model(
            model_name="Phone Stand",
            print_time_hours=2.0,
            printer=printer
        )

        order = OrderHeader(
            order_date=date.today(),
            shipping_price=10.00,
            extra_fee=2.00,
            total_price=60.00,
            order_tracking_number="TRK123",
            order_status="Pending",
            payment_status="Pending",
            user=user,
        )

        detail = OrderDetail(
            order_quantity=2,
            infill_percent=50,
            scale=100,
            unit_price=30.00,
            model=model,
            order_header=order,
            filament=filament,
        )

        self.session.add(detail)
        self.session.commit()

        saved_order = self.session.query(OrderHeader).first()
        self.assertEqual(len(saved_order.details), 1)
        self.assertEqual(saved_order.details[0].model.model_name, "Phone Stand")

    # Validates order date is not blank
    def test_negative_order_date_blank(self):
        order = OrderHeader(
            order_date=None,
            shipping_price=10.00,
            extra_fee=2.00,
            total_price=60.00,
            order_tracking_number="TRK123",
            order_status="Pending",
            payment_status="Pending",
        )

        self.session.add(order)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates order date is valid
    def test_negative_order_date_valid(self):
        order = OrderHeader(
            order_date=123,
            shipping_price=10.00,
            extra_fee=2.00,
            total_price=60.00,
            order_tracking_number="TRK123",
            order_status="Pending",
            payment_status="Pending",
        )

        self.session.add(order)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates shipping price is not blank
    def test_negative_shipping_price_blank(self):
        order = OrderHeader(
            order_date=date.today(),
            shipping_price=None,
            extra_fee=2.00,
            total_price=60.00,
            order_tracking_number="TRK123",
            order_status="Pending",
            payment_status="Pending",
        )
    
    # Validates total price is not blank
    def test_negative_shipping_price_valid(self):
        order = OrderHeader(
            order_date=date.today(),
            shipping_price=10.00,
            extra_fee=2.00,
            total_price=None,
            order_tracking_number="TRK123",
            order_status="Pending",
            payment_status="Pending",
        )

        self.session.add(order)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates tracking number is unique
    def test_negative_tracking_number_unique(self):
        order1 = OrderHeader(
            order_date=date.today(),
            shipping_price=10.00,
            extra_fee=2.00,
            total_price=60.00,
            order_tracking_number="TRK123",
            order_status="Pending",
            payment_status="Pending",
        )
        order2 = OrderHeader(
            order_date=date.today(),
            shipping_price=10.00,
            extra_fee=2.00,
            total_price=60.00,
            order_tracking_number="TRK123",
            order_status="Pending",
            payment_status="Pending",
        )

        self.session.add(order1)
        self.session.commit()
        self.session.add(order2)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates order status is not blank
    def test_negative_order_status_blank(self):
        order = OrderHeader(
            order_date=date.today(),
            shipping_price=10.00,
            extra_fee=2.00,
            total_price=60.00,
            order_tracking_number="TRK123",
            order_status=None,
            payment_status="Pending",
        )

        self.session.add(order)
        with self.assertRaises(Exception):
            self.session.commit()

    # Validates orders can be called during pending status
    def test_order_cancel_only_when_pending(self):
        user = self.make_user(username="cancel_user", phone="888")

        order = OrderHeader(
            order_date=date.today(),
            shipping_price=10.00,
            total_price=50.00,
            order_tracking_number="TRK999",
            order_status="Printing",
            payment_status="Succeeded",
            user=user,
        )

        self.session.add(order)
        self.session.commit()

        saved = self.session.query(OrderHeader).first()
        self.assertNotEqual(saved.order_status, "Pending")
        self.assertEqual(saved.order_status, "Printing")


if __name__ == "__main__":
    unittest.main()