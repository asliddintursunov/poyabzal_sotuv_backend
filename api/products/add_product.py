from flask import Blueprint, jsonify, request
from models import Products
from extensions import db
from helpers.decorators import token_required

add_product_bp = Blueprint("add_product", __name__)

def add_product_route():
    @add_product_bp.post("/add-product")
    @token_required
    def add_product(jwt_data):
        data = request.get_json()
        
        name = data.get("name")
        size = int(data.get("size"))
        color = data.get("color")
        sold_price = int(data.get("sold_price"))
        get_price = int(data.get("get_price"))
        seller_id = jwt_data["id"]
        
        try:
            new_shoe = Products(name=name, size=size, color=color, sold_price=sold_price, get_price=get_price, seller_id=seller_id)

            
            db.session.add(new_shoe)
            db.session.commit()
            print(f"print: {repr(new_shoe)}")
            return jsonify({"message": f"Yangi poyabzal {color} {size} {name} {sold_price} ming so'mga sotildi."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "error": str(e),
                "message": "Yangi poyabzal qo'shishda xatolik, keyinroq urunib ko'ring"
            }), 400