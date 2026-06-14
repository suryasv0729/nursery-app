from flask import Blueprint, jsonify, request
from controllers.tribute_controller import get_tribute_data, claim_reward
from controllers.auth_controller import verify_token, authorize

tribute_bp = Blueprint('tribute', __name__)

@tribute_bp.route('/', methods=['GET'])
def get_tribute():
    # Attempt to extract user_id from optional auth token
    user_id = None
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        payload = verify_token(token)
        if payload and 'user_id' in payload:
            user_id = payload['user_id']
            
    res = get_tribute_data(user_id)
    return jsonify(res['data']), res['status']

@tribute_bp.route('/claim', methods=['POST'])
@authorize()
def claim_reward_route(current_user_id, current_user_role):
    data = request.json
    product_ids = data.get('product_ids', [])
    res = claim_reward(current_user_id, product_ids)
    return jsonify(res['data']), res['status']

