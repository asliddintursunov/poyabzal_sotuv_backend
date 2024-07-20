import os
import jwt
import datetime
from dotenv import load_dotenv
from flask import request, jsonify

load_dotenv()
jwt_secret = os.getenv("JWT_SECRET_KEY")

def create_token(username, user_id, expiration_days=365):
    payload = {
        "username": username,
        "id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=expiration_days)
    }
    token = jwt.encode(payload, jwt_secret, algorithm='HS256')
    return token

# Token decoding function
def decode_token(token):
    try:
        # Ensure the token is a byte string
        if isinstance(token, str):
            token = token.encode('utf-8')
        decoded_payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
    except Exception as e:
        return str(e)

# Decorator to protect routes
def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = decode_token(token)
            if isinstance(data, str):
                raise jwt.InvalidTokenError(data)
        except Exception as e:
            return jsonify({'message': str(e)}), 401

        return f(data, *args, **kwargs)
    
    decorated.__name__ = f.__name__
    return decorated
