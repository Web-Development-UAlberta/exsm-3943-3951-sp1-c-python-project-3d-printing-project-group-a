from flask import Blueprint, request, jsonify, send_from_directory, redirect, url_for
from ..database import get_db
from ..models import Model, Filament, ModelTag, ModelFilament, FilamentPrinter
from ..services.pricing import calculate_quote
from werkzeug.utils import secure_filename
import os
import json

models_bp = Blueprint("models", __name__)


@models_bp.route("/", methods=["GET"])
def get_models():
    tag_id = request.args.get("tag_id", type=int)
    order = request.args.get("order")
    filament_id = request.args.get("filament_id", type=int)
    search = request.args.get("search")

    try:
        with get_db() as db:

            query = db.query(Model)

            # SAFE FILTERING (NO outer joins)
            if tag_id:
                query = query.join(ModelTag).filter(ModelTag.tag_id == tag_id).filter(Model.model_name.notlike('%custom product%'))
            if filament_id:
                query = query.join(ModelFilament).filter(ModelFilament.filament_id == filament_id).filter(Model.model_name.notlike('%custom product%'))
            if search:
                query = query.filter(Model.model_name.ilike(f"%{search}%")).filter(Model.model_name.notlike('%custom product%'))
            if order == "asc":
                query = query.order_by(Model.model_name.asc())
            elif order == "desc":
                query = query.order_by(Model.model_name.desc())

            models = query.filter(Model.model_name.notlike('%custom product%')).all()   # ❗ REMOVE distinct()

            result = []

            for m in models:

                tags = []
                for link in getattr(m, "tag_links", []):
                    if link.tag:
                        tags.append({
                            "tag_id": link.tag.tag_id,
                            "tag_name": link.tag.tag_name
                        })

                filaments = []
                for link in getattr(m, "filament_links", []):
                    if link.filament:
                        filaments.append({
                            "filament_id": link.filament.filament_id,
                            "material_name": link.filament.material_name,
                            "color_hex": link.filament.color_hex
                        })

                result.append({
                    "model_id": m.model_id,
                    "model_name": m.model_name,
                    "model_image": m.model_image,
                    "tags": tags,
                    "filaments": filaments
                })

            return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@models_bp.route("/upload", methods=["POST"])
def custom_upload():
    CUSTOM_UPLOAD = os.getenv('CUSTOM_UPLOAD', 'src/app/model_files/')
    MODEL_IMAGES = os.getenv('MODEL_IMAGES', 'src/app/model_images/')
    ALLOWED_EXTENSIONS = {'stl', '3mf'}

    def extension_check(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not extension_check(file.filename):
            return jsonify({"error": "File extension not supported", "filename": file.filename}), 400

        # save file
        filename  = secure_filename(file.filename)
        save_path = os.path.join(CUSTOM_UPLOAD, filename)
        os.makedirs(CUSTOM_UPLOAD, exist_ok=True)
        file.save(save_path)

        # read pre-configured values from form data or json
        model_length = float(request.form.get("model_length", 100))
        model_width = float(request.form.get("model_width", 100))
        model_height = float(request.form.get("model_height", 100))
        scale = float(request.form.get("scale", 100))
        infill_percent = float(request.form.get("infill_percent", 20))
        color_count = int(request.form.get("color_count", 1))
        filament_id = request.form.get("filament_id")
        print_time_hours = float(request.form.get("print_time_hours", 3))
        custom_image = f"{MODEL_IMAGES}custom_print.png"

        # create model row in database
        with get_db() as db:

            # find any available printer
            from ..models import Printer
            printer = db.query(Printer).first()
            printer_id = printer.printer_id if printer else None

            model = Model(
                model_name = f"Custom: {filename}",
                model_length = model_length,
                model_width = model_width,
                model_height = model_height,
                model_description = "Custom uploaded model",
                model_file = save_path,
                model_image = custom_image,
                print_time_hours = print_time_hours,
                printer_id = printer_id
            )
            db.add(model)
            db.flush()
            model_id = model.model_id

        return jsonify({
            "message": "File uploaded successfully",
            "model_id": model_id,
            "model_name": f"Custom: {filename}",
            "model_length": model_length,
            "model_width": model_width,
            "model_height": model_height,
            "scale": scale,
            "infill_percent": infill_percent,
            "color_count": color_count,
            "filament_id": filament_id,
            "print_time_hours": print_time_hours,
            "redirect_to": f"/product/{model_id}"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@models_bp.route("/quote", methods=["POST"])
def get_quote():
    data = request.get_json() or {}

    required = [
        "model_id",
        "filament_id",
        "scale",
        "infill_percent",
        "color_count"
    ]

    for field in required:
        if data.get(field) is None:
            return jsonify({"error": f"{field} is required"}), 400

    if not (1 <= data["scale"] <= 200):
        return jsonify({
            "error": "Scale must be between 1 and 200"
        }), 400

    if not (1 <= data["infill_percent"] <= 100):
        return jsonify({
            "error": "Infill must be between 1 and 100"
        }), 400

    if data["color_count"] < 1:
        return jsonify({
            "error": "color_count must be at least 1"
        }), 400

    try:
        with get_db() as db:
            model = db.query(Model).filter_by(
                model_id=data["model_id"]
            ).first()

            filament = db.query(Filament).filter_by(
                filament_id=data["filament_id"]
            ).first()

            if not model:
                return jsonify({"error": "Model not found"}), 404

            if not filament:
                return jsonify({"error": "Filament not found"}), 404

            if (
                model.model_length is None or
                model.model_width is None or
                model.model_height is None
            ):
                return jsonify({
                    "error": "Model is missing dimension data"
                }), 400

            if model.print_time_hours is None:
                return jsonify({
                    "error": "Model is missing print time data"
                }), 400

            # Check scaled dimensions
            scale_factor = data["scale"] / 100.0
            scaled_length = model.model_length * scale_factor
            scaled_width = model.model_width * scale_factor
            scaled_height = model.model_height * scale_factor

            MAX_DIMENSION_MM = 500

            if any(
                d > MAX_DIMENSION_MM
                for d in [scaled_length, scaled_width, scaled_height]
            ):
                return jsonify({
                    "error": "Scaled dimensions exceed maximum of 500mm per side"
                }), 400

            quote = calculate_quote(
                length=model.model_length,
                width=model.model_width,
                height=model.model_height,
                scale=data["scale"],
                infill_percent=data["infill_percent"],
                filament_price=float(filament.filament_price),
                color_count=data["color_count"],
                print_time_hours=float(model.print_time_hours),
            )

            return jsonify(quote), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@models_bp.route("/<int:model_id>", methods=["GET"])
def get_model(model_id):
    try:
        with get_db() as db:
            model = db.query(Model).filter_by(
                model_id=model_id
            ).first()

            if not model:
                return jsonify({"error": "Model not found"}), 404

            tags = []
            for link in model.tag_links:
                if link.tag is not None:
                    tags.append({
                        "tag_id": link.tag.tag_id,
                        "tag_name": link.tag.tag_name
                    })

            filaments = []
            for link in model.filament_links:
                if link.filament is not None:
                    filaments.append({
                        "filament_id": link.filament.filament_id,
                        "material_name": link.filament.material_name,
                        "color_hex": link.filament.color_hex,
                        "filament_price": float(
                            link.filament.filament_price
                        ),
                        "in_stock": (
                            link.filament.quantity_in_stock > 0
                        )
                    })

            return jsonify({
                "model_id": model.model_id,
                "model_name": model.model_name,
                "model_description": model.model_description,
                "model_length": model.model_length,
                "model_width": model.model_width,
                "model_height": model.model_height,
                "model_image": model.model_image,
                "print_time_hours": (
                    float(model.print_time_hours)
                    if model.print_time_hours is not None
                    else None
                ),
                "tags": tags,
                "filaments": filaments
            }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@models_bp.route("/images/<filename>")
def serve_image(filename):
    image_dir = os.path.join(os.path.dirname(__file__), "../model_images")
    return send_from_directory(image_dir, filename)