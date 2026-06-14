from flask import Blueprint, request, jsonify
import os
import json
import random
import urllib.request
from controllers.order_controller import create_order, verify_payment, get_user_orders
from controllers.auth_controller import authorize

order_bp = Blueprint('order', __name__)

OTP_STORE = {}


@order_bp.route('/create', methods=['POST'])
@authorize()
def init_order(current_user_id, current_user_role):
    data = request.json
    res = create_order(current_user_id, data)
    return jsonify(res['data']), res['status']

@order_bp.route('/verify', methods=['POST'])
@authorize()
def verify(current_user_id, current_user_role):
    data = request.json
    res = verify_payment(data)
    return jsonify(res['data']), res['status']

@order_bp.route('/history', methods=['GET'])
@authorize()
def history(current_user_id, current_user_role):
    orders = get_user_orders(current_user_id)
    return jsonify(orders), 200

@order_bp.route('/send-otp', methods=['POST'])
@authorize()
def send_otp(current_user_id, current_user_role):
    data = request.json or {}
    mobile = data.get('mobile_number')
    if not mobile:
        return jsonify({'message': 'Mobile number is required'}), 400
    
    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    OTP_STORE[current_user_id] = otp

    print(f"[MOCK OTP] Send to {mobile}: {otp}")
    # We still accept 123456 as a universal fallback for easy demo testing
    return jsonify({'message': 'OTP sent. (Mock mode active - check console or use 123456)'}), 200

@order_bp.route('/verify-otp', methods=['POST'])
@authorize()
def verify_otp(current_user_id, current_user_role):
    data = request.json or {}
    user_otp = data.get('otp')
    stored_otp = OTP_STORE.get(current_user_id)
    
    if user_otp == '123456' or (stored_otp and user_otp == stored_otp):
        # Clear the OTP after successful verification
        if current_user_id in OTP_STORE:
            del OTP_STORE[current_user_id]
        return jsonify({'message': 'OTP verified successfully'}), 200
        
    return jsonify({'message': 'Invalid OTP'}), 400

@order_bp.route('/<int:order_id>/cancel', methods=['POST'])
@authorize()
def cancel(current_user_id, current_user_role, order_id):
    data = request.json or {}
    reason = data.get('reason', 'No reason provided')
    from controllers.order_controller import cancel_order
    res = cancel_order(order_id, current_user_id, reason)
    return jsonify(res['data']), res['status']
