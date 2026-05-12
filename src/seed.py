import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import get_db
from app.models import (
    Filament, PrinterType, Printer, Tag,
    Model, ModelFilament, ModelTag
)


def seed():
    with get_db() as db:
        try:

            def clear_db(db):
                # child tables FIRST
                db.query(ModelFilament).delete()
                db.query(ModelTag).delete()
                db.query(Model).delete()

                # IMPORTANT: if order_detail exists
                db.query("DELETE FROM order_detail")

                db.query(Printer).delete()
                db.query(PrinterType).delete()
                db.query(Filament).delete()
                db.query(Tag).delete()

                db.commit()

            pla_black = Filament("PLA", "#000000", 820, "Hatchbox", 25.00, "Matte")
            pla_white = Filament("PLA", "#FFFFFF", 140, "Hatchbox", 25.00, "Matte")
            petg_blue = Filament("PETG", "#0000FF", 510, "Prusament", 32.00, "Glossy")
            abs_grey  = Filament("ABS", "#808080", 670, "eSUN", 28.00, "Matte")
            tpu_red   = Filament("TPU", "#FF0000", 90, "NinjaTek", 38.00, "Flexible")

            db.add_all([pla_black, pla_white, petg_blue, abs_grey, tpu_red])
            db.flush()

            prusa_type = PrinterType("Prusa MK4", 500.0)
            db.add(prusa_type)
            db.flush()

            printer1 = Printer(prusa_type.printer_type_id, pla_black.filament_id)
            printer2 = Printer(prusa_type.printer_type_id, petg_blue.filament_id)
            printer3 = Printer(prusa_type.printer_type_id, abs_grey.filament_id)

            db.add_all([printer1, printer2, printer3])
            db.flush()


            tags = {
                "decor": Tag("Decorations"),
                "gaming": Tag("Gaming"),
                "collectibles": Tag("Collectibles"),
                "utilities": Tag("Utilities"),
                "props": Tag("Props"),
                "edu": Tag("Education"),
            }

            db.add_all(tags.values())
            db.flush()

            desk_vase = Model("Desk Vase", 120, 80, 95, "A sleek desk vase.", 8.0, printer1.printer_id)
            d20_dice  = Model("D20 Dice", 50, 50, 50, "Classic dice.", 3.5, printer1.printer_id)
            iron_man  = Model("Iron Man Bust", 150, 120, 200, "Bust model.", 18.0, printer2.printer_id)
            cable_clip = Model("Cable Clip", 30, 20, 15, "Cable organizer.", 1.0, printer1.printer_id)
            helmet_prop = Model("Helmet Prop", 300, 250, 280, "Helmet prop.", 24.0, printer3.printer_id)
            dna_model = Model("DNA Model", 80, 80, 200, "DNA helix.", 6.0, printer2.printer_id)

            db.add_all([desk_vase, d20_dice, iron_man, cable_clip, helmet_prop, dna_model])
            db.flush()

            db.add_all([
                ModelTag(desk_vase.model_id, tags["decor"].tag_id),
                ModelTag(d20_dice.model_id, tags["gaming"].tag_id),
                ModelTag(iron_man.model_id, tags["collectibles"].tag_id),
                ModelTag(cable_clip.model_id, tags["utilities"].tag_id),
                ModelTag(helmet_prop.model_id, tags["props"].tag_id),
                ModelTag(dna_model.model_id, tags["edu"].tag_id),
            ])

            db.add_all([
                ModelFilament(desk_vase.model_id, pla_black.filament_id),
                ModelFilament(desk_vase.model_id, pla_white.filament_id),

                ModelFilament(d20_dice.model_id, pla_black.filament_id),
                ModelFilament(d20_dice.model_id, petg_blue.filament_id),

                ModelFilament(iron_man.model_id, abs_grey.filament_id),
                ModelFilament(iron_man.model_id, pla_black.filament_id),

                ModelFilament(cable_clip.model_id, pla_black.filament_id),
                ModelFilament(cable_clip.model_id, pla_white.filament_id),

                ModelFilament(helmet_prop.model_id, abs_grey.filament_id),
                ModelFilament(helmet_prop.model_id, tpu_red.filament_id),

                ModelFilament(dna_model.model_id, pla_white.filament_id),
                ModelFilament(dna_model.model_id, petg_blue.filament_id),
            ])

            db.commit()
            print("Seed data inserted successfully!")

        except Exception as e:
            db.rollback()
            print(f"Seed failed: {e}")
            raise


if __name__ == "__main__":
    seed()