from flask import Blueprint, request, jsonify
from shared.auth import require_auth
import sys
sys.path.append('..')

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

# Import service from services directory
from services.chat_service import ChatService
service = ChatService()

@chat_bp.route("/message", methods=["POST"])
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

@chat_bp.route("/history", methods=["GET"])
@require_auth
def get_chat_history():
    """Get chat history for user"""
    try:
        result = service.get_chat_history(request.user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@chat_bp.route("/clear", methods=["POST"])
@require_auth
def clear_chat():
    """Clear chat history"""
    try:
        result = service.clear_chat(request.user_id)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@chat_bp.route("/test", methods=["GET"])
def test():
    """Test endpoint to verify service is running"""
    return jsonify({"Code": 200, "Message": "AI Chat service is running"}), 200

@chat_bp.route("/test-guidance", methods=["POST"])
def test_guidance():
    """Test guidance endpoint without authentication"""
    try:
        body = request.get_json(silent=True) or {}
        message = body.get("message", "test message")
        user_id = body.get("user_id", 1)
        context = {"user_profile": {"name": "Test User", "job_title": "Software Engineer"}, "user_skills": []}
        service = ChatService()
        result = service.generate_career_guidance(user_id, message, context)
        return jsonify(result), result.get("Code", 200)
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal error: {str(e)}"}), 500