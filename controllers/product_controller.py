from utils.db import get_db_connection

def get_all_products():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
            products = cursor.fetchall()
            return products
    except Exception as e:
        print(e)
        return []
    finally:
        conn.close()

def get_product_by_id(product_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            if not product:
                return None
                
            # Fetch reviews
            cursor.execute('''
                SELECT r.*, u.name as user_name 
                FROM reviews r 
                JOIN users u ON r.user_id = u.id 
                WHERE r.product_id = %s
            ''', (product_id,))
            reviews = cursor.fetchall()
            
            product['reviews'] = reviews
            return product
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()

def add_product(data):
    if not data or not data.get('name') or not data.get('price') or not data.get('category'):
        return None

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO products (name, description, price, category, stock, image_url, origin, bloom_time, medicinal_uses, other_uses, psychology_note, watering_time)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (data['name'], data.get('description', ''), data['price'], 
                 data['category'], data.get('stock', 0), data.get('image_url', ''),
                 data.get('origin', ''), data.get('bloom_time', ''), data.get('medicinal_uses', ''),
                 data.get('other_uses', ''), data.get('psychology_note', ''), data.get('watering_time', ''))
            )
            conn.commit()
            return {'message': 'Product added successfully'}
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()

def add_review(product_id, user_id, data):
    if not data or not data.get('rating') or not data.get('comment'):
        return None
        
    rating = int(data['rating'])
    if rating < 1 or rating > 5:
        return None

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (%s, %s, %s, %s)",
                (user_id, product_id, rating, data['comment'])
            )
            conn.commit()
            return {'message': 'Review added successfully'}
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()

def update_product(product_id, data):
    if not data:
        return None
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """UPDATE products 
                   SET name=%s, description=%s, price=%s, category=%s, stock=%s, image_url=%s,
                       origin=%s, bloom_time=%s, medicinal_uses=%s, other_uses=%s, psychology_note=%s, watering_time=%s
                   WHERE id=%s""",
                (data.get('name'), data.get('description', ''), data.get('price'), 
                 data.get('category'), data.get('stock', 0), data.get('image_url', ''), 
                 data.get('origin', ''), data.get('bloom_time', ''), data.get('medicinal_uses', ''), 
                 data.get('other_uses', ''), data.get('psychology_note', ''), data.get('watering_time', ''), 
                 product_id)
            )
            conn.commit()
            return {'message': 'Product updated successfully'}
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM cart WHERE product_id = %s", (product_id,))
            cursor.execute("DELETE FROM wishlist WHERE product_id = %s", (product_id,))
            cursor.execute("DELETE FROM reviews WHERE product_id = %s", (product_id,))
            
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
            return {'message': 'Product deleted successfully'}
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()
