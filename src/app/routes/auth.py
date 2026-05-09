from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import bcrypt
from app.database import get_db
from app.models import User
from app.services.validation import validate_postal_code, validate_province, validate_phone

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    required = ["username", "password", "phone_number", "city", "street_address", "province"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400
        

    # validate phone
    ok, err = validate_phone(data["phone_number"])
    if not ok:
        return jsonify({"error": err}), 400

    # validate province
    ok, err = validate_province(data["province"])
    if not ok:
        return jsonify({"error": err}), 400

    # validate postal code if provided
    if data.get("postal_code"):
        ok, err = validate_postal_code(data["postal_code"])
        if not ok:
            return jsonify({"error": err}), 400

    db = get_db()
    try:
        existing = db.query(User).filter_by(username=data["username"]).first()
        if existing:
            return jsonify({"error": "Username already taken"}), 409

        hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

        user = User(
            username=data["username"],
            full_name=data.get("full_name"),
            email=data.get("email"),
            phone_number=data["phone_number"],
            city=data["city"],
            street_address=data["street_address"],
            province=data["province"],
            postal_code=data.get("postal_code"),
            password=hashed_pw
        )
        db.add(user)
        db.commit()       
        db.refresh(user)  #gets the new user_id back
    except Exception as e:
        db.rollback()     #undo if something goes wrong
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

    return jsonify({"message": "Account created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    db = get_db()
    try:
        user = db.query(User).filter_by(username=data["username"]).first()

        if not user or not bcrypt.check_password_hash(user.password, data["password"]):
            return jsonify({"error": "Invalid username or password"}), 401

        token = create_access_token(identity=str(user.user_id))
        user_id = user.user_id  # ← save before session closes
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

    return jsonify({"access_token": token, "user_id": user_id}), 200