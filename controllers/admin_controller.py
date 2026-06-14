from flask import jsonify
from utils.db import get_db_connection

def get_dashboard_stats():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total_users FROM users WHERE role='user'")
            total_users = cursor.fetchone()['total_users']
            
            cursor.execute("SELECT COUNT(*) AS total_orders FROM orders")
            total_orders = cursor.fetchone()['total_orders']
            
            cursor.execute("SELECT SUM(total_amount) AS revenue FROM orders WHERE status != 'cancelled'")
            revenue = cursor.fetchone()['revenue'] or 0
            
            return jsonify({
                'total_users': total_users,
                'total_orders': total_orders,
                'revenue': float(revenue)
            }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

def get_all_users():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, role, created_at FROM users ORDER BY created_at DESC")
            users = cursor.fetchall()
            return jsonify(users), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

def get_all_orders():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT o.id, o.user_id, u.name as user_name, o.total_amount, o.status, o.created_at
                FROM orders o
                JOIN users u ON o.user_id = u.id
                ORDER BY o.created_at DESC
            ''')
            orders = cursor.fetchall()
            return jsonify(orders), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()
