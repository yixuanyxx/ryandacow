from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

mentorship_bp = Blueprint("mentorship", __name__, url_prefix="/mentorship")

# Import service from services directory
from services.mentorship_service import MentorshipService
service = MentorshipService()

@mentorship_bp.route("/mentors/find", methods=["GET"])
@require_auth
def find_mentors():
    """Find potential mentors"""
    try:
        result = service.find_mentors(request.user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@mentorship_bp.route("/requests", methods=["POST"])
@require_auth
def send_request():
    """Send mentorship request"""
    try:
        data = request.get_json(silent=True) or {}
        result = service.send_mentorship_request(request.user_id, data)
        status_code = result.pop("Code", 201)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500
