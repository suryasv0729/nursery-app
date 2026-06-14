"""
Quick test script to verify Google Cloud SQL connection
"""
from utils.db import get_db_connection
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Test database connection"""
    print("=" * 60)
    print("  Testing Google Cloud SQL Connection")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Host: {os.getenv('DB_HOST')}")
    print(f"  Port: {os.getenv('DB_PORT', 3306)}")
    print(f"  User: {os.getenv('DB_USER')}")
    print(f"  Database: {os.getenv('DB_NAME')}")
    print("\n" + "=" * 60)
    
    try:
        print("\n🔄 Attempting to connect...")
        conn = get_db_connection()
        
        print("✅ Connection successful!")
        
        with conn.cursor() as cursor:
            # Test 1: Get MySQL version
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"\n📊 MySQL Version: {list(version.values())[0]}")
            
            # Test 2: Get current database
            cursor.execute("SELECT DATABASE()")
            db = cursor.fetchone()
            print(f"📊 Current Database: {list(db.values())[0]}")
            
            # Test 3: Show tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"\n📋 Found {len(tables)} tables:")
                for table in tables:
                    table_name = list(table.values())[0]
                    cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                    count = cursor.fetchone()['count']
                    print(f"  - {table_name}: {count} rows")
            else:
                print("\n⚠️  No tables found. Run init_cloud_db.py to initialize schema.")
            
            # Test 4: Check admin user
            try:
                cursor.execute("SELECT id, name, email, role FROM users WHERE role = 'admin' LIMIT 1")
                admin = cursor.fetchone()
                if admin:
                    print(f"\n👤 Admin User Found:")
                    print(f"  - Name: {admin['name']}")
                    print(f"  - Email: {admin['email']}")
                else:
                    print("\n⚠️  No admin user found. Schema may not be initialized.")
            except:
                print("\n⚠️  Users table not found. Run init_cloud_db.py first.")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed! Database is ready.")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("  1. If tables are missing, run: python init_cloud_db.py")
        print("  2. Start your Flask app: python app.py")
        print("  3. Access at: http://localhost:5000")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n🔍 Troubleshooting:")
        print("  1. Check if your Cloud SQL instance is running")
        print("  2. Verify your IP is in the authorized networks:")
        print("     - Go to: Cloud Console → SQL → Your Instance → Connections")
        print("     - Add your IP under 'Authorized networks'")
        print("  3. Verify credentials in .env file:")
        print(f"     - DB_HOST={os.getenv('DB_HOST')}")
        print(f"     - DB_USER={os.getenv('DB_USER')}")
        print(f"     - DB_NAME={os.getenv('DB_NAME')}")
        print("  4. Test MySQL connection directly:")
        print(f"     mysql -h {os.getenv('DB_HOST')} -u {os.getenv('DB_USER')} -p")
        
        return False

if __name__ == "__main__":
    test_connection()
