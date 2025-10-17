from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

skills_bp = Blueprint("skills", __name__, url_prefix="/skills")

# Import service from services directory
from services.skills_service import SkillsService
service = SkillsService()

@skills_bp.route("/", methods=["GET"])
def get_all_skills():
    """Get all skills"""
    try:
        result = service.get_all_skills()
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@skills_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_skills(user_id):
    """Get user's skills"""
    try:
        result = service.get_user_skills(user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@skills_bp.route("/user", methods=["POST"])
@require_auth
def add_user_skill():
    """Add skill to user profile"""
    try:
        data = request.get_json(silent=True) or {}
        result = service.add_user_skill(request.user_id, data)
        status_code = result.pop("Code", 201)
        return jsonify(result), status_code
    except ValueError as e:
        return jsonify({"Code": 400, "Message": str(e)}), 400
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500