import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from ..database import get_db
from ..models import OrderHeader
from ..services.stripe_service import (
    create_payment_intent,
    construct_webhook_event
)

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
                # try real Stripe
                intent = create_payment_intent(
                    amount_dollars=float(cart.total_price),
                    currency="cad",
                    metadata={
                        "user_id": str(user_id),
                        "cart_id": str(cart.order_header_id)
                    }
                )
                payment_intent_id = intent.id
                client_secret     = intent.client_secret

            except Exception:
                # fallback dummy for testing without real Stripe
                payment_intent_id = f"pi_test_dummy_{cart.order_header_id}"
                client_secret     = f"pi_test_dummy_{cart.order_header_id}_secret"

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
    data    = request.get_json()

    if not data.get("payment_intent_id"):
        return jsonify({"error": "payment_intent_id is required"}), 400

    try:
        with get_db() as db:
            cart = db.query(OrderHeader).filter_by(user_id=user_id, order_status="Cart").first()

            if not cart:
                return jsonify({"error": "No active cart found"}), 400
            if not cart.details:
                return jsonify({"error": "Cart is empty"}), 400

            # always approve — payment assumed successful
            cart.order_status = "Pending"
            cart.stripe_payment_id = data["payment_intent_id"]
            cart.payment_status = "Succeeded"
            cart.payment_date = date.today()

            return jsonify({
                "message": "Order placed successfully",
                "order_id": cart.order_header_id,
                "total": float(cart.total_price),
                "status": cart.order_status
            }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@checkout_bp.route("/webhook", methods=["POST"])
def stripe_webhook():

    payload = request.get_data()
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = construct_webhook_event(payload, sig_header, webhook_secret)
    except Exception as e:
        return jsonify({"error": f"Webhook verification failed: {str(e)}"}), 400

    if event["type"] == "payment_intent.succeeded":
        intent  = event["data"]["object"]
        cart_id = intent.get("metadata", {}).get("cart_id")
        if cart_id:
            try:
                with get_db() as db:
                    order = db.query(OrderHeader).filter_by(
                        order_header_id=int(cart_id)
                    ).first()
                    if order and order.order_status == "Cart":
                        order.order_status = "Pending"
                        order.payment_status = "Succeeded"
                        order.stripe_payment_id = intent["id"]
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