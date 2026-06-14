from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from utils.auth import token_required, admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/products', methods=['POST'])
@admin_required
def create_product(current_user):
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        price = data.get('price')
        category = data.get('category')
        stock = data.get('stock', 0)
        image_url = data.get('image_url', '')
        origin = data.get('origin', '')
        bloom_time = data.get('bloom_time', '')
        medicinal_uses = data.get('medicinal_uses', '')
        other_uses = data.get('other_uses', '')
        psychology_note = data.get('psychology_note', '')
        watering_time = data.get('watering_time', '')
        
        if not name or not price or not category:
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO products 
               (name, description, price, category, stock, image_url, origin, bloom_time, 
                medicinal_uses, other_uses, psychology_note, watering_time) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (name, description, price, category, stock, image_url, origin, bloom_time,
             medicinal_uses, other_uses, psychology_note, watering_time)
        )
        conn.commit()
        product_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Product created successfully',
            'product_id': product_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/products/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(current_user, product_id):
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if product exists
        cursor.execute("SELECT id FROM products WHERE id = %s", (product_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Product not found'}), 404
        
        # Build update query dynamically
        fields = []
        values = []
        
        allowed_fields = ['name', 'description', 'price', 'category', 'stock', 'image_url',
                         'origin', 'bloom_time', 'medicinal_uses', 'other_uses', 
                         'psychology_note', 'watering_time']
        
        for field in allowed_fields:
            if field in data:
                fields.append(f"{field} = %s")
                values.append(data[field])
        
        if not fields:
            cursor.close()
            conn.close()
            return jsonify({'error': 'No fields to update'}), 400
        
        values.append(product_id)
        query = f"UPDATE products SET {', '.join(fields)} WHERE id = %s"
        
        cursor.execute(query, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Product updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(current_user, product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Product not found'}), 404
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/orders', methods=['GET'])
@admin_required
def get_all_orders(current_user):
    try:
        status = request.args.get('status')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """SELECT o.id, o.user_id, u.name, u.email, o.total_amount, o.status, 
                         o.shipping_address, o.mobile_number, o.created_at
                   FROM orders o 
                   JOIN users u ON o.user_id = u.id"""
        params = []
        
        if status:
            query += " WHERE o.status = %s"
            params.append(status)
        
        query += " ORDER BY o.created_at DESC"
        
        cursor.execute(query, params)
        orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        orders_list = []
        for o in orders:
            orders_list.append({
                'id': o[0],
                'user_id': o[1],
                'user_name': o[2],
                'user_email': o[3],
                'total_amount': float(o[4]),
                'status': o[5],
                'shipping_address': o[6],
                'mobile_number': o[7],
                'created_at': o[8].isoformat() if o[8] else None
            })
        
        return jsonify(orders_list), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
@admin_required
def update_order_status(current_user, order_id):
    try:
        data = request.get_json()
        status = data.get('status')
        
        valid_statuses = ['pending', 'paid', 'shipped', 'delivered', 'cancelled']
        if status not in valid_statuses:
            return jsonify({'error': 'Invalid status'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE orders SET status = %s WHERE id = %s",
            (status, order_id)
        )
        conn.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Order not found'}), 404
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Order status updated'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/messages', methods=['GET'])
@admin_required
def get_messages(current_user):
    try:
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, name, email, subject, message, is_read, created_at FROM messages"
        if unread_only:
            query += " WHERE is_read = FALSE"
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query)
        messages = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        messages_list = []
        for m in messages:
            messages_list.append({
                'id': m[0],
                'name': m[1],
                'email': m[2],
                'subject': m[3],
                'message': m[4],
                'is_read': bool(m[5]),
                'created_at': m[6].isoformat() if m[6] else None
            })
        
        return jsonify(messages_list), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/messages/<int:message_id>/read', methods=['PUT'])
@admin_required
def mark_message_read(current_user, message_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE messages SET is_read = TRUE WHERE id = %s",
            (message_id,)
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Message marked as read'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
