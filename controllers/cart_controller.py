from utils.db import get_db_connection

def get_cart(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT c.id, c.product_id, c.quantity, p.name, p.price, p.image_url 
                FROM cart c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = %s
            ''', (user_id,))
            return cursor.fetchall()
    except Exception as e:
        print(e)
        return []
    finally:
        conn.close()

def add_to_cart(user_id, product_id, quantity=1):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check if exists
            cursor.execute("SELECT id, quantity FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            item = cursor.fetchone()
            
            if item:
                cursor.execute("UPDATE cart SET quantity = quantity + %s WHERE id = %s", (quantity, item['id']))
            else:
                cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)", 
                               (user_id, product_id, quantity))
            conn.commit()
            return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()

def update_cart_quantity(user_id, product_id, quantity):
    conn = get_db_connection()
    try:
        if quantity <= 0:
            return remove_from_cart(user_id, product_id)
            
        with conn.cursor() as cursor:
            cursor.execute("UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s", 
                           (quantity, user_id, product_id))
            conn.commit()
            return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()

def remove_from_cart(user_id, product_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            conn.commit()
            return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()

def get_wishlist(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT w.id, w.product_id, p.name, p.price, p.image_url 
                FROM wishlist w
                JOIN products p ON w.product_id = p.id
                WHERE w.user_id = %s
            ''', (user_id,))
            return cursor.fetchall()
    except Exception as e:
        print(e)
        return []
    finally:
        conn.close()

def toggle_wishlist(user_id, product_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM wishlist WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            item = cursor.fetchone()
            
            if item:
                cursor.execute("DELETE FROM wishlist WHERE id = %s", (item['id'],))
                conn.commit()
                return {'message': 'Removed from wishlist', 'is_wishlisted': False}
            else:
                cursor.execute("INSERT INTO wishlist (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
                conn.commit()
                return {'message': 'Added to wishlist', 'is_wishlisted': True}
    except Exception as e:
        print(e)
        return {'message': 'Database error'}
    finally:
        conn.close()
