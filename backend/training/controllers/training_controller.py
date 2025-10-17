from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

training_bp = Blueprint("training", __name__, url_prefix="/training")

# Import service from services directory
from services.training_service import TrainingService
service = TrainingService()

@training_bp.route("/courses", methods=["GET"])
def get_courses():
    """Get available courses"""
    try:
        result = service.get_courses()
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@training_bp.route("/enroll", methods=["POST"])
@require_auth
def enroll_course():
    """Enroll in a course"""
    try:
        data = request.get_json(silent=True) or {}
        result = service.enroll_course(request.user_id, data)
        status_code = result.pop("Code", 201)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500
