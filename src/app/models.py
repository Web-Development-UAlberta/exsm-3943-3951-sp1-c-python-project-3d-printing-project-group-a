from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey,
    Float, Boolean, Date, Text, Enum, DECIMAL
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import CheckConstraint

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# USer
class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("username IS NOT NULL AND username != ''", name="username_not_empty"),
    )

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200), unique=True, nullable=False)
    full_name = Column(String(200))
    email = Column(String(250), unique=True)
    phone_number = Column(String(15), unique=True, nullable=False)
    city = Column(String(100), nullable=False)
    street_address = Column(String(250), nullable=False)
    province = Column(String(2), nullable=False)
    postal_code = Column(String(10))
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    orders = relationship("OrderHeader", back_populates="user")


# Filament
class Filament(Base):
    __tablename__ = "filament"
    __table_args__ = (
        CheckConstraint("filament_price >= 0", name="filament_price_positive"),
    )

    filament_id = Column(Integer, primary_key=True, autoincrement=True)
    material_name = Column(String(100), nullable=False)
    color_hex = Column(String(250))
    quantity_in_stock = Column(Float)
    manufacturer = Column(String(100))
    more_wear_and_tear = Column(DECIMAL(5, 2))
    finish_filament = Column(String(100))
    filament_price = Column(DECIMAL(10,2), nullable=False)

    printers = relationship("Printer", back_populates="filament")
    model_links = relationship("ModelFilament", back_populates="filament")
    order_details = relationship("OrderDetail", back_populates="filament")


# Printer Type
class PrinterType(Base):
    __tablename__ = "printer_type"

    printer_type_id = Column(Integer, primary_key=True, autoincrement=True)
    printer_name = Column(String(100))
    max_size = Column(Float, nullable=False)

    printers = relationship("Printer", back_populates="printer_type")


# Printer
class Printer(Base):
    __tablename__ = "printer"

    printer_id = Column(Integer, primary_key=True, autoincrement=True)
    filament_id = Column(Integer, ForeignKey("filament.filament_id"))
    printer_type_id = Column(Integer, ForeignKey("printer_type.printer_type_id"))

    filament = relationship("Filament", back_populates="printers")
    printer_type = relationship("PrinterType", back_populates="printers")
    models = relationship("Model", back_populates="printer")


# Tag
class Tag(Base):
    __tablename__ = "tag"

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String(100), unique=True, nullable=False)

    model_links = relationship("ModelTag", back_populates="tag")


# Model
class Model(Base):
    __tablename__ = "model"
    __table_args__ = (
        CheckConstraint("model_length >= 0", name="length_positive"),
        CheckConstraint("model_width >= 0", name="width_positive"),
        CheckConstraint("model_height >= 0", name="height_positive"),
    )
    
    model_id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(100), nullable=False)
    model_length = Column(Float)
    model_width = Column(Float)
    model_height = Column(Float)
    model_description = Column(Text)
    model_file = Column(String(500))
    print_time_hours = Column(DECIMAL(6, 2))

    printer_id = Column(Integer, ForeignKey("printer.printer_id"))

    tag_links   = relationship("ModelTag", back_populates="model")
    printer = relationship("Printer", back_populates="models")

    filament_links = relationship("ModelFilament", back_populates="model")
    order_details = relationship("OrderDetail", back_populates="model")

# ModelTag Table
class ModelTag(Base):
    __tablename__ = "model_tag"

    model_id = Column(Integer, ForeignKey("model.model_id"), primary_key=True)
    tag_id   = Column(Integer, ForeignKey("tag.tag_id"), primary_key=True)

    model = relationship("Model", back_populates="tag_links")
    tag   = relationship("Tag", back_populates="model_links")


# Many-to-Many: Model_Filament
class ModelFilament(Base):
    __tablename__ = "model_filament"

    model_id = Column(Integer, ForeignKey("model.model_id"), primary_key=True)
    filament_id = Column(Integer, ForeignKey("filament.filament_id"), primary_key=True)

    model = relationship("Model", back_populates="filament_links")
    filament = relationship("Filament", back_populates="model_links")


# Order Header
class OrderHeader(Base):
    __tablename__ = "order_header"

    order_header_id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(Date, nullable=False)
    shipping_price = Column(DECIMAL(10, 2), nullable=False)
    extra_fee = Column(DECIMAL(10, 2))
    total_price = Column(DECIMAL(10, 2), nullable=False)
    order_tracking_number = Column(String(200), unique=True)

    order_status = Column(Enum("Cart", "Pending", "Printing", "Shipped", "Completed", "Cancelled"), nullable=False)

    stripe_payment_id = Column(String(500))
    payment_date = Column(Date)
    payment_status = Column(Enum("Pending", "Succeeded", "Failed"))

    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="orders")
    details = relationship("OrderDetail", back_populates="order_header")


# Order Detail
class OrderDetail(Base):
    __tablename__ = "order_detail"

    order_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    order_quantity = Column(Integer)
    infill_percent = Column(DECIMAL(5, 2))
    scale = Column(Float)
    unit_price = Column(DECIMAL(10, 2))

    model_id = Column(Integer, ForeignKey("model.model_id"))
    order_header_id = Column(Integer, ForeignKey("order_header.order_header_id"))
    filament_id = Column(Integer, ForeignKey("filament.filament_id"))

    model = relationship("Model", back_populates="order_details")
    order_header = relationship("OrderHeader", back_populates="details")
    filament = relationship("Filament", back_populates="order_details")