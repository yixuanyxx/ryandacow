from flask import Blueprint, request, jsonify
from backend.shared.auth import require_auth
import sys
sys.path.append('..')
import traceback

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

# Import service from services directory
from backend.ai_chat.services.chat_service import ChatService
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

# backend/ai_chat/controllers/chat_controller.py

def _normalize_user_id(raw) -> int:
    """
    Accepts: 1 / "1" / "EMP-20001" / "EMP20001".
    Maps EMP-2000X -> X (1..99), else falls back to digits or 1.
    """
    s = str(raw or "").strip().upper()
    digits = "".join(ch for ch in s if ch.isdigit())
    if digits.startswith("200") and len(digits) >= 5:
        # EMP-20001 -> 1, EMP-20015 -> 15
        tail = digits[-2:]  # last 2 digits are usually the short employee index
        try:
            n = int(tail)
            return n if n > 0 else 1
        except ValueError:
            pass
    # Otherwise, try raw digits as-is
    try:
        return int(digits) if digits else 1
    except ValueError:
        return 1

@chat_bp.post("/guidance")
def guidance():
    body = request.get_json(force=True) or {}
    user_id = _normalize_user_id(body.get("user_id", 1))
    message = body.get("message", "career guidance")
    try:
        result = service.generate_career_guidance(user_id, message, {})
        code = result.pop("Code", 200)
        return jsonify(result), code
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"Code": 500, "Message": f"{type(e).__name__}: {e}"}), 500

@chat_bp.get("/health")
def health():
    from backend.shared.database import get_db_connection
    db = get_db_connection()
    return {"db": "ready" if db.ready() else "demo"}

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