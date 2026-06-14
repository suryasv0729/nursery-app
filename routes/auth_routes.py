from flask import Blueprint, request, jsonify
from controllers.auth_controller import register_user, login_user, handle_forgot_password, handle_reset_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    return register_user(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return login_user(data)

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    return handle_forgot_password(data)

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    return handle_reset_password(data)
