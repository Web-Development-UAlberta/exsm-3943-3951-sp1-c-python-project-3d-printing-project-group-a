from flask import Blueprint, request, jsonify
from ..database import get_db
from ..models import Filament

# Blueprint
filament_bp = Blueprint("filaments", __name__)


# Returns all filaments
@filament_bp.route("/", methods=["GET"])
def get_filaments():
    try:
        material = request.args.get("material")
        manufacturer = request.args.get("manufacturer")
        in_stock = request.args.get("in_stock")

        with get_db() as db:
            query = db.query(Filament)

            # Filter by material name
            if material:
                query = query.filter(Filament.material_name == material)

            # Filter by manufacturer
            if manufacturer:
                query = query.filter(Filament.manufacturer == manufacturer)

            # Filter by stock availability
            if in_stock is not None:
                if in_stock.lower() == "true":
                    query = query.filter(Filament.quantity_in_stock > 0)
                elif in_stock.lower() == "false":
                    query = query.filter(Filament.quantity_in_stock <= 0)

            filaments = query.all()

            result = []
            for filament in filaments:
                result.append({
                    "filament_id": filament.filament_id,
                    "material_name": filament.material_name,
                    "color_hex": filament.color_hex,
                    "quantity_in_stock": filament.quantity_in_stock,
                    "manufacturer": filament.manufacturer,
                    "more_wear_and_tear": (
                        float(filament.more_wear_and_tear)
                        if filament.more_wear_and_tear is not None
                        else None
                    ),
                    "finish_filament": filament.finish_filament,
                    "filament_price": float(filament.filament_price)
                })

            return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Returns one filament by ID
@filament_bp.route("/<int:filament_id>", methods=["GET"])
def get_filament(filament_id):
    try:
        with get_db() as db:
            filament = (
                db.query(Filament)
                .filter(Filament.filament_id == filament_id)
                .first()
            )

            if not filament:
                return jsonify({"error": "Filament not found"}), 404

            return jsonify({
                "filament_id": filament.filament_id,
                "material_name": filament.material_name,
                "color_hex": filament.color_hex,
                "quantity_in_stock": filament.quantity_in_stock,
                "manufacturer": filament.manufacturer,
                "more_wear_and_tear": (
                    float(filament.more_wear_and_tear)
                    if filament.more_wear_and_tear is not None
                    else None
                ),
                "finish_filament": filament.finish_filament,
                "filament_price": float(filament.filament_price)
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Create a new filament
@filament_bp.route("/", methods=["POST"])
def create_filament():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = [
        "material_name",
        "quantity_in_stock",
        "filament_price"
    ]

    for field in required_fields:
        if data.get(field) is None:
            return jsonify({"error": f"{field} is required"}), 400

    try:
        with get_db() as db:
            filament = Filament(
                material_name=data["material_name"],
                color_hex=data.get("color_hex"),
                quantity_in_stock=data["quantity_in_stock"],
                manufacturer=data.get("manufacturer"),
                more_wear_and_tear=data.get("more_wear_and_tear"),
                finish_filament=data.get("finish_filament"),
                filament_price=data["filament_price"]
            )

            db.add(filament)
            db.commit()
            db.refresh(filament)

            return jsonify({
                "message": "Filament created successfully",
                "filament_id": filament.filament_id
            }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update an existing filament
@filament_bp.route("/<int:filament_id>", methods=["PUT"])
def update_filament(filament_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        with get_db() as db:
            filament = (
                db.query(Filament)
                .filter(Filament.filament_id == filament_id)
                .first()
            )

            if not filament:
                return jsonify({"error": "Filament not found"}), 404

            # Update only provided fields
            if "material_name" in data:
                filament.material_name = data["material_name"]

            if "color_hex" in data:
                filament.color_hex = data["color_hex"]

            if "quantity_in_stock" in data:
                filament.quantity_in_stock = data["quantity_in_stock"]

            if "manufacturer" in data:
                filament.manufacturer = data["manufacturer"]

            if "more_wear_and_tear" in data:
                filament.more_wear_and_tear = data["more_wear_and_tear"]

            if "finish_filament" in data:
                filament.finish_filament = data["finish_filament"]

            if "filament_price" in data:
                filament.filament_price = data["filament_price"]

            db.commit()

            return jsonify({
                "message": "Filament updated successfully"
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Delete a filament
@filament_bp.route("/<int:filament_id>", methods=["DELETE"])
def delete_filament(filament_id):
    try:
        with get_db() as db:
            filament = (
                db.query(Filament)
                .filter(Filament.filament_id == filament_id)
                .first()
            )

            if not filament:
                return jsonify({"error": "Filament not found"}), 404

            db.delete(filament)
            db.commit()

            return jsonify({
                "message": "Filament deleted successfully"
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500