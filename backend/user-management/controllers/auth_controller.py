from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Import service from services directory
from services.auth_service import AuthService
service = AuthService()

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login user - MVP version with demo accounts"""
    try:
        data = request.get_json(silent=True) or {}
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"Code": 400, "Message": "Email and password are required"}), 400
        
        result = service.login_user(email, password)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@auth_bp.route("/profile", methods=["GET"])
@require_auth
def get_profile():
    """Get user profile for dashboard"""
    try:
        result = service.get_user_profile(request.user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500