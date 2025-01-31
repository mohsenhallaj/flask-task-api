from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import Config

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    """ Factory function to create the Flask app """
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    jwt.init_app(app)

    # ✅ Add a home route (fix for 404 error)
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Tasks API!"})

    # Import blueprints
    from app.auth import auth_bp
    from app.routes import task_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(task_bp, url_prefix='/tasks')

    return app
