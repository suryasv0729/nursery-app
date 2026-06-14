from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from utils.auth import token_required

product_bp = Blueprint('products', __name__)

@product_bp.route('/', methods=['GET'])
def get_products():
    try:
        category = request.args.get('category')
        search = request.args.get('search')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, name, description, price, category, stock, image_url, origin, bloom_time, medicinal_uses, other_uses, psychology_note, watering_time FROM products WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        if search:
            query += " AND (name LIKE %s OR description LIKE %s)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        products = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        products_list = []
        for p in products:
            products_list.append({
                'id': p[0],
                'name': p[1],
                'description': p[2],
                'price': float(p[3]),
                'category': p[4],
                'stock': p[5],
                'image_url': p[6],
                'origin': p[7],
                'bloom_time': p[8],
                'medicinal_uses': p[9],
                'other_uses': p[10],
                'psychology_note': p[11],
                'watering_time': p[12]
            })
        
        return jsonify(products_list), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, name, description, price, category, stock, image_url, origin, bloom_time, medicinal_uses, other_uses, psychology_note, watering_time FROM products WHERE id = %s",
            (product_id,)
        )
        product = cursor.fetchone()
        
        if not product:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Product not found'}), 404
        
        # Get reviews
        cursor.execute(
            """SELECT r.id, r.rating, r.comment, r.created_at, u.name 
               FROM reviews r 
               JOIN users u ON r.user_id = u.id 
               WHERE r.product_id = %s 
               ORDER BY r.created_at DESC""",
            (product_id,)
        )
        reviews = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        reviews_list = []
        for r in reviews:
            reviews_list.append({
                'id': r[0],
                'rating': r[1],
                'comment': r[2],
                'created_at': r[3].isoformat() if r[3] else None,
                'user_name': r[4]
            })
        
        product_data = {
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': float(product[3]),
            'category': product[4],
            'stock': product[5],
            'image_url': product[6],
            'origin': product[7],
            'bloom_time': product[8],
            'medicinal_uses': product[9],
            'other_uses': product[10],
            'psychology_note': product[11],
            'watering_time': product[12],
            'reviews': reviews_list
        }
        
        return jsonify(product_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
        categories = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify([cat[0] for cat in categories]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>/reviews', methods=['POST'])
@token_required
def add_review(current_user, product_id):
    try:
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if not rating or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if product exists
        cursor.execute("SELECT id FROM products WHERE id = %s", (product_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Product not found'}), 404
        
        # Insert review
        cursor.execute(
            "INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (%s, %s, %s, %s)",
            (current_user['user_id'], product_id, rating, comment)
        )
        conn.commit()
        review_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Review added successfully',
            'review_id': review_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/wishlist', methods=['GET'])
@token_required
def get_wishlist(current_user):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT p.id, p.name, p.description, p.price, p.category, p.stock, p.image_url 
               FROM wishlist w 
               JOIN products p ON w.product_id = p.id 
               WHERE w.user_id = %s 
               ORDER BY w.created_at DESC""",
            (current_user['user_id'],)
        )
        products = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        wishlist = []
        for p in products:
            wishlist.append({
                'id': p[0],
                'name': p[1],
                'description': p[2],
                'price': float(p[3]),
                'category': p[4],
                'stock': p[5],
                'image_url': p[6]
            })
        
        return jsonify(wishlist), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/wishlist/<int:product_id>', methods=['POST'])
@token_required
def add_to_wishlist(current_user, product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if product exists
        cursor.execute("SELECT id FROM products WHERE id = %s", (product_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Product not found'}), 404
        
        # Add to wishlist (ignore if already exists)
        cursor.execute(
            "INSERT IGNORE INTO wishlist (user_id, product_id) VALUES (%s, %s)",
            (current_user['user_id'], product_id)
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Added to wishlist'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/wishlist/<int:product_id>', methods=['DELETE'])
@token_required
def remove_from_wishlist(current_user, product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM wishlist WHERE user_id = %s AND product_id = %s",
            (current_user['user_id'], product_id)
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Removed from wishlist'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
