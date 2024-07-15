from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from models import Products
from helpers.products_helper import stats_graph_dict

stats_graph_bp = Blueprint("stats_graph", __name__)

def stats_graph_route():
    @stats_graph_bp.get("/stats-graph")
    @jwt_required()
    def stats_graph():
        req_args = request.args
        claims = get_jwt()
        
        id = claims.get("id")
        date_str = req_args.get("date")
        
        sixMonthStats = stats_graph_dict(date_str=date_str, id=id)
        
        return jsonify({
            "sixMonthStats": sixMonthStats
        })
