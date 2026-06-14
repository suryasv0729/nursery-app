import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from utils.db import get_db_connection

def check():
    conn = get_db_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT * FROM users WHERE name LIKE '%kanna%'")
            user = c.fetchone()
            
            if not user:
                print("User not found.")
                return
                
            print(f"User: {user}")
            
            c.execute("SELECT * FROM orders WHERE user_id = %s", (user['id'],))
            orders = c.fetchall()
            print("\nOrders:")
            for o in orders:
                print(o)
                
            c.execute('''
                SELECT oi.*, o.status, o.total_amount 
                FROM order_items oi 
                JOIN orders o ON oi.order_id = o.id 
                WHERE o.user_id = %s
            ''', (user['id'],))
            items = c.fetchall()
            
            print("\nItems:")
            for i in items:
                print(i)
                
            c.execute('''
                SELECT SUM(oi.quantity) as total_plants
                FROM orders o
                JOIN order_items oi ON o.id = oi.order_id
                WHERE o.user_id = %s AND o.status != 'cancelled' AND o.total_amount > 0
            ''', (user['id'],))
            total = c.fetchone()
            print(f"\nStreak Calculation Output: {total}")
            
    finally:
        conn.close()

if __name__ == '__main__':
    check()
