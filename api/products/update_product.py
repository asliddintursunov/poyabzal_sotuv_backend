from flask import Blueprint, request, jsonify
from models import Products
from extensions import db
from helpers.decorators import token_required

update_product_bp = Blueprint("update_product", __name__)

def update_product_route():
    @update_product_bp.patch("/update-product")
    @token_required
    def update_product(jwt_data):
        json_data = request.get_json()
        user_id = jwt_data["id"]
        product_id = json_data.get("product_id")
        
        new_product_name = json_data.get("product_name")
        new_product_color = json_data.get("product_color")
        new_pruduct_size = int(json_data.get("pruduct_size"))
        new_product_sold_price = int(json_data.get("product_sold_price"))
        new_product_get_price = int(json_data.get("product_get_price"))
        
        try:
            old_product_data = Products.query.filter_by(product_id = product_id, seller_id = user_id).first()
            if old_product_data:
                Products.update_product(
                    self=old_product_data, 
                    updated_name=new_product_name, 
                    updated_size=new_pruduct_size, 
                    updated_color=new_product_color, 
                    updated_sold_price=new_product_sold_price, 
                    updated_get_price=new_product_get_price
                )
                db.session.commit()
                return jsonify({
                    "message": "Poyabzal muvaffaqiyatli almashtirildi va yangilandi"
                }), 200
            else:
                return jsonify({
                    "message": "Poyabzalni yangilashda xatolik"
                }), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "error": str(e),
                "message": "Poyabzalni yangilashda xatolik"
            }), 400