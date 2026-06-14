import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from utils.db import get_db_connection

def update():
    conn = get_db_connection()
    try:
        with conn.cursor() as c:
            c.execute("UPDATE orders SET status='shipped' WHERE id=4")
        conn.commit()
        print("Updated order 4 to shipped")
    finally:
        conn.close()

if __name__ == '__main__':
    update()
