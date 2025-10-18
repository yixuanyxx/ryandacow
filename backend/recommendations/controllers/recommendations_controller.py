from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

recommendations_bp = Blueprint("recommendations", __name__, url_prefix="/recommendations")

# Import service from services directory
from services.recommendations_service import RecommendationsService
service = RecommendationsService()

@recommendations_bp.route("/<int:user_id>", methods=["GET"])
def get_recommendations(user_id):
    """Get AI-powered recommendations for user dashboard"""
    try:
        result = service.get_user_recommendations(user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@recommendations_bp.route("/courses/<int:user_id>", methods=["GET"])
def get_course_recommendations(user_id):
    """Get personalized course recommendations"""
    try:
        result = service.get_course_recommendations(user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@recommendations_bp.route("/mentors/<int:user_id>", methods=["GET"])
def get_mentor_recommendations(user_id):
    """Get mentor recommendations"""
    try:
        result = service.get_mentor_recommendations(user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500
