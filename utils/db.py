import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Create a database connection to Google Cloud SQL.
    Supports both direct connection (via public IP) and Cloud SQL Proxy.
    """
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'nursery_db'),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10,
        charset='utf8mb4'
    )
