from flask import Blueprint, request, jsonify
from controllers.product_controller import get_all_products, get_product_by_id, add_product, add_review
from controllers.auth_controller import authorize

product_bp = Blueprint('products', __name__)

# GET /products/ - Get all products
@product_bp.route('/', methods=['GET'])
def get_products():
    return jsonify(get_all_products()), 200

# GET /products/<id> - Get single product
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'message': 'Not found'}), 404
    return jsonify(product), 200

# POST /products/ - Admin adds a new product
@product_bp.route('/', methods=['POST'])
@authorize(role_required='admin')
def create_product(current_user_id, current_user_role):
    data = request.json
    res = add_product(data)
    if res:
        return jsonify(res), 201
    return jsonify({'message': 'Failed'}), 400

# POST /products/<id>/reviews - User adds a review
@product_bp.route('/<int:product_id>/reviews', methods=['POST'])
@authorize()
def review_product(product_id, current_user_id, current_user_role):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    review = add_review(product_id, current_user_id, data)
    if not review:
        return jsonify({"error": "Failed to add review"}), 400
    return jsonify(review), 201

# PUT /products/<id> - Admin updates a product
@product_bp.route('/<int:product_id>', methods=['PUT'])
@authorize(role_required='admin')
def update_product_route(product_id, current_user_id, current_user_role):
    data = request.json
    from controllers.product_controller import update_product # dynamic import to avoid circular logic
    res = update_product(product_id, data)
    if res:
        return jsonify(res), 200
    return jsonify({'message': 'Failed'}), 400

# DELETE /products/<id> - Admin deletes a product
@product_bp.route('/<int:product_id>', methods=['DELETE'])
@authorize(role_required='admin')
def delete_product_route(product_id, current_user_id, current_user_role):
    from controllers.product_controller import delete_product
    res = delete_product(product_id)
    if res:
        return jsonify(res), 200
    return jsonify({'message': 'Failed'}), 400