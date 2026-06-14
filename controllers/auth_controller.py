import jwt
import datetime
import os
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import get_db_connection
from utils.mail import send_email

def handle_forgot_password(data):
    if not data or not data.get('email'):
        return jsonify({'message': 'Please provide email'}), 400
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, role FROM users WHERE email = %s", (data['email'],))
            user = cursor.fetchone()
            if not user:
                return jsonify({'message': 'If an account exists, a reset link was sent.'}), 200
                
            if user['role'] == 'admin':
                # For security, do not allow admins to perform forgot-password,
                # but return a generic response to prevent email discovery
                return jsonify({'message': 'If an account exists, a reset link was sent.'}), 200
            
            token = jwt.encode({
                'id': user['id'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, os.getenv('SECRET_KEY', 'default_secret'), algorithm='HS256')
            
            reset_link = f"http://localhost:5000/reset-password?token={token}"
            email_body = f"Click the link to reset your password: {reset_link}\nThis link expires in 30 minutes."
            
            send_email(data['email'], 'Password Reset - GreenHaven', email_body)
            return jsonify({'message': 'Password reset link sent to your email!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal Server Error'}), 500
    finally:
        conn.close()

def handle_reset_password(data):
    if not data or not data.get('token') or not data.get('password'):
        return jsonify({'message': 'Missing data'}), 400
    try:
        decoded = jwt.decode(data['token'], os.getenv('SECRET_KEY', 'default_secret'), algorithms=['HS256'])
        user_id = decoded['id']
        hashed_pw = generate_password_hash(data['password'])
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (hashed_pw, user_id))
                conn.commit()
                return jsonify({'message': 'Password reset successfully!'}), 200
        finally:
            conn.close()
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Reset link has expired.'}), 400
    except Exception as e:
        return jsonify({'message': 'Invalid token.'}), 400

def register_user(data):
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Please provide name, email and password'}), 400
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check if email exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (data['email'],))
            if cursor.fetchone():
                return jsonify({'message': 'Email already exists'}), 400
                
            hashed_pw = generate_password_hash(data['password'])
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                (data['name'], data['email'], hashed_pw)
            )
            conn.commit()
            return jsonify({'message': 'Registration successful'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

def login_user(data):
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Please provide email and password'}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (data['email'],))
            user = cursor.fetchone()
            
            if not user or not check_password_hash(user['password_hash'], data['password']):
                return jsonify({'message': 'Invalid credentials'}), 401
                
            token = jwt.encode({
                'id': user['id'],
                'role': user['role'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, os.getenv('SECRET_KEY', 'default_secret'), algorithm='HS256')
            
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role']
                }
            }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

def verify_token(token):
    try:
        data = jwt.decode(token, os.getenv('SECRET_KEY', 'default_secret'), algorithms=['HS256'])
        return {'user_id': data.get('id'), 'role': data.get('role')}
    except Exception:
        return None

def authorize(role_required=None):
    from functools import wraps
    from flask import request
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                parts = request.headers['Authorization'].split()
                if len(parts) == 2 and parts[0] == 'Bearer':
                    token = parts[1]
            
            if not token:
                return jsonify({'message': 'Token is missing'}), 401
                
            try:
                data = jwt.decode(token, os.getenv('SECRET_KEY', 'default_secret'), algorithms=['HS256'])
                if role_required and data.get('role') != role_required:
                    return jsonify({'message': 'Unauthorized role'}), 403
                # Inject current user ID into kwargs
                kwargs['current_user_id'] = data.get('id')
                kwargs['current_user_role'] = data.get('role')
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 401
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
