from flask import Flask
from src.app.config import Config
from src.app.extensions import jwt, bcrypt, cors


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    from src.app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from src.app.routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/api/users")

    from src.app.routes.models_routes import models_bp
    app.register_blueprint(models_bp, url_prefix="/api/models")

    return app