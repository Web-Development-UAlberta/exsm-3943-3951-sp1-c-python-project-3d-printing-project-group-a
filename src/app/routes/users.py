from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import bcrypt
from ..database import get_db
from ..models import User, OrderHeader

users_bp = Blueprint("users", __name__)

@users_bp.route("/me", methods=["GET"])
@jwt_required()

def get_profile():
    user_id = int(get_jwt_identity())

    try:
        with get_db() as db:
            user = db.query(User).filter_by(user_id=user_id).first()
            
            if not user:
                return jsonify({"error": "User not found"}), 404
            return jsonify({
                "user_id": user.user_id,
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "city": user.city,
                "street_address": user.street_address,
                "province": user.province,
                "postal_code": user.postal_code,
                "is_admin": user.is_admin
            }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@users_bp.route("/me", methods=["PUT"])
@jwt_required()

def update_profile():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    try:
        with get_db() as db:
            user = db.query(User).filter_by(user_id=user_id).first()
            if not user:
                return jsonify({"error": "User not found"}), 404
            if data.get("full_name") is not None: user.full_name = data["full_name"]
            if data.get("email") is not None: user.email = data["email"]
            if data.get("phone_number") is not None: user.phone_number = data["phone_number"]
            if data.get("city") is not None: user.city = data["city"]
            if data.get("street_address") is not None: user.street_address = data["street_address"]
            if data.get("province") is not None: user.province = data["province"]
            if data.get("postal_code") is not None: user.postal_code = data["postal_code"]

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Profile updated successfully"}), 200

@users_bp.route("/me/password", methods=["PUT"])
@jwt_required()

def change_password():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    required = ["current_password", "new_password"]

    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400
        
    if len(data["new_password"]) < 8:
        return jsonify({"error": "New password must be at least 8 characters"}), 400
    
    try:
        with get_db() as db:
            user = db.query(User).filter_by(user_id=user_id).first()

            if not user:
                return jsonify({"error": "User not found"}), 404
            
            if not bcrypt.check_password_hash(user.password, data["current_password"]):
                return jsonify({"error": "Current password is incorrect"}), 401
            
            user.password = bcrypt.generate_password_hash(data["new_password"]).decode("utf-8")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"message": "Password changed successfully"}), 200



@users_bp.route("/me", methods=["DELETE"])
@jwt_required()
def delete_account():
    user_id = int(get_jwt_identity())
    try:
        with get_db() as db:
            user = db.query(User).filter_by(user_id=user_id).first()
            if not user:
                return jsonify({"error": "User not found"}), 404
            orders = db.query(OrderHeader).filter_by(user_id=user_id).all()
            for order in orders:
                for detail in order.details:
                    db.delete(detail)
                db.delete(order)
            db.delete(user)
            return jsonify({"message": "Account deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500