from flask import Blueprint, request, jsonify
from helpers.products_helper import stats_graph_dict
from helpers.decorators import token_required

stats_graph_bp = Blueprint("stats_graph", __name__)

def stats_graph_route():
    @stats_graph_bp.get("/stats-graph")
    @token_required
    def stats_graph(jwt_data):
        req_args = request.args
        
        id = jwt_data["id"]
        date_str = req_args.get("date")
        
        sixMonthStats = stats_graph_dict(date_str=date_str, id=id)
        
        return jsonify({
            "sixMonthStats": sixMonthStats
        })
