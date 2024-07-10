import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db

from api.auth.login import login_bp, login_route

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
    
    
    
    
    # APIs
    app.register_blueprint(login_bp)
    
    return app
    