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

            petg_black = Filament(
                material_name="PETG",
                color_hex="#000000",
                quantity_in_stock=510,
                manufacturer="Prusament",
                filament_price=32.00,
                finish_filament="Satin"
            )

            petg_white = Filament(
                material_name="PETG",
                color_hex="#FFFFFF",
                quantity_in_stock=510,
                manufacturer="Prusament",
                filament_price=32.00,
                finish_filament="Satin"
            )

            petg_blue = Filament(
                material_name="PETG",
                color_hex="#0000FF",
                quantity_in_stock=510,
                manufacturer="Prusament",
                filament_price=32.00,
                finish_filament="Glossy"
            )

            petg_red = Filament(
                material_name="PETG",
                color_hex="#FF0000",
                quantity_in_stock=510,
                manufacturer="Prusament",
                filament_price=32.00,
                finish_filament="Silk"
            )

            abs_black = Filament(
                material_name="ABS",
                color_hex="#000000",
                quantity_in_stock=670,
                manufacturer="eSUN",
                filament_price=28.00,
                finish_filament="Silk"
            )

            abs_white = Filament(
                material_name="ABS",
                color_hex="#FFFFFF",
                quantity_in_stock=670,
                manufacturer="eSUN",
                filament_price=28.00,
                finish_filament="Silk"
            )

            abs_grey = Filament(
                material_name="ABS",
                color_hex="#808080",
                quantity_in_stock=670,
                manufacturer="eSUN",
                filament_price=28.00,
                finish_filament="Satin"
            )

            tpu_black = Filament(
                material_name="TPU",
                color_hex="#000000",
                quantity_in_stock=90,
                manufacturer="NinjaTek",
                filament_price=38.00,
                finish_filament="Glossy"
            )

            tpu_white = Filament(
                material_name="TPU",
                color_hex="#FFFFFF",
                quantity_in_stock=90,
                manufacturer="NinjaTek",
                filament_price=38.00,
                finish_filament="Glossy"
            )

            tpu_red = Filament(
                material_name="TPU",
                color_hex="#FF0000",
                quantity_in_stock=90,
                manufacturer="NinjaTek",
                filament_price=38.00,
                finish_filament="Flexible"
            )

            db.add_all([pla_black, pla_white, petg_black, petg_white, petg_blue, petg_red, abs_black, abs_white, abs_grey, tpu_black, tpu_white, tpu_red])
            db.flush()

            prusa_type1 = PrinterType(
                printer_name="Prusa MK4",
                max_size=500.0
            )

            prusa_type2 = PrinterType(
                printer_name="Prusa MK4",
                max_size=500.0
            )

            prusa_type3 = PrinterType(
                printer_name="Prusa MK4",
                max_size=500.0
            )

            db.add_all([prusa_type1, prusa_type2, prusa_type3])
            db.flush()

            printer1 = Printer(
                filament_id=pla_black.filament_id,
                printer_type_id=prusa_type1.printer_type_id
            )

            printer2 = Printer(
                filament_id=pla_white.filament_id,
                printer_type_id=prusa_type1.printer_type_id
            )

            printer3 = Printer(
                filament_id=petg_black.filament_id,
                printer_type_id=prusa_type1.printer_type_id
            )

            printer4 = Printer(
                filament_id=petg_white.filament_id,
                printer_type_id=prusa_type1.printer_type_id
            )

            printer5 = Printer(
                filament_id=petg_blue.filament_id,
                printer_type_id=prusa_type1.printer_type_id
            )

            printer6 = Printer(
                filament_id=petg_red.filament_id,
                printer_type_id=prusa_type1.printer_type_id
            )

            printer7 = Printer(
                filament_id=abs_black.filament_id,
                printer_type_id=prusa_type2.printer_type_id
            )

            printer8 = Printer(
                filament_id=abs_white.filament_id,
                printer_type_id=prusa_type2.printer_type_id
            )

            printer9 = Printer(
                filament_id=abs_grey.filament_id,
                printer_type_id=prusa_type2.printer_type_id
            )

            printer10 = Printer(
                filament_id=tpu_black.filament_id,
                printer_type_id=prusa_type3.printer_type_id
            )

            printer11 = Printer(
                filament_id=tpu_white.filament_id,
                printer_type_id=prusa_type3.printer_type_id
            )

            printer12 = Printer(
                filament_id=tpu_red.filament_id,
                printer_type_id=prusa_type3.printer_type_id
            )

            db.add_all([printer1, printer2, printer3, printer4, printer5, printer6, printer7, printer8, printer9, printer10, printer11, printer12])
            db.flush()

            tags = {
                "gaming": Tag(tag_name="Gaming"),
                "utilities": Tag(tag_name="Utilities"),
                "collectibles": Tag(tag_name="Collectibles"),
                "decor": Tag(tag_name="Decorations"),
                "edu": Tag(tag_name="Education"),
                "props": Tag(tag_name="Props"),
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
                printer_id=printer1.printer_id,
                model_file="src/app/model_files/desk_vase.3tl",
		        model_image="src/app/model_images/desk_vase.png"
            )

            tree_ornament = Model(
                model_name="Christmas Ornament",
                model_length=120,
                model_width=80,
                model_height=95,
                model_description="Tree ornament.",
                print_time_hours=8.0,
                printer_id=printer1.printer_id,
                model_file="src/app/model_files/christmas_ornament.3tl",
		        model_image="src/app/model_images/christmas_ornament.png"
            )

            d20_dice = Model(
                model_name="D20 Dice",
                model_length=50,
                model_width=50,
                model_height=50,
                model_description="Classic dice.",
                print_time_hours=3.5,
                printer_id=printer1.printer_id,
                model_file="src/app/model_files/d20_dice.3tl",
		        model_image="src/app/model_images/d20_dice.png"
            )

            chess_queen = Model(
                model_name="Chess Queen",
                model_length=50,
                model_width=50,
                model_height=50,
                model_description="Chess piece.",
                print_time_hours=3.5,
                printer_id=printer1.printer_id,
                model_file="src/app/model_files/chess_queen.3tl",
		        model_image="src/app/model_images/chess_queen.png"
            )

            iron_man = Model(
                model_name="Iron Man Bust",
                model_length=150,
                model_width=120,
                model_height=200,
                model_description="Bust model.",
                print_time_hours=18.0,
                printer_id=printer1.printer_id,
                model_file="src/app/model_files/iron_man.3tl",
		        model_image="src/app/model_images/iron_man.png"
            )

            bat_man = Model(
                model_name="Batman Man Bust",
                model_length=150,
                model_width=120,
                model_height=200,
                model_description="Bust model.",
                print_time_hours=18.0,
                printer_id=printer1.printer_id,
                model_file="src/app/model_files/bat_man.3tl",
		        model_image="src/app/model_images/bat_man.png"
            )

            cable_clip = Model(
                model_name="Cable Clip",
                model_length=30,
                model_width=20,
                model_height=15,
                model_description="Cable organizer.",
                print_time_hours=1.0,
                printer_id=printer1.printer_id,
                model_file="src/app/model_files/cable_clip.3tl",
		        model_image="src/app/model_images/cable_clip.png"
            )

            tool_hammer = Model(
                model_name="Hammer",
                model_length=30,
                model_width=20,
                model_height=15,
                model_description="Impact tool.",
                print_time_hours=1.0,
                printer_id=printer1.printer_id,
                model_file="src/app/model_files/tool_hammer.3tl",
		        model_image="src/app/model_images/tool_hammer.png"
            )

            helmet_prop = Model(
                model_name="Helmet",
                model_length=300,
                model_width=250,
                model_height=280,
                model_description="Helmet prop.",
                print_time_hours=24.0,
                printer_id=printer2.printer_id,
                model_file="src/app/model_files/prop_helmet.3tl",
		        model_image="src/app/model_images/prop_helmet.png"
            )

            pylon_prop = Model(
                model_name="Traffic Cone",
                model_length=300,
                model_width=250,
                model_height=280,
                model_description="Traffic cone prop.",
                print_time_hours=24.0,
                printer_id=printer2.printer_id,
                model_file="src/app/model_files/prop_traffic_cone.3tl",
		        model_image="src/app/model_images/prop_traffic_cone.png"
            )

            dna_model = Model(
                model_name="DNA Model",
                model_length=80,
                model_width=80,
                model_height=200,
                model_description="DNA helix.",
                print_time_hours=6.0,
                printer_id=printer3.printer_id,
                model_file="src/app/model_files/dna_model.3tl",
		        model_image="src/app/model_images/dna_model.png"
            )

            globe_earth = Model(
                model_name="Earth Model",
                model_length=80,
                model_width=80,
                model_height=200,
                model_description="World globe.",
                print_time_hours=6.0,
                printer_id=printer3.printer_id,
                model_file="src/app/model_files/earth_model.3tl",
		        model_image="src/app/model_images/earth_model.png"
            )

            custom_upload = Model(
                model_name="Custom Product",
                model_length=100,
                model_width=100,
                model_height=100,
                model_description="Custom Upload",
                print_time_hours=3.0,
                printer_id=printer2.printer_id,
                model_file="custom.3tl",
		        model_image="src/app/model_images/custom_print.png"
            )

            db.add_all([desk_vase, tree_ornament, d20_dice, chess_queen, iron_man, bat_man, cable_clip, tool_hammer, helmet_prop, pylon_prop, dna_model, globe_earth, custom_upload])
            db.flush()


            db.add_all([
                ModelTag(model_id=desk_vase.model_id, tag_id=tags["decor"].tag_id),
                ModelTag(model_id=tree_ornament.model_id, tag_id=tags["decor"].tag_id),
                ModelTag(model_id=d20_dice.model_id, tag_id=tags["gaming"].tag_id),
                ModelTag(model_id=chess_queen.model_id, tag_id=tags["gaming"].tag_id),
                ModelTag(model_id=iron_man.model_id, tag_id=tags["collectibles"].tag_id),
                ModelTag(model_id=bat_man.model_id, tag_id=tags["collectibles"].tag_id),
                ModelTag(model_id=cable_clip.model_id, tag_id=tags["utilities"].tag_id),
                ModelTag(model_id=tool_hammer.model_id, tag_id=tags["utilities"].tag_id),
                ModelTag(model_id=helmet_prop.model_id, tag_id=tags["props"].tag_id),
                ModelTag(model_id=pylon_prop.model_id, tag_id=tags["props"].tag_id),
                ModelTag(model_id=dna_model.model_id, tag_id=tags["edu"].tag_id),
                ModelTag(model_id=globe_earth.model_id, tag_id=tags["edu"].tag_id),
            ])


            db.add_all([
                ModelFilament(model_id=desk_vase.model_id, filament_id=pla_black.filament_id),
                ModelFilament(model_id=desk_vase.model_id, filament_id=pla_white.filament_id),
                ModelFilament(model_id=desk_vase.model_id, filament_id=petg_black.filament_id),
                ModelFilament(model_id=desk_vase.model_id, filament_id=petg_white.filament_id),
                ModelFilament(model_id=desk_vase.model_id, filament_id=petg_blue.filament_id),
                ModelFilament(model_id=desk_vase.model_id, filament_id=petg_red.filament_id),

                ModelFilament(model_id=tree_ornament.model_id, filament_id=pla_black.filament_id),
                ModelFilament(model_id=tree_ornament.model_id, filament_id=pla_white.filament_id),
                ModelFilament(model_id=tree_ornament.model_id, filament_id=petg_blue.filament_id),
                ModelFilament(model_id=tree_ornament.model_id, filament_id=petg_red.filament_id),

                ModelFilament(model_id=d20_dice.model_id, filament_id=pla_black.filament_id),
                ModelFilament(model_id=d20_dice.model_id, filament_id=pla_white.filament_id),
                ModelFilament(model_id=d20_dice.model_id, filament_id=petg_black.filament_id),
                ModelFilament(model_id=d20_dice.model_id, filament_id=petg_white.filament_id),
                ModelFilament(model_id=d20_dice.model_id, filament_id=petg_blue.filament_id),
                ModelFilament(model_id=d20_dice.model_id, filament_id=petg_red.filament_id),

                ModelFilament(model_id=chess_queen.model_id, filament_id=pla_black.filament_id),
                ModelFilament(model_id=chess_queen.model_id, filament_id=pla_white.filament_id),
                ModelFilament(model_id=chess_queen.model_id, filament_id=petg_blue.filament_id),
                ModelFilament(model_id=chess_queen.model_id, filament_id=petg_red.filament_id),

                ModelFilament(model_id=iron_man.model_id, filament_id=pla_black.filament_id),
                ModelFilament(model_id=iron_man.model_id, filament_id=pla_white.filament_id),
                ModelFilament(model_id=iron_man.model_id, filament_id=petg_black.filament_id),
                ModelFilament(model_id=iron_man.model_id, filament_id=petg_white.filament_id),
                ModelFilament(model_id=iron_man.model_id, filament_id=petg_blue.filament_id),
                ModelFilament(model_id=iron_man.model_id, filament_id=petg_red.filament_id),

                ModelFilament(model_id=bat_man.model_id, filament_id=pla_black.filament_id),
                ModelFilament(model_id=bat_man.model_id, filament_id=pla_white.filament_id),
                ModelFilament(model_id=bat_man.model_id, filament_id=petg_black.filament_id),
                ModelFilament(model_id=bat_man.model_id, filament_id=petg_white.filament_id),

                ModelFilament(model_id=cable_clip.model_id, filament_id=pla_black.filament_id),
                ModelFilament(model_id=cable_clip.model_id, filament_id=pla_white.filament_id),
                ModelFilament(model_id=cable_clip.model_id, filament_id=petg_black.filament_id),
                ModelFilament(model_id=cable_clip.model_id, filament_id=petg_white.filament_id),
                ModelFilament(model_id=cable_clip.model_id, filament_id=petg_blue.filament_id),
                ModelFilament(model_id=cable_clip.model_id, filament_id=petg_red.filament_id),

                ModelFilament(model_id=tool_hammer.model_id, filament_id=pla_black.filament_id),
                ModelFilament(model_id=tool_hammer.model_id, filament_id=pla_white.filament_id),
                ModelFilament(model_id=tool_hammer.model_id, filament_id=petg_black.filament_id),
                ModelFilament(model_id=tool_hammer.model_id, filament_id=petg_white.filament_id),

                ModelFilament(model_id=helmet_prop.model_id, filament_id=abs_black.filament_id),
                ModelFilament(model_id=helmet_prop.model_id, filament_id=abs_white.filament_id),
                ModelFilament(model_id=helmet_prop.model_id, filament_id=abs_grey.filament_id),

                ModelFilament(model_id=pylon_prop.model_id, filament_id=abs_black.filament_id),
                ModelFilament(model_id=pylon_prop.model_id, filament_id=abs_white.filament_id),
                ModelFilament(model_id=pylon_prop.model_id, filament_id=abs_grey.filament_id),

                ModelFilament(model_id=dna_model.model_id, filament_id=tpu_black.filament_id),
                ModelFilament(model_id=dna_model.model_id, filament_id=tpu_white.filament_id),
                ModelFilament(model_id=dna_model.model_id, filament_id=tpu_red.filament_id),

                ModelFilament(model_id=globe_earth.model_id, filament_id=tpu_black.filament_id),
                ModelFilament(model_id=globe_earth.model_id, filament_id=tpu_white.filament_id),
                ModelFilament(model_id=globe_earth.model_id, filament_id=tpu_red.filament_id),

                ModelFilament(model_id=custom_upload.model_id, filament_id=abs_black.filament_id),
                ModelFilament(model_id=custom_upload.model_id, filament_id=abs_white.filament_id),
                ModelFilament(model_id=custom_upload.model_id, filament_id=abs_grey.filament_id),
            ])

            db.commit()
            print("Seed data inserted successfully!")

        except Exception as e:
            db.rollback()
            print(f"Seed failed: {e}")
            raise


if __name__ == "__main__":
    seed()