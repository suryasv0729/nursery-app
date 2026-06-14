from utils.db import get_db_connection

def get_tribute_data(user_id=None):
    conn = get_db_connection()
    try:
        data = {
            'top_contributors': [],
            'user_stats': None,
            'rewards': []
        }
        with conn.cursor() as cursor:
            # 1. Top 5 Contributors (excluding cancelled orders and reward orders)
            cursor.execute('''
                SELECT u.name, SUM(oi.quantity) as total_plants
                FROM users u
                JOIN orders o ON u.id = o.user_id
                JOIN order_items oi ON o.id = oi.order_id
                JOIN products p ON oi.product_id = p.id
                WHERE o.status != 'cancelled' AND o.total_amount > 0 AND p.category NOT IN ('Pots', 'Organic Pesticides')
                GROUP BY u.id
                ORDER BY total_plants DESC
                LIMIT 5
            ''')
            top_users = cursor.fetchall()
            data['top_contributors'] = top_users
            
            # 2. Authenticated user stats
            if user_id:
                cursor.execute('''
                    SELECT SUM(oi.quantity) as total_plants, 
                           (SELECT reward_claimed FROM users WHERE id = %s) as reward_claimed
                    FROM orders o
                    JOIN order_items oi ON o.id = oi.order_id
                    JOIN products p ON oi.product_id = p.id
                    WHERE o.user_id = %s AND o.status != 'cancelled' AND o.total_amount > 0 AND p.category NOT IN ('Pots', 'Organic Pesticides')
                ''', (user_id, user_id))
                user_res = cursor.fetchone()
                total_user_plants = user_res['total_plants'] if user_res and user_res['total_plants'] else 0
                
                data['user_stats'] = {
                    'total_plants': int(total_user_plants),
                    'reward_claimed': bool(user_res['reward_claimed']) if user_res else False
                }
                
                # 3. Rewards setup if total >= 50 and not claimed
                if total_user_plants >= 50 and not data['user_stats']['reward_claimed']:
                    cursor.execute('''
                        SELECT id, name, category, image_url, price 
                        FROM products 
                        WHERE stock > 0
                        ORDER BY category
                    ''')
                    all_products = cursor.fetchall()
                    
                    # Group by category
                    cat_map = {}
                    for p in all_products:
                        cat = p['category']
                        if cat not in cat_map:
                            cat_map[cat] = []
                        cat_map[cat].append(p)
                        
                    data['reward_categories'] = [{"category": k, "products": v} for k, v in cat_map.items()]
                    
        return {'status': 200, 'data': data}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': {'message': 'Error fetching tribute data'}}
    finally:
        conn.close()

def claim_reward(user_id, product_ids):
    if not product_ids or not isinstance(product_ids, list):
        return {'status': 400, 'data': {'message': 'Invalid selection'}}
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check eligibility
            cursor.execute('''
                SELECT reward_claimed FROM users WHERE id = %s
            ''', (user_id,))
            user_res = cursor.fetchone()
            
            if not user_res or user_res['reward_claimed']:
                return {'status': 400, 'data': {'message': 'Reward already claimed or user not found'}}
                
            cursor.execute('''
                SELECT SUM(oi.quantity) as total_plants
                FROM orders o
                JOIN order_items oi ON o.id = oi.order_id
                JOIN products p ON oi.product_id = p.id
                WHERE o.user_id = %s AND o.status != 'cancelled' AND o.total_amount > 0 AND p.category NOT IN ('Pots', 'Organic Pesticides')
            ''', (user_id,))
            stats = cursor.fetchone()
            total_plants = stats['total_plants'] if stats and stats['total_plants'] else 0
            
            if total_plants < 50:
                return {'status': 400, 'data': {'message': 'Not eligible yet'}}
            
            # Verify exactly 1 product per category is selected
            format_strings = ','.join(['%s'] * len(product_ids))
            cursor.execute(f'''
                SELECT id, category FROM products WHERE id IN ({format_strings})
            ''', tuple(product_ids))
            
            selected_products = cursor.fetchall()
            
            if not selected_products:
                return {'status': 400, 'data': {'message': 'Invalid products'}}
                
            # Create the free Reward Order
            import uuid
            rzp_order_id = f"reward_{uuid.uuid4().hex[:10]}"
            
            cursor.execute('''
                INSERT INTO orders (user_id, total_amount, status, razorpay_order_id)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, 0.00, 'paid', rzp_order_id))
            
            order_id = cursor.lastrowid
            
            # Insert items (price is 0)
            for p in selected_products:
                cursor.execute('''
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                ''', (order_id, p['id'], 1, 0.00))
                
            # Mark claimed
            cursor.execute('''
                UPDATE users SET reward_claimed = TRUE WHERE id = %s
            ''', (user_id,))
            
            conn.commit()
            return {'status': 200, 'data': {'message': 'Rewards claimed successfully! Check your orders.'}}
            
    except Exception as e:
        print(e)
        return {'status': 500, 'data': {'message': 'Error processing claim'}}
    finally:
        conn.close()
