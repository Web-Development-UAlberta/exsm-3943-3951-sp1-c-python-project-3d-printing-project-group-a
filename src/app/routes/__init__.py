from flask import Flask
from ..config import Config
from ..extensions import jwt, bcrypt, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/api/users")

    from app.routes.checkout import checkout_bp
    app.register_blueprint(checkout_bp, url_prefix="/api/checkout")
    
    

    return app