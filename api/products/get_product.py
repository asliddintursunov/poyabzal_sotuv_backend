from flask import Blueprint, jsonify, request
from models import Products
from datetime import datetime, timedelta
from helpers.products_helper import products_dict
from helpers.decorators import token_required

get_product_bp = Blueprint("get_product", __name__)

def get_product_route():
    @get_product_bp.get("/get-products")
    @token_required
    def get_products(jwt_data):
        try:
            id = jwt_data["id"]
            args = request.args
            date = args.get("date")   

            frontend_date = datetime.strptime(date, '%m/%d/%Y')
            
            curr_products_result = Products.query.filter(Products.product_sold_time >= frontend_date,Products.product_sold_time < frontend_date + timedelta(days=1), Products.seller_id == id).all()
            
            old_products_result = Products.query.filter(Products.old_product_sold_time >= frontend_date,Products.old_product_sold_time < frontend_date + timedelta(days=1), Products.seller_id == id).all()


            curr_products = products_dict(curr_products_result, product_type="curr")
            old_products = products_dict(old_products_result, product_type="old")
            
            return jsonify({
                "date": date,
                'curr_products': curr_products,
                "old_products": old_products
            })
        except Exception as e:
            print(e)
            return jsonify({
                "error": str(e),
                "message": "Ma'lumotlarni olishda xatolik, keyinroq urunib ko'ring"
            }), 400
