from models import Users
import re

def check_username_exists(username):
    username = Users.query.filter(Users.user_name == username).first()
    return username

def regex_validation(username, password):
    REGEX_PATTERN = {
        "username": r"^[a-zA-Z0-9@_!]{8,20}$",
        "password": r"^[a-zA-Z0-9]{8,20}$",
    }
    
    if not re.match(REGEX_PATTERN["username"], username):
            return "Invalid username"
    elif not re.match(REGEX_PATTERN["password"], password):
        return "Invalid password"
    
    return None