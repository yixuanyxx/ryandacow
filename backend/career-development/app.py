from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
sys.path.append('..')

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, origins=os.getenv("CORS_ORIGINS", "*").split(","), supports_credentials=True)
    
    # Register blueprints
    from controllers.pathways_controller import pathways_bp
    
    app.register_blueprint(pathways_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    port = "5003"
    print(f"Career Development microservice running on port {port}")
    app.run(host="0.0.0.0", port=int(port), debug=True)