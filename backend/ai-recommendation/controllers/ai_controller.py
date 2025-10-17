from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")

# Import service from services directory
from services.ai_service import AIService
service = AIService()

@ai_bp.route("/chat/message", methods=["POST"])
@require_auth
def send_message():
    """Send message to AI chatbot"""
    try:
        data = request.get_json(silent=True) or {}
        message = data.get('message')
        
        if not message:
            return jsonify({"Code": 400, "Message": "Message is required"}), 400
        
        result = service.send_message(request.user_id, message)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@ai_bp.route("/suggestions", methods=["GET"])
@require_auth
def get_quick_suggestions():
    """Get quick action suggestions"""
    try:
        result = service.get_quick_suggestions(request.user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500
