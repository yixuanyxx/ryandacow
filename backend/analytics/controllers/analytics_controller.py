from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

# Import service from services directory
from services.analytics_service import AnalyticsService
service = AnalyticsService()

@analytics_bp.route("/dashboard/<int:user_id>", methods=["GET"])
def get_dashboard_data(user_id):
    """Get dashboard analytics data"""
    try:
        result = service.get_dashboard_data(user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@analytics_bp.route("/metrics/<int:user_id>", methods=["GET"])
def get_user_metrics(user_id):
    """Get user metrics"""
    try:
        result = service.get_user_metrics(user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500
