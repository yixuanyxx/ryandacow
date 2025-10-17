from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

user_bp = Blueprint("users", __name__, url_prefix="/users")

# Import service from services directory
from services.user_service import UserService
service = UserService()

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get user by ID"""
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
        db = service.db
        users = db.table("users").select(`
            *,
            employment_info!inner(department)
        `).eq("employment_info.department", department).execute()
        
        return jsonify({
            "Code": 200,
            "Message": "Success",
            "data": users.data or []
        })
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500