from flask import Blueprint, request, jsonify
from controllers.cart_controller import get_cart, add_to_cart, remove_from_cart, update_cart_quantity
from controllers.cart_controller import get_wishlist, toggle_wishlist
from controllers.auth_controller import authorize

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@authorize()
def view_cart(current_user_id, current_user_role):
    items = get_cart(current_user_id)
    return jsonify(items), 200

@cart_bp.route('/add', methods=['POST'])
@authorize()
def add_item(current_user_id, current_user_role):
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({'message': 'Product ID required'}), 400
        
    res = add_to_cart(current_user_id, product_id, quantity)
    if res:
        return jsonify({'message': 'Added to cart'}), 200
    return jsonify({'message': 'Failed to add'}), 400

@cart_bp.route('/update', methods=['PUT'])
@authorize()
def update_item_quantity(current_user_id, current_user_role):
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    if not product_id or quantity is None:
        return jsonify({'message': 'Invalid data'}), 400
        
    res = update_cart_quantity(current_user_id, product_id, quantity)
    if res:
        return jsonify({'message': 'Cart updated'}), 200
    return jsonify({'message': 'Failed to update'}), 400

@cart_bp.route('/remove/<int:product_id>', methods=['DELETE'])
@authorize()
def remove_item(current_user_id, current_user_role, product_id):
    res = remove_from_cart(current_user_id, product_id)
    if res:
        return jsonify({'message': 'Removed from cart'}), 200
    return jsonify({'message': 'Failed to remove'}), 400

@cart_bp.route('/wishlist', methods=['GET'])
@authorize()
def view_wishlist(current_user_id, current_user_role):
    items = get_wishlist(current_user_id)
    return jsonify(items), 200

@cart_bp.route('/wishlist/toggle', methods=['POST'])
@authorize()
def toggle_wishlist_item(current_user_id, current_user_role):
    data = request.json
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'message': 'Product ID required'}), 400
        
    res = toggle_wishlist(current_user_id, product_id)
    return jsonify(res), 200
