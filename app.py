import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db, jwt
import redis
from datetime import timedelta
from jwt import DecodeError

from api.auth.login import login_bp, login_route
from api.auth.register import register_bp, register_route
from api.products.add_product import add_product_bp, add_product_route
from api.products.get_product import get_product_bp, get_product_route
from api.settings.update_profile import update_profile_bp, update_profile_route
from api.settings.get_data import get_data_bp, get_data_route
from api.stats.monthly_stats import montly_stats_bp, montly_stats_route
from api.stats.stats_graph import stats_graph_bp, stats_graph_route

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    CORS(app)
    ACCESS_EXPIRES = timedelta(weeks=52)
    jwt.init_app(app)
    jwt_redis_blocklist = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
    
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    db.init_app(app)
    
    # Routes
    login_route()
    register_route()
    add_product_route()
    get_product_route()
    update_profile_route()
    get_data_route()
    montly_stats_route()
    stats_graph_route()
    
    # APIs
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(add_product_bp)
    app.register_blueprint(get_product_bp)
    app.register_blueprint(update_profile_bp)
    app.register_blueprint(get_data_bp)
    app.register_blueprint(montly_stats_bp)
    app.register_blueprint(stats_graph_bp)
    
    # Callback function to check if a JWT exists in the redis blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has expired", "error": "token_expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Request doesn't include header and token", "error": "authorization_header"}), 401
        
    
    return app
    