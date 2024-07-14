from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from models import Products
from datetime import datetime, timedelta
from helpers.products_helper import products_dict

get_product_bp = Blueprint("get_product", __name__)

def get_product_route():
    @get_product_bp.get("/get-products")
    @jwt_required()
    def get_products():
        try:
            claims = get_jwt()
            id = claims.get("id")
            args = request.args
            date = args.get("date")   

            frontend_date = datetime.strptime(date, '%m/%d/%Y')
            
            products_result = Products.query.filter(Products.product_sold_time >= frontend_date,Products.product_sold_time < frontend_date + timedelta(days=1), Products.seller_id == id).all()

            products = products_dict(products_result)
            
            return jsonify({
                "date": date,
                'products': products
            })
        except Exception as e:
            print(e)
            return jsonify({
                "error": str(e),
                "message": "Ma'lumotlarni olishda xatolik, keyinroq urunib ko'ring"
            }), 400
