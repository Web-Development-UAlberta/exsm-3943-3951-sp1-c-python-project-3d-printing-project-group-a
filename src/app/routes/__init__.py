from flask import Flask
from ..config import Config
from ..extensions import jwt, bcrypt, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/api/users")

    from app.routes.checkout import checkout_bp
    app.register_blueprint(checkout_bp, url_prefix="/api/checkout")

    return app