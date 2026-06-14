from flask import Blueprint, request, jsonify
import razorpay
import os
from utils.db import get_db_connection
from utils.auth import token_required

order_bp = Blueprint('orders', __name__)

# Initialize Razorpay client
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)) if RAZORPAY_KEY_ID else None

@order_bp.route('/', methods=['GET'])
@token_required
def get_orders(current_user):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, total_amount, status, shipping_address, mobile_number, created_at 
               FROM orders 
               WHERE user_id = %s 
               ORDER BY created_at DESC""",
            (current_user['user_id'],)
        )
        orders = cursor.fetchall()
        
        orders_list = []
        for o in orders:
            # Get order items
            cursor.execute(
                """SELECT oi.product_id, oi.quantity, oi.price, p.name, p.image_url 
                   FROM order_items oi 
                   JOIN products p ON oi.product_id = p.id 
                   WHERE oi.order_id = %s""",
                (o[0],)
            )
            items = cursor.fetchall()
            
            items_list = []
            for item in items:
                items_list.append({
                    'product_id': item[0],
                    'quantity': item[1],
                    'price': float(item[2]),
                    'product_name': item[3],
                    'image_url': item[4]
                })
            
            orders_list.append({
                'id': o[0],
                'total_amount': float(o[1]),
                'status': o[2],
                'shipping_address': o[3],
                'mobile_number': o[4],
                'created_at': o[5].isoformat() if o[5] else None,
                'items': items_list
            })
        
        cursor.close()
        conn.close()
        
        return jsonify(orders_list), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_bp.route('/<int:order_id>', methods=['GET'])
@token_required
def get_order(current_user, order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, total_amount, status, shipping_address, mobile_number, 
                      razorpay_order_id, razorpay_payment_id, created_at 
               FROM orders 
               WHERE id = %s AND user_id = %s""",
            (order_id, current_user['user_id'])
        )
        order = cursor.fetchone()
        
        if not order:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Order not found'}), 404
        
        # Get order items
        cursor.execute(
            """SELECT oi.product_id, oi.quantity, oi.price, p.name, p.image_url 
               FROM order_items oi 
               JOIN products p ON oi.product_id = p.id 
               WHERE oi.order_id = %s""",
            (order_id,)
        )
        items = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        items_list = []
        for item in items:
            items_list.append({
                'product_id': item[0],
                'quantity': item[1],
                'price': float(item[2]),
                'product_name': item[3],
                'image_url': item[4]
            })
        
        order_data = {
            'id': order[0],
            'total_amount': float(order[1]),
            'status': order[2],
            'shipping_address': order[3],
            'mobile_number': order[4],
            'razorpay_order_id': order[5],
            'razorpay_payment_id': order[6],
            'created_at': order[7].isoformat() if order[7] else None,
            'items': items_list
        }
        
        return jsonify(order_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_bp.route('/create', methods=['POST'])
@token_required
def create_order(current_user):
    try:
        data = request.get_json()
        shipping_address = data.get('shipping_address')
        mobile_number = data.get('mobile_number')
        
        if not shipping_address or not mobile_number:
            return jsonify({'error': 'Shipping address and mobile number are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get cart items
        cursor.execute(
            """SELECT c.product_id, c.quantity, p.price, p.stock 
               FROM cart c 
               JOIN products p ON c.product_id = p.id 
               WHERE c.user_id = %s""",
            (current_user['user_id'],)
        )
        cart_items = cursor.fetchall()
        
        if not cart_items:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate total and check stock
        total_amount = 0
        for item in cart_items:
            if item[3] < item[1]:  # stock < quantity
                cursor.close()
                conn.close()
                return jsonify({'error': f'Insufficient stock for product ID {item[0]}'}), 400
            total_amount += float(item[2]) * item[1]
        
        # Create Razorpay order
        razorpay_order_id = None
        if razorpay_client:
            try:
                razorpay_order = razorpay_client.order.create({
                    'amount': int(total_amount * 100),  # Amount in paise
                    'currency': 'INR',
                    'payment_capture': 1
                })
                razorpay_order_id = razorpay_order['id']
            except Exception as e:
                print(f"Razorpay error: {e}")
        
        # Create order
        cursor.execute(
            """INSERT INTO orders (user_id, total_amount, status, shipping_address, mobile_number, razorpay_order_id) 
               VALUES (%s, %s, 'pending', %s, %s, %s)""",
            (current_user['user_id'], total_amount, shipping_address, mobile_number, razorpay_order_id)
        )
        order_id = cursor.lastrowid
        
        # Create order items and update stock
        for item in cart_items:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, item[0], item[1], item[2])
            )
            cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE id = %s",
                (item[1], item[0])
            )
        
        # Clear cart
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (current_user['user_id'],))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Order created successfully',
            'order_id': order_id,
            'razorpay_order_id': razorpay_order_id,
            'amount': total_amount,
            'razorpay_key_id': RAZORPAY_KEY_ID
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_bp.route('/verify-payment', methods=['POST'])
@token_required
def verify_payment(current_user):
    try:
        data = request.get_json()
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return jsonify({'error': 'Missing payment details'}), 400
        
        # Verify signature
        if razorpay_client:
            try:
                razorpay_client.utility.verify_payment_signature({
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature
                })
            except Exception as e:
                return jsonify({'error': 'Payment verification failed'}), 400
        
        # Update order status
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """UPDATE orders 
               SET status = 'paid', razorpay_payment_id = %s, razorpay_signature = %s 
               WHERE razorpay_order_id = %s AND user_id = %s""",
            (razorpay_payment_id, razorpay_signature, razorpay_order_id, current_user['user_id'])
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Payment verified successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
