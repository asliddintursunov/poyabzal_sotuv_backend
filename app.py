import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db #, jwt

from api.auth.login import login_bp, login_route
from api.auth.register import register_bp, register_route
from api.products.add_product import add_product_bp, add_product_route
from api.products.get_product import get_product_bp, get_product_route
from api.products.update_product import update_product_bp, update_product_route
from api.products.delete_product import delete_product_bp, delete_product_route
from api.settings.update_profile import update_profile_bp, update_profile_route
from api.settings.get_data import get_data_bp, get_data_route
from api.stats.monthly_stats import montly_stats_bp, montly_stats_route
from api.stats.stats_graph import stats_graph_bp, stats_graph_route

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    db.init_app(app)
    
    # Routes
    login_route()
    register_route()
    add_product_route()
    get_product_route()
    update_product_route()
    delete_product_route()
    update_profile_route()
    get_data_route()
    montly_stats_route()
    stats_graph_route()
    
    # APIs
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(add_product_bp)
    app.register_blueprint(get_product_bp)
    app.register_blueprint(update_product_bp)
    app.register_blueprint(delete_product_bp)
    app.register_blueprint(update_profile_bp)
    app.register_blueprint(get_data_bp)
    app.register_blueprint(montly_stats_bp)
    app.register_blueprint(stats_graph_bp)
    
    return app
    