from flask import Blueprint, jsonify, request
from models import Users
from helpers.auth_helper import check_username_exists, regex_validation
import bcrypt
from extensions import db
import re
from helpers.decorators import token_required

update_profile_bp = Blueprint("update_profile", __name__)

def update_profile_route():
    @update_profile_bp.patch("/update-profile")
    @token_required
    def update_profile(jwt_data):
        id = jwt_data["id"]
        json_data = request.get_json()
        username = json_data.get("username", None)
        new_password = json_data.get("new_password", None)
        old_password = json_data.get("old_password", None)
        
        try:
            if username:
                update_validation = regex_validation(username=username,  password=new_password)
                if update_validation:
                    return update_validation, 400
                
                is_username_exists = check_username_exists(username)
                if is_username_exists:
                    return jsonify({
                        "message": f"{username} nomli foydalanuvchi mavjud, boshqa nom tanlang"
                    }), 400
            else:
                password_regex = r"^[a-zA-Z0-9]{8,20}$"
                if not re.match(password_regex, new_password):
                    return "Invalid password"
                
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
                }), 200
            else:
                return jsonify({"message": f"{old_password} paroli sizning parololingiz bilan mos kelmadi, qaytadan urunb ko'ring."}), 400
            
        except Exception as e:
            return jsonify({
                    "error": str(e),
                    "message": "Error: Xisobni yangilashda xatolik"
                }), 400