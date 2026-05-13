from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from ..database import get_db
from ..models import User


def require_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())
        with get_db() as db:
            user = db.query(User).filter_by(user_id=user_id).first()
            if not user or not user.is_admin:
                return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper