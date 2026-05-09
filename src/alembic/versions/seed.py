from alembic import op

revision = '1234567890'
down_revision = '0cd4f77e0e19'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
    INSERT INTO users(username, full_name, phone_number, city, street_address, province, postal_code, is_admin)
    VALUES ('admin', 'Bo Cen', '000-111-2222', 'Edmonton', '123 Main St', 'AB', 'T6G 2G5', TRUE);
    """)

    op.execute("""
    INSERT INTO filament(material_name, color_hex, quantity_in_stock, manufacturer, more_wear_and_tear, finish_filament, filament_price)
    VALUES ('PLA', '#FFFFFF', 100, 'm3D', 10.00, 'Satin', 18.00);
    """)

    op.execute("""
    INSERT INTO printer_type(printer_name, max_size)
    VALUES ('Prusa MK4', 500.00);
    """)

    op.execute("""
    INSERT INTO printer(printer_type_id, filament_id)
    VALUES (1, 1);
    """)

    op.execute("""
    INSERT INTO tag(tag_name)
    VALUES ('Gaming');
    """)
    
    op.execute("""
    INSERT INTO model(model_name, model_length, model_width, model_height, model_description, tag_id, printer_id)
    VALUES ('Iron Man', 10, 10, 10, 'Iron Man Model', 1, 1);
    """)


def downgrade():
    op.execute("DELETE FROM model WHERE model_name = 'Iron Man';")
    op.execute("DELETE FROM tag WHERE tag_name = 'Gaming';")
    op.execute("DELETE FROM printer WHERE printer_id = 1;")
    op.execute("DELETE FROM printer_type WHERE printer_name = 'Prusa MK4';")
    op.execute("DELETE FROM filament WHERE material_name = 'PLA';")
    op.execute("DELETE FROM users WHERE username = 'admin';")