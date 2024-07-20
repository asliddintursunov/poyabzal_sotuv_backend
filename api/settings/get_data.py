from flask import Blueprint, jsonify
from models import Users
from helpers.decorators import token_required

get_data_bp = Blueprint("get_data", __name__)

def get_data_route():
    @get_data_bp.get("/get-data")
    @token_required
    def get_data(jwt_data):
        id = jwt_data["id"]
        
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