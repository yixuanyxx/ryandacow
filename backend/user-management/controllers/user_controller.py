from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

user_bp = Blueprint("users", __name__, url_prefix="/users")

# Import service from services directory
from services.user_service import UserService
service = UserService()

@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get user by ID (using employee ID as string)"""
    try:
        result = service.get_user_profile(user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@user_bp.route("/department/<department>", methods=["GET"])
def get_users_by_department(department):
    """Get users by department"""
    try:
        result = service.get_users_by_department(department)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500