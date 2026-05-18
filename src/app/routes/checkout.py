import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from ..database import get_db
from ..models import OrderHeader
from ..services.stripe_service import create_payment_intent
from ..services.order_service import assign_printer_to_order

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.route("/create-intent", methods=["POST"])
@jwt_required()
def create_intent():
    user_id = int(get_jwt_identity())
    try:
        with get_db() as db:
            cart = db.query(OrderHeader).filter_by(
                user_id=user_id,
                order_status="Cart"
            ).first()
            if not cart:
                return jsonify({"error": "Cart is empty"}), 400
            if not cart.details:
                return jsonify({"error": "Cart has no items"}), 400
            try:
                intent = create_payment_intent(
                    amount_dollars=float(cart.total_price),
                    currency="cad",
                    metadata={
                        "user_id": str(user_id),
                        "cart_id": str(cart.order_header_id)
                    }
                )
                payment_intent_id = intent.id
                client_secret = intent.client_secret
            except Exception:
                payment_intent_id = f"pi_test_dummy_{cart.order_header_id}"
                client_secret = f"pi_test_dummy_{cart.order_header_id}_secret"
            return jsonify({
                "client_secret": client_secret,
                "payment_intent_id": payment_intent_id,
                "amount": float(cart.total_price),
                "cart_id": cart.order_header_id
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@checkout_bp.route("/confirm", methods=["POST"])
@jwt_required()
def confirm_order():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data.get("payment_intent_id"):
        return jsonify({"error": "payment_intent_id is required"}), 400

    print_time_hours = data.get("print_time_hours")

    try:
        with get_db() as db:
            cart = db.query(OrderHeader).filter_by(user_id=user_id, order_status="Cart").first()
            if not cart:
                return jsonify({"error": "No active cart found"}), 400
            if not cart.details:
                return jsonify({"error": "Cart is empty"}), 400

            cart.order_status = "Pending"
            cart.stripe_payment_id = data["payment_intent_id"]
            cart.payment_status = "Succeeded"
            cart.payment_date = date.today()

            printer_info = None
            if print_time_hours:
                try:
                    printer_info = assign_printer_to_order(db, cart, print_time_hours)
                except Exception:
                    printer_info = None

            response = {
                "message": "Order placed successfully",
                "order_id": cart.order_header_id,
                "total": float(cart.total_price),
                "status": cart.order_status
            }

            if printer_info:
                response["assigned_printer"] = printer_info["printer_name"]
                response["printer_id"] = printer_info["printer_id"]
                response["estimated_hours"] = printer_info["estimated_hours"]
                response["print_time_with_buffer"] = printer_info["print_time_with_buffer"]

            return jsonify(response), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@checkout_bp.route("/webhook", methods=["POST"])
def stripe_webhook():
    event = request.get_json()
    if not event or "type" not in event or "data" not in event:
        return jsonify({"error": "Invalid webhook payload"}), 400

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        cart_id = intent.get("metadata", {}).get("cart_id")
        if cart_id:
            try:
                with get_db() as db:
                    order = db.query(OrderHeader).filter_by(order_header_id=int(cart_id)).first()
                    if order and order.order_status == "Cart":
                        order.order_status = "Pending"
                        order.payment_status = "Succeeded"
                        order.stripe_payment_id = intent.get("id", "mock_stripe_id")
                        order.payment_date = date.today()
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    elif event["type"] == "payment_intent.payment_failed":
        intent = event["data"]["object"]
        cart_id = intent.get("metadata", {}).get("cart_id")
        if cart_id:
            try:
                with get_db() as db:
                    order = db.query(OrderHeader).filter_by(order_header_id=int(cart_id)).first()
                    if order:
                        order.payment_status = "Failed"
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ok"}), 200