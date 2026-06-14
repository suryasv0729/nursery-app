"""
Script to initialize the database schema on Google Cloud SQL
Run this after deploying to set up the database structure
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Initialize database schema on Google Cloud SQL"""
    
    print("🔄 Connecting to Google Cloud SQL...")
    
    try:
        # Connect to MySQL server (without specific database)
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', '34.10.117.44'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ Connected successfully!")
        
        with connection.cursor() as cursor:
            # Read and execute schema file
            print("\n📋 Reading schema.sql...")
            with open('schema.sql', 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # Split and execute each statement
            statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            
            print(f"🚀 Executing {len(statements)} SQL statements...")
            
            for i, statement in enumerate(statements, 1):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                        print(f"  ✓ Statement {i}/{len(statements)} executed")
                    except Exception as e:
                        print(f"  ⚠ Statement {i} warning: {e}")
            
            connection.commit()
            print("\n✅ Database schema initialized successfully!")
            
            # Verify tables were created
            cursor.execute(f"USE {os.getenv('DB_NAME', 'nursery_db')}")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"\n📊 Created {len(tables)} tables:")
            for table in tables:
                table_name = list(table.values())[0]
                cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                count = cursor.fetchone()['count']
                print(f"  - {table_name}: {count} rows")
        
        connection.close()
        print("\n🎉 Database initialization complete!")
        print("\n📝 Next steps:")
        print("  1. Test the connection from your app")
        print("  2. Deploy your Flask application")
        print("  3. Access your app and create an account")
        print("  4. Login with admin credentials:")
        print("     Email: admin@nursery.com")
        print("     Password: admin123")
        
    except pymysql.Error as e:
        print(f"\n❌ Database error: {e}")
        print("\n🔍 Troubleshooting:")
        print("  1. Verify your Cloud SQL instance is running")
        print("  2. Check that your IP is authorized in Cloud SQL settings")
        print("  3. Verify credentials in .env file")
        print("  4. Ensure the database 'nursery_db' exists")
        return False
    except FileNotFoundError:
        print("\n❌ schema.sql file not found!")
        print("Make sure you're running this script from the nursery_app directory")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    return True

def test_connection():
    """Test database connection"""
    print("\n🧪 Testing database connection...")
    
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', '34.10.117.44'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'nursery_db'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ Connected to MySQL version: {list(version.values())[0]}")
            
            cursor.execute("SELECT DATABASE()")
            db = cursor.fetchone()
            print(f"✅ Using database: {list(db.values())[0]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  Google Cloud SQL Database Initialization")
    print("=" * 60)
    print(f"\nDatabase Configuration:")
    print(f"  Host: {os.getenv('DB_HOST', '34.10.117.44')}")
    print(f"  Port: {os.getenv('DB_PORT', 3306)}")
    print(f"  User: {os.getenv('DB_USER', 'root')}")
    print(f"  Database: {os.getenv('DB_NAME', 'nursery_db')}")
    print("\n" + "=" * 60)
    
    # Test connection first
    if test_connection():
        print("\n" + "=" * 60)
        response = input("\n⚠️  This will create/reset database tables. Continue? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            init_database()
        else:
            print("❌ Operation cancelled")
    else:
        print("\n🔧 Please fix connection issues before initializing database")
