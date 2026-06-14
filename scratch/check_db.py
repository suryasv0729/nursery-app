from utils.db import get_db_connection

conn = get_db_connection()
try:
    with conn.cursor() as cursor:
        cursor.execute("SELECT DISTINCT category FROM products")
        print(cursor.fetchall())
        cursor.execute("SHOW COLUMNS FROM users LIKE 'reward_claimed'")
        print("Column exists:", bool(cursor.fetchone()))
finally:
    conn.close()
