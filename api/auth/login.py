from flask import Blueprint, request, jsonify
from models import Users
import bcrypt
from helpers.auth_helper import regex_validation, check_username_exists

from helpers.decorators import create_token

login_bp = Blueprint("login", __name__)

def login_route():
    @login_bp.route("/auth/login", methods=["POST"])
    def login():
        if request.method == "POST":
            try:
                data = request.get_json()
                username = data.get("username").strip()
                password = data.get("password").strip()
                
                login_validation = regex_validation(username=username, password=password)
                if login_validation:
                    return login_validation
                
                try:
                    existing_username = check_username_exists(username=username)
                    if existing_username:
                        user = Users.query.filter_by(user_name = username).first()
                        
                        if bcrypt.checkpw(
                            password.encode('utf-8'), 
                            bytes(Users.get_password(user))
                        ):
                            access_token = create_token(
                                username=Users.get_username(user),
                                user_id=Users.get_userid(user)
                            )
                            return jsonify({
                                        "success": True,
                                        "message": "Muvafaqiyatli xisobga kirildi",
                                        "username": Users.get_username(user),
                                        "tokens": {
                                            "access_token": access_token,
                                        }
                                    }), 200
                        else:
                            return jsonify({
                                    "success": False,
                                    "message": "Foydalanuvchi nomi yokida paroli xato"
                                }), 400
                    else:
                        return jsonify({
                                    "success": False,
                                    "message": "Foydalanuvchi nomi yokida paroli xato"
                                }), 400
                except Exception as e:
                    return jsonify({
                        "success": False,
                        'message': "Xisobga kirishda serverda xatolik, qaytadan urunib ko'ring",
                        'error': str(e)
                    }), 400
            except:
                return jsonify({
                        "success": False,
                        'message': "Xisobga kirishda serverda xatolik, qaytadan urunib ko'ring",
                        'error': str(e)
                    }), 400