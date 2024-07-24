from flask import Blueprint, request, jsonify
from helpers.decorators import token_required
from extensions import db
from models import Products

delete_product_bp = Blueprint("delete_product", __name__)

def delete_product_route():
    @delete_product_bp.delete("/delete-product/<int:product_id>")
    @token_required
    def delete_product(jwt_data, product_id):
        user_id = jwt_data["id"]
        try:
            product = Products.query.filter_by(product_id = product_id, seller_id = user_id).first()
            if product:
                db.session.delete(product)
                db.session.commit()
                return jsonify({
                    "message": "Poyabzal muvaffaqiyatli o'chirildi"
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