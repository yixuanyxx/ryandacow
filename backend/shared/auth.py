import jwt
import os
from typing import Optional
from functools import wraps
from flask import request, jsonify

class AuthError(Exception):
    """Custom exception for authentication errors"""
    pass

def verify_token(token: str) -> Optional[int]:
    """Verify JWT token and return user ID"""
    try:
        jwt_secret = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator to require authentication for microservice endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"Code": 401, "Message": "No token provided"}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        user_id = verify_token(token)
        if not user_id:
            return jsonify({"Code": 401, "Message": "Invalid token"}), 401
        
        request.user_id = user_id
        return f(*args, **kwargs)
    return decorated_function

def generate_token(user_id: int) -> str:
    """Generate JWT token for user"""
    jwt_secret = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    payload = {
        'user_id': user_id,
        'exp': int(os.getenv('JWT_EXPIRY', 86400))  # 24 hours default
    }
    return jwt.encode(payload, jwt_secret, algorithm='HS256')
