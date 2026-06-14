import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from utils.db import get_db_connection

def migrate():
    conn = get_db_connection()
    try:
        with conn.cursor() as c:
            try:
                c.execute("ALTER TABLE orders ADD COLUMN mobile_number VARCHAR(20)")
                print("Column mobile_number added to orders table.")
            except Exception as e:
                print(f"Migration error (might already exist): {e}")
        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
