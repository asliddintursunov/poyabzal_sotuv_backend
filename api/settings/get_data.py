from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import Users

get_data_bp = Blueprint("get_data", __name__)

def get_data_route():
    @get_data_bp.get("/get-data")
    @jwt_required()
    def get_data():
        claims = get_jwt()
        id = claims.get("id")
        
        try:
            user = Users.query.filter_by(user_id = id).first()
            user_name = Users.get_username(user)
            
            return jsonify({
                "user_name": user_name
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e),
                "message": "Profil ma'lumotlarini olishda xatolik."
            }), 400