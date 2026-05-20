from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..database import get_db
from ..models import OrderHeader, OrderDetail

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/", methods=["GET"])
@jwt_required()
def get_my_orders():
    user_id = int(get_jwt_identity())
    try:
        with get_db() as db:
            orders = db.query(OrderHeader).filter(
                OrderHeader.user_id == user_id,
                OrderHeader.order_status != "Cart"
            ).all()
            result = []
            for o in orders:
                result.append({
                    "order_id": o.order_header_id,
                    "order_date": str(o.order_date),
                    "total_price": float(o.total_price),
                    "order_status": o.order_status,
                    "payment_status": o.payment_status,
                    "tracking_number": o.order_tracking_number,
                    "items": [
                     {
                            "model": d.model.model_name,
                            "model_image": d.model.model_image if d.model else None,
                            "quantity": d.order_quantity,
                            "unit_price": float(d.unit_price),
                            "filament": d.filament.material_name
                        }
                        for d in o.details
                    ]
                })
            return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@orders_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    user_id = int(get_jwt_identity())
    try:
        with get_db() as db:
            order = db.query(OrderHeader).filter_by(
                order_header_id=order_id,
                user_id=user_id
            ).first()
            if not order:
                return jsonify({"error": "Order not found"}), 404
            if order.order_status == "Cart":
                return jsonify({"error": "Order not found"}), 404
            return jsonify({
                "order_id": order.order_header_id,
                "order_date": str(order.order_date),
                "total_price": float(order.total_price),
                "shipping_price": float(order.shipping_price),
                "order_status": order.order_status,
                "payment_status": order.payment_status,
                "tracking_number": order.order_tracking_number,
                "stripe_payment_id": order.stripe_payment_id,
                "items": [
             {
                        "model": d.model.model_name,
                        "model_image": d.model.model_image if d.model else None,
                        "quantity": d.order_quantity,
                        "infill": float(d.infill_percent),
                        "scale": float(d.scale),
                        "unit_price": float(d.unit_price),
                        "filament": d.filament.material_name
                    }
                    for d in order.details
                ]
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@orders_bp.route("/<int:order_id>/cancel", methods=["PUT"])
@jwt_required()
def cancel_order(order_id):
    user_id = int(get_jwt_identity())
    try:
        with get_db() as db:
            order = db.query(OrderHeader).filter_by(
                order_header_id=order_id,
                user_id=user_id
            ).first()
            if not order:
                return jsonify({"error": "Order not found"}), 404
            if order.order_status != "Pending":
                return jsonify({"error": "Only pending orders can be cancelled"}), 400
            order.order_status = "Cancelled"
            return jsonify({"message": "Order cancelled successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500