from utils.db import get_db_connection

def update_db():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Add reward_claimed to users if it doesn't exist
            cursor.execute("SHOW COLUMNS FROM users LIKE 'reward_claimed'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE users ADD COLUMN reward_claimed BOOLEAN DEFAULT FALSE")
                conn.commit()
                print("Added reward_claimed column.")
            else:
                print("reward_claimed column already exists.")
            
            # Print categories just to see
            cursor.execute("SELECT DISTINCT category FROM products")
            categories = cursor.fetchall()
            print("Categories:", categories)
    finally:
        conn.close()

if __name__ == '__main__':
    update_db()
