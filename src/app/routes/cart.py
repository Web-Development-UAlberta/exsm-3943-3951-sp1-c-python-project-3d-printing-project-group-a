from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..database import get_db
from ..models import OrderHeader, OrderDetail, Model, Filament
from ..services.order_service import (
    add_item_to_cart,
    remove_item_from_cart,
    clear_cart
)

cart_bp = Blueprint("cart", __name__)


def format_cart(cart):
    return {
        "order_header_id": cart.order_header_id,
        "shipping_price": float(cart.shipping_price),
        "total_price": float(cart.total_price),
        "items": [
            {
                "order_detail_id": d.order_detail_id,
                "model_id": d.model_id,
                "model_name": d.model.model_name if d.model else None,
                "filament_id": d.filament_id,
                "material_name": d.filament.material_name if d.filament else None,
                "color_hex": d.filament.color_hex if d.filament else None,
                "order_quantity": d.order_quantity,
                "scale": d.scale,
                "infill_percent": float(d.infill_percent) if d.infill_percent else None,
                "unit_price": float(d.unit_price) if d.unit_price else None,
            }
            for d in cart.details
        ]
    }


@cart_bp.route("/", methods=["GET"])
@jwt_required()
def get_cart():
    user_id = int(get_jwt_identity())
    try:
        with get_db() as db:
            cart = db.query(OrderHeader).filter_by(
                user_id=user_id,
                order_status="Cart"
            ).first()
            if not cart:
                return jsonify({
                    "order_header_id": None,
                    "items": [],
                    "shipping_price": 10.00,
                    "total_price": 10.00
                }), 200
            return jsonify(format_cart(cart)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cart_bp.route("/", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    required = ["model_id", "filament_id", "scale", "infill_percent", "color_count"]
    for field in required:
        if data.get(field) is None:
            return jsonify({"error": f"{field} is required"}), 400
    if not (1 <= data["scale"] <= 200):
        return jsonify({"error": "Scale must be between 1 and 200"}), 400
    if not (1 <= data["infill_percent"] <= 100):
        return jsonify({"error": "Infill must be between 1 and 100"}), 400
    quantity = data.get("quantity", 1)
    if quantity < 1:
        return jsonify({"error": "Quantity must be at least 1"}), 400
    try:
        with get_db() as db:
            cart = add_item_to_cart(
                db = db,
                user_id = user_id,
                model_id = data["model_id"],
                filament_id = data["filament_id"],
                quantity = quantity,
                scale = data["scale"],
                infill_percent = data["infill_percent"],
                color_count = data["color_count"]
            )
            return jsonify(format_cart(cart)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cart_bp.route("/<int:order_detail_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(order_detail_id):
    user_id = int(get_jwt_identity())
    try:
        with get_db() as db:
            cart = remove_item_from_cart(db, user_id, order_detail_id)
            return jsonify(format_cart(cart)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cart_bp.route("/", methods=["DELETE"])
@jwt_required()
def clear_cart_route():
    user_id = int(get_jwt_identity())
    try:
        with get_db() as db:
            clear_cart(db, user_id)
            return jsonify({"message": "Cart cleared"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500