from functools import wraps
from flask import request, jsonify
import jwt
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = {
                'user_id': decoded['user_id'],
                'email': decoded['email'],
                'role': decoded['role']
            }
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            
            if decoded.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            current_user = {
                'user_id': decoded['user_id'],
                'email': decoded['email'],
                'role': decoded['role']
            }
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated
