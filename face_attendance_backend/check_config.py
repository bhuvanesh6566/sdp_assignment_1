"""
Configuration Checker
Verifies that your database connection settings are correct.
"""
import sys
import pymysql
from config import Config

def check_config():
    """Checks if database connection works."""
    print("=" * 50)
    print("  Configuration Checker")
    print("=" * 50)
    print()
    
    # Parse database URI
    uri = Config.SQLALCHEMY_DATABASE_URI
    print(f"Database URI: {uri.replace(uri.split('@')[0].split('//')[1].split(':')[1], '***')}")
    print()
    
    try:
        # Extract connection details
        if 'mysql+pymysql://' in uri:
            parts = uri.replace('mysql+pymysql://', '').split('@')
            if len(parts) != 2:
                print("✗ Invalid database URI format")
                return False
            
            user_pass = parts[0].split(':')
            host_db = parts[1].split('/')
            
            if len(user_pass) != 2 or len(host_db) != 2:
                print("✗ Invalid database URI format")
                return False
            
            db_user = user_pass[0]
            db_pass = user_pass[1]
            db_host = host_db[0]
            db_name = host_db[1]
            
            print(f"Attempting to connect...")
            print(f"  Host: {db_host}")
            print(f"  User: {db_user}")
            print(f"  Database: {db_name}")
            print()
            
            # Test connection
            conn = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_pass,
                database=db_name,
                charset='utf8mb4'
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            print("✓ Database connection successful!")
            print(f"  MySQL Version: {version}")
            print(f"  Database '{db_name}' is accessible")
            print()
            print("✓ Configuration is correct. You can run the backend now!")
            return True
            
        else:
            print("✗ Only MySQL databases are supported")
            return False
            
    except pymysql.Error as e:
        print(f"✗ Database connection failed!")
        print(f"  Error: {e}")
        print()
        print("Common issues:")
        print("  1. MySQL server is not running")
        print("  2. Database doesn't exist (run setup_database.py first)")
        print("  3. Wrong username/password in config.py")
        print("  4. Database user doesn't have permissions")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = check_config()
    sys.exit(0 if success else 1)
