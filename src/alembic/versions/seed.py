from alembic import op 
import sqlalchemy as sa
from models import User, Filament, PrinterType, Printer, Tag, Model, ModelFilament, OrderHeader, OrderDetail

revision = '1234567890'
down_revision = '0cd4f77e0e19'
branch_labels = None
depends_on = None

def upgrade():
    # Users
    op.execute("""
    INSERT INTO Users(username, full_name, phone_number, city, street_address, province, postal_code, is_admin)
    VALUES ('admin', 'Bo Cen', '000-111-2222', 'Edmonton', '123 Main St', 'AB', 'T6G 2G5', TRUE);
    """)

    # Filament
    op.execute("""
    INSERT INTO Filament(material_name, color_hex, quantity_in_stock,
    manufacturer, more_wear_and_tear, finish_filament, filament_price)
    VALUES ('PLA', '#FFFFFF', 100, 'm3D', 10.00, 'Satin', 18.00);
    """)

    # Printer Type
    op.execute("""
    INSERT INTO Printer_Type(printer_name, max_size)
    VALUES ('Prusa MK4', 500.00);
    """)

    # Printer
    op.execute("""
    INSERT INTO Printer(printer_type_id, filament_id)
    VALUES (1, 1);
    """)

    # Tag
    op.execute("""
    INSERT INTO Tag(tag_name)
    VALUES ('Gaming');
    """)

    # Model
    op.execute("""
    INSERT INTO Model(model_name, model_length, model_width, model_height,
    model_description, tag_id, printer_id)
    VALUES ('Iron Man', 10, 10, 10, 'Iron Man Model', 1, 1);
    """)


def downgrade():
    op.execute("DELETE FROM Model WHERE model_name = 'Iron Man';")
    op.execute("DELETE FROM Tag WHERE tag_name = 'Gaming';")
    op.execute("DELETE FROM Printer WHERE printer_id = 1;")
    op.execute("DELETE FROM Printer_Type WHERE printer_name = 'Prusa MK4';")
    op.execute("DELETE FROM Filament WHERE material_name = 'PLA';")
    op.execute("DELETE FROM Users WHERE username = 'admin';")