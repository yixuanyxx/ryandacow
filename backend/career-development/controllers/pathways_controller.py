from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

pathways_bp = Blueprint("pathways", __name__, url_prefix="/pathways")

# Import service from services directory
from services.career_service import CareerService
service = CareerService()

@pathways_bp.route("/", methods=["GET"])
def get_all_pathways():
    """Get all career pathways"""
    try:
        result = service.get_all_pathways()
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@pathways_bp.route("/recommendations/<int:user_id>", methods=["GET"])
def get_pathway_recommendations(user_id):
    """Get career pathway recommendations"""
    try:
        result = service.get_pathway_recommendations(user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500
