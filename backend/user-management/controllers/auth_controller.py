from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Import service from services directory
from services.user_service import UserService
service = UserService()

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    try:
        data = request.get_json(silent=True) or {}
        result = service.register_user(data)
        status_code = result.pop("Code", 201)
        return jsonify(result), status_code
    except ValueError as e:
        return jsonify({"Code": 400, "Message": str(e)}), 400
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login user"""
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
    """Get user profile"""
    try:
        result = service.get_user_profile(request.user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@auth_bp.route("/profile", methods=["PUT"])
@require_auth
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json(silent=True) or {}
        result = service.update_profile(request.user_id, data)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500