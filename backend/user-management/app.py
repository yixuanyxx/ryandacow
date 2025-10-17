from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
sys.path.append('..')

from shared.database import get_db_connection
from shared.auth import generate_token
from services.user_service import UserService

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, origins=os.getenv("CORS_ORIGINS", "*").split(","), supports_credentials=True)
    
    # Register blueprints
    from controllers.auth_controller import auth_bp
    from controllers.user_controller import user_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    port = "5001"
    print(f"User Management microservice running on port {port}")
    app.run(host="0.0.0.0", port=int(port), debug=True)