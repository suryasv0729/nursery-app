import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Create and return a database connection"""
    
    # Check if we should use cloud database
    use_cloud = os.getenv('USE_CLOUD_DB', 'false').lower() == 'true'
    
    if use_cloud:
        # Cloud database configuration
        return pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'nursery_db'),
            port=int(os.getenv('DB_PORT', 3306)),
            cursorclass=pymysql.cursors.Cursor,
            charset='utf8mb4'
        )
    else:
        # Local SQLite fallback (for development)
        # Note: This uses SQLite which has different syntax than MySQL
        # For production, always use MySQL/Cloud DB
        import sqlite3
        conn = sqlite3.connect('nursery.db')
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    """Initialize the database with schema"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        with open('schema.sql', 'r') as f:
            schema = f.read()
            # Execute schema statements
            for statement in schema.split(';'):
                if statement.strip():
                    cursor.execute(statement)
        conn.commit()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        cursor.close()
        conn.close()
