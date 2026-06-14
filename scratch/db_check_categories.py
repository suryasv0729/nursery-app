import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from utils.db import get_db_connection

def check():
    conn = get_db_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT DISTINCT category FROM products")
            categories = c.fetchall()
            print("Categories:")
            for cat in categories:
                print(cat)
                
            c.execute('''
                SELECT p.id, p.name, p.category 
                FROM products p
                WHERE p.id IN (1, 2, 13, 74, 81, 39, 77, 79)
            ''')
            print("\nProducts from Kanna's orders:")
            for p in c.fetchall():
                print(p)
    finally:
        conn.close()

if __name__ == '__main__':
    check()
