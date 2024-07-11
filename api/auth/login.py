from flask import Blueprint, request, jsonify
from models import Users
import bcrypt
from flask_jwt_extended import create_access_token
from helpers.auth_helper import regex_validation, check_username_exists

login_bp = Blueprint("login_bp", __name__)

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
                            additional_claims = {
                                "id": Users.get_userid(user)
                            }
                            access_token = create_access_token(identity=Users.get_username(user), additional_claims=additional_claims)
                            # access_token = "This is an access token"
                            return jsonify({
                                        "message": "Successfully logged in",
                                        "username": Users.get_username(user),
                                        "tokens": {
                                            "access_token": access_token,
                                        }
                                    }), 200
                        else:
                            return f"Incorrect username or password!", 400
                    else:
                        return f"Incorrect username or password!", 400 
                except Exception as e:
                    return jsonify({
                            'error': str(e),
                            'message': 'Error occured during login'
                        }), 400
            except:
                return "Invalid Credentials", 400