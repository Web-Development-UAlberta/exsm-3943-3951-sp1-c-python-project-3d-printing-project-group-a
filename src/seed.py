import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import get_db
from app.models import (
    Filament, PrinterType, Printer, Tag,
    Model, ModelFilament, ModelTag, OrderDetail
)


def seed():
    with get_db() as db:
        try:

            db.query(OrderDetail).delete()
            db.query(ModelFilament).delete()
            db.query(ModelTag).delete()
            db.query(Model).delete()
            db.query(Printer).delete()
            db.query(PrinterType).delete()
            db.query(Filament).delete()
            db.query(Tag).delete()

            db.commit()

            pla_black = Filament(
                material_name="PLA",
                color_hex="#000000",
                quantity_in_stock=820,
                manufacturer="Hatchbox",
                filament_price=25.00,
                finish_filament="Matte"
            )

            pla_white = Filament(
                material_name="PLA",
                color_hex="#FFFFFF",
                quantity_in_stock=140,
                manufacturer="Hatchbox",
                filament_price=25.00,
                finish_filament="Matte"
            )

            petg_blue = Filament(
                material_name="PETG",
                color_hex="#0000FF",
                quantity_in_stock=510,
                manufacturer="Prusament",
                filament_price=32.00,
                finish_filament="Glossy"
            )

            abs_grey = Filament(
                material_name="ABS",
                color_hex="#808080",
                quantity_in_stock=670,
                manufacturer="eSUN",
                filament_price=28.00,
                finish_filament="Matte"
            )

            tpu_red = Filament(
                material_name="TPU",
                color_hex="#FF0000",
                quantity_in_stock=90,
                manufacturer="NinjaTek",
                filament_price=38.00,
                finish_filament="Flexible"
            )

            db.add_all([pla_black, pla_white, petg_blue, abs_grey, tpu_red])
            db.flush()

            prusa_type = PrinterType(
                printer_name="Prusa MK4",
                max_size=500.0
            )

            db.add(prusa_type)
            db.flush()


            printer1 = Printer(
                printer_type_id=prusa_type.printer_type_id,
                filament_id=pla_black.filament_id
            )

            printer2 = Printer(
                printer_type_id=prusa_type.printer_type_id,
                filament_id=petg_blue.filament_id
            )

            printer3 = Printer(
                printer_type_id=prusa_type.printer_type_id,
                filament_id=abs_grey.filament_id
            )

            db.add_all([printer1, printer2, printer3])
            db.flush()

            tags = {
                "decor": Tag(tag_name="Decorations"),
                "gaming": Tag(tag_name="Gaming"),
                "collectibles": Tag(tag_name="Collectibles"),
                "utilities": Tag(tag_name="Utilities"),
                "props": Tag(tag_name="Props"),
                "edu": Tag(tag_name="Education"),
            }

            db.add_all(tags.values())
            db.flush()


            desk_vase = Model(
                model_name="Desk Vase",
                model_length=120,
                model_width=80,
                model_height=95,
                model_description="A sleek desk vase.",
                print_time_hours=8.0,
                printer_id=printer1.printer_id
            )

            d20_dice = Model(
                model_name="D20 Dice",
                model_length=50,
                model_width=50,
                model_height=50,
                model_description="Classic dice.",
                print_time_hours=3.5,
                printer_id=printer1.printer_id
            )

            iron_man = Model(
                model_name="Iron Man Bust",
                model_length=150,
                model_width=120,
                model_height=200,
                model_description="Bust model.",
                print_time_hours=18.0,
                printer_id=printer2.printer_id
            )

            cable_clip = Model(
                model_name="Cable Clip",
                model_length=30,
                model_width=20,
                model_height=15,
                model_description="Cable organizer.",
                print_time_hours=1.0,
                printer_id=printer1.printer_id
            )

            helmet_prop = Model(
                model_name="Helmet Prop",
                model_length=300,
                model_width=250,
                model_height=280,
                model_description="Helmet prop.",
                print_time_hours=24.0,
                printer_id=printer3.printer_id
            )

            dna_model = Model(
                model_name="DNA Model",
                model_length=80,
                model_width=80,
                model_height=200,
                model_description="DNA helix.",
                print_time_hours=6.0,
                printer_id=printer2.printer_id
            )

            db.add_all([desk_vase, d20_dice, iron_man, cable_clip, helmet_prop, dna_model])
            db.flush()


            db.add_all([
                ModelTag(model_id=desk_vase.model_id, tag_id=tags["decor"].tag_id),
                ModelTag(model_id=d20_dice.model_id, tag_id=tags["gaming"].tag_id),
                ModelTag(model_id=iron_man.model_id, tag_id=tags["collectibles"].tag_id),
                ModelTag(model_id=cable_clip.model_id, tag_id=tags["utilities"].tag_id),
                ModelTag(model_id=helmet_prop.model_id, tag_id=tags["props"].tag_id),
                ModelTag(model_id=dna_model.model_id, tag_id=tags["edu"].tag_id),
            ])


            db.add_all([
                ModelFilament(model_id=desk_vase.model_id, filament_id=pla_black.filament_id),
                ModelFilament(model_id=desk_vase.model_id, filament_id=pla_white.filament_id),

                ModelFilament(model_id=d20_dice.model_id, filament_id=pla_black.filament_id),
                ModelFilament(model_id=d20_dice.model_id, filament_id=petg_blue.filament_id),

                ModelFilament(model_id=iron_man.model_id, filament_id=abs_grey.filament_id),
                ModelFilament(model_id=iron_man.model_id, filament_id=pla_black.filament_id),

                ModelFilament(model_id=cable_clip.model_id, filament_id=pla_black.filament_id),
                ModelFilament(model_id=cable_clip.model_id, filament_id=pla_white.filament_id),

                ModelFilament(model_id=helmet_prop.model_id, filament_id=abs_grey.filament_id),
                ModelFilament(model_id=helmet_prop.model_id, filament_id=tpu_red.filament_id),

                ModelFilament(model_id=dna_model.model_id, filament_id=pla_white.filament_id),
                ModelFilament(model_id=dna_model.model_id, filament_id=petg_blue.filament_id),
            ])

            db.commit()
            print("Seed data inserted successfully!")

        except Exception as e:
            db.rollback()
            print(f"Seed failed: {e}")
            raise


if __name__ == "__main__":
    seed()