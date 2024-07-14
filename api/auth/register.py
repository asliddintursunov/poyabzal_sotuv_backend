from flask import Blueprint
from extensions import db
from models import Users
import bcrypt
from flask import Blueprint, request, jsonify
from helpers.auth_helper import check_username_exists, regex_validation

register_bp = Blueprint("register", __name__)

def register_route():
    @register_bp.route("/auth/register", methods=["POST"])
    def register():
        if request.method == 'POST':
            try:
                data = request.get_json()
                print(f"data => {data}")
                username = data.get("username").strip()
                password = data.get("password").strip()
            except:
                return "Wrong input", 400
            
            register_validation = regex_validation(username=username,  password=password)
            if register_validation:
                return register_validation, 400
        
            try:
                existing_username = check_username_exists(username=username)
                if existing_username:
                    return jsonify({'success': False, 'message': f'Foydalanuvchi {username} allaqachon mavjud.'}), 400
                        
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                new_user = Users(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                return jsonify({
                    "success": True,
                    "message": "Muvafaqiyatli ro'yxatdan o'tildi"
                })
            except Exception as e:
                db.session.rollback()
                return jsonify({
                        "success": False,
                        'message': "Registratsiya vaqtida serverda xatolik, qaytadan urunib ko'ring",
                        'error': str(e)
                    }), 400