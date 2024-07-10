from flask import Blueprint, request, jsonify

login_bp = Blueprint("login", __name__)

def login_route():
    @login_bp.route("/auth/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            return jsonify({"message": "THIS IS A LOGIN POST API"})
        return jsonify({"message": "THIS IS A LOGIN GET API"})