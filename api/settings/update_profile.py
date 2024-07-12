from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from models import Users
from helpers.auth_helper import check_username_exists, regex_validation
import bcrypt
from extensions import db

update_profile_bp = Blueprint("update_profile", __name__)

def update_profile_route():
    @update_profile_bp.post("/update-profile")
    @jwt_required()
    def update_profile():
        claims = get_jwt()
        id = claims.get("id")
        json_data = request.get_json()
        try:
            username = json_data.get("username")
            new_password = json_data.get("new_password")
            old_password = json_data.get("old_password")
        except Exception as e:
            return jsonify({
                "error": "Invalid Inputs",
                "message": str(e)
            })
        
        try:
            update_validation = regex_validation(username=username,  password=new_password)
            if update_validation:
                return update_validation, 400
            
            is_username_exists = check_username_exists(username)
            if is_username_exists:
                return jsonify({
                    "message": f"{username} nomli foydalanuvchi mavjud, boshqa nom tanlang"
                })
                
            user = Users.query.filter_by(user_id = id).first()
            if bcrypt.checkpw(
                old_password.encode('utf-8'),
                bytes(Users.get_password(user))
            ):
                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                Users.update_data(self=user, username=username, password=hashed_new_password)
                db.session.commit()
                return jsonify({
                    "message": "Profil muvaffaqiyatli  yangilandi"
                })
            else:
                return jsonify({"message": f"{old_password} paroli sizning parololingiz bilan mos kelmadi, qaytadan urunb ko'ring."}), 400
            
        except Exception as e:
            return jsonify({
                    "error": "Error while fetching!",
                    "message": str(e)
                }), 400