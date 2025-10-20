# backend/ai_chat/app.py
import os
from flask import Flask, request
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Allowed origins (edit if your FE runs elsewhere)
    origins = [o.strip() for o in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",") if o.strip()]

    # Apply CORS to all /chat/* routes
    CORS(app,
         resources={r"/chat/*": {"origins": origins}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "OPTIONS"])

    # Ensure even error responses include CORS headers
    @app.after_request
    def add_cors_headers(resp):
        origin = request.headers.get("Origin")
        if origin and any(origin == o for o in origins):
            resp.headers.setdefault("Access-Control-Allow-Origin", origin)
            resp.headers.setdefault("Vary", "Origin")
            resp.headers.setdefault("Access-Control-Allow-Credentials", "true")
            resp.headers.setdefault("Access-Control-Allow-Headers", "Content-Type, Authorization")
            resp.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        return resp

    # Register blueprints
    from controllers.chat_controller import chat_bp
    app.register_blueprint(chat_bp, url_prefix="/chat")

    return app

if __name__ == "__main__":
    app = create_app()
    print("Routes:")
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(host="0.0.0.0", port=5002, debug=True)