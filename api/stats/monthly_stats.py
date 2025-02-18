from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models import Products
from helpers.products_helper import monthly_stats_dict
from helpers.decorators import token_required

montly_stats_bp = Blueprint("montly_stats", __name__)

def montly_stats_route():
    @montly_stats_bp.get("/monthly-stats")
    @token_required
    def monthly_stats(jwt_data):
        try:
            req_args = request.args
            
            id = jwt_data["id"]
            date_str = req_args.get("date")
            print(f"date_str => {date_str}")
            date = datetime.strptime(date_str, "%Y-%m")
            
            start_date = date.replace(day=1)
            next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
            end_date = next_month - timedelta(days=1)
            
            sold_products = Products.query.filter(
                Products.product_sold_time >= start_date, 
                Products.product_sold_time <= end_date, 
                Products.seller_id == id
            ).all()
            stats = monthly_stats_dict(sold_products)
            
            return jsonify({
                "start_date": start_date,
                "end_date": end_date,   
                "stats": stats
            })
        except Exception as e:
            return jsonify({
                "error": str(e),
                "message": "Oylik grafik ma'lumotlanini olishda xatolik."
            })
        
        