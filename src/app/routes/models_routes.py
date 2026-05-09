from flask import Blueprint, request, jsonify
from ..database import get_db
from ..models import Model, Filament, Tag, ModelTag
from ..services.pricing import calculate_quote

models_bp = Blueprint("models", __name__)


@models_bp.route("/", methods=["GET"])
def get_models():
    tag_id = request.args.get("tag_id")
    material = request.args.get("material")
    sort = request.args.get("sort")  

    db = get_db()
    try:
        query = db.query(Model)

        
        if tag_id:
            query = query.join(ModelTag).filter(ModelTag.tag_id == tag_id)

        models = query.all()

        result = []
        for m in models:
            # get tags for this model
            tags = [
                {"tag_id": link.tag.tag_id, "tag_name": link.tag.tag_name}
                for link in m.tag_links
            ]

            # get filaments for this model
            filaments = [
                {
                    "filament_id": link.filament.filament_id,
                    "material_name": link.filament.material_name,
                    "color_hex": link.filament.color_hex,
                    "filament_price": float(link.filament.filament_price)
                }
                for link in m.filament_links
            ]

            result.append({
                "model_id": m.model_id,
                "model_name": m.model_name,
                "model_description": m.model_description,
                "model_length": m.model_length,
                "model_width": m.model_width,
                "model_height": m.model_height,
                "tags": tags,
                "filaments": filaments
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# GET /api/models/<id> 
@models_bp.route("/<int:model_id>", methods=["GET"])
def get_model(model_id):
    db = get_db()
    try:
        model = db.query(Model).filter_by(model_id=model_id).first()
        if not model:
            return jsonify({"error": "Model not found"}), 404

        tags = [
            {"tag_id": link.tag.tag_id, "tag_name": link.tag.tag_name}
            for link in model.tag_links
        ]

        filaments = [
            {
                "filament_id": link.filament.filament_id,
                "material_name": link.filament.material_name,
                "color_hex": link.filament.color_hex,
                "filament_price": float(link.filament.filament_price),
                "in_stock": link.filament.quantity_in_stock > 0
            }
            for link in model.filament_links
        ]

        return jsonify({
            "model_id": model.model_id,
            "model_name": model.model_name,
            "model_description": model.model_description,
            "model_length": model.model_length,
            "model_width": model.model_width,
            "model_height": model.model_height,
            "tags": tags,
            "filaments": filaments
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# POST /api/models/quote
@models_bp.route("/quote", methods=["POST"])
def get_quote():
    data = request.get_json()

    required = ["model_id", "filament_id", "scale", "infill_percent", "color_count"]
    for field in required:
        if data.get(field) is None:
            return jsonify({"error": f"{field} is required"}), 400

    if not (1 <= data["scale"] <= 200):
        return jsonify({"error": "Scale must be between 1 and 200"}), 400

    if not (1 <= data["infill_percent"] <= 100):
        return jsonify({"error": "Infill must be between 1 and 100"}), 400

    if data["color_count"] < 1:
        return jsonify({"error": "color_count must be at least 1"}), 400

    db = get_db()
    try:
        model    = db.query(Model).filter_by(model_id=data["model_id"]).first()
        filament = db.query(Filament).filter_by(filament_id=data["filament_id"]).first()

        if not model:
            return jsonify({"error": "Model not found"}), 404
        if not filament:
            return jsonify({"error": "Filament not found"}), 404

        if not model.model_length or not model.model_width or not model.model_height:
            return jsonify({"error": "Model is missing dimension data"}), 400

        if not model.print_time_hours:
            return jsonify({"error": "Model is missing print time data"}), 400

        # 500mm validation
        MAX_DIMENSION_MM = 500
        scaled_length = model.model_length * (data["scale"] / 100)
        scaled_width  = model.model_width  * (data["scale"] / 100)
        scaled_height = model.model_height * (data["scale"] / 100)

        if any(d > MAX_DIMENSION_MM for d in [scaled_length, scaled_width, scaled_height]):
            return jsonify({"error": "Scaled dimensions exceed maximum of 500mm per side"}), 400

        quote = calculate_quote(
            length = model.model_length,
            width = model.model_width,
            height = model.model_height,
            scale = data["scale"],
            infill_percent = data["infill_percent"],
            filament_price = float(filament.filament_price),
            color_count = data["color_count"],
            print_time_hours = float(model.print_time_hours),
        )

        return jsonify(quote), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()