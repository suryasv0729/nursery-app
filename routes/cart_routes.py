from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from utils.auth import token_required

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@token_required
def get_cart(current_user):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT c.id, c.product_id, c.quantity, p.name, p.price, p.image_url, p.stock 
               FROM cart c 
               JOIN products p ON c.product_id = p.id 
               WHERE c.user_id = %s""",
            (current_user['user_id'],)
        )
        items = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        cart_items = []
        total = 0
        for item in items:
            subtotal = float(item[4]) * item[2]
            total += subtotal
            cart_items.append({
                'id': item[0],
                'product_id': item[1],
                'quantity': item[2],
                'product_name': item[3],
                'price': float(item[4]),
                'image_url': item[5],
                'stock': item[6],
                'subtotal': subtotal
            })
        
        return jsonify({
            'items': cart_items,
            'total': total
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/add', methods=['POST'])
@token_required
def add_to_cart(current_user):
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id or quantity < 1:
            return jsonify({'error': 'Invalid product_id or quantity'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if product exists and has stock
        cursor.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Product not found'}), 404
        
        if product[0] < quantity:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Insufficient stock'}), 400
        
        # Check if item already in cart
        cursor.execute(
            "SELECT id, quantity FROM cart WHERE user_id = %s AND product_id = %s",
            (current_user['user_id'], product_id)
        )
        existing_item = cursor.fetchone()
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item[1] + quantity
            if product[0] < new_quantity:
                cursor.close()
                conn.close()
                return jsonify({'error': 'Insufficient stock'}), 400
            
            cursor.execute(
                "UPDATE cart SET quantity = %s WHERE id = %s",
                (new_quantity, existing_item[0])
            )
        else:
            # Insert new item
            cursor.execute(
                "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                (current_user['user_id'], product_id, quantity)
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Item added to cart'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/update/<int:cart_id>', methods=['PUT'])
@token_required
def update_cart_item(current_user, cart_id):
    try:
        data = request.get_json()
        quantity = data.get('quantity')
        
        if not quantity or quantity < 1:
            return jsonify({'error': 'Invalid quantity'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify cart item belongs to user and check stock
        cursor.execute(
            """SELECT c.product_id, p.stock 
               FROM cart c 
               JOIN products p ON c.product_id = p.id 
               WHERE c.id = %s AND c.user_id = %s""",
            (cart_id, current_user['user_id'])
        )
        item = cursor.fetchone()
        
        if not item:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Cart item not found'}), 404
        
        if item[1] < quantity:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Insufficient stock'}), 400
        
        cursor.execute(
            "UPDATE cart SET quantity = %s WHERE id = %s",
            (quantity, cart_id)
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Cart updated'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/remove/<int:cart_id>', methods=['DELETE'])
@token_required
def remove_from_cart(current_user, cart_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM cart WHERE id = %s AND user_id = %s",
            (cart_id, current_user['user_id'])
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Item removed from cart'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/clear', methods=['DELETE'])
@token_required
def clear_cart(current_user):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM cart WHERE user_id = %s",
            (current_user['user_id'],)
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Cart cleared'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
