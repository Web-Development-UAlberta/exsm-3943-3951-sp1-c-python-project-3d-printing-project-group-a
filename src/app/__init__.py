from flask import Flask
from .config import Config
from .extensions import jwt, bcrypt, cors


def create_app():
    app = Flask(__name__) 
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/api/users")

    from .routes.models_routes import models_bp
    app.register_blueprint(models_bp, url_prefix="/api/models")

    from .routes.cart import cart_bp
    app.register_blueprint(cart_bp, url_prefix="/api/cart")

    from .routes.orders import orders_bp
    app.register_blueprint(orders_bp, url_prefix="/api/orders")

    from .routes.filaments import filament_bp
    app.register_blueprint(filament_bp, url_prefix="/api/filaments")

    from .routes.checkout import checkout_bp
    app.register_blueprint(checkout_bp, url_prefix="/api/checkout")

    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app