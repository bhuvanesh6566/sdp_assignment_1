"""
Database Setup Script for Face Attendance System
This script helps you create the MySQL database if it doesn't exist.
"""
import pymysql
import sys

# Database configuration - UPDATE THESE VALUES
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "bhuvan@10"  # ⚠️ CHANGE THIS to your MySQL password
DB_NAME = "face_attendance"

def create_database():
    """Creates the database if it doesn't exist."""
    try:
        print("Connecting to MySQL server...")
        # Connect without specifying database
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            charset='utf8mb4'
        )
        
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
        exists = cursor.fetchone()
        
        if exists:
            print(f"✓ Database '{DB_NAME}' already exists.")
        else:
            print(f"Creating database '{DB_NAME}'...")
            cursor.execute(f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ Database '{DB_NAME}' created successfully!")
        
        cursor.close()
        conn.close()
        
        print("\n✓ Database setup complete!")
        print(f"  Database: {DB_NAME}")
        print(f"  Host: {DB_HOST}")
        print(f"  User: {DB_USER}")
        print("\nNext steps:")
        print("  1. Make sure config.py has the same database credentials")
        print("  2. Run: python app.py")
        print("  3. The tables will be created automatically when the app starts")
        
        return True
        
    except pymysql.Error as e:
        print(f"\n✗ Database setup failed!")
        print(f"  Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure MySQL is installed and running")
        print("  2. Check that DB_USER and DB_PASS are correct in this script")
        print("  3. Try connecting manually: mysql -u root -p")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("  Face Attendance - Database Setup")
    print("=" * 50)
    print()
    
    # Warn about password
    if DB_PASS == "bhuvan@10" or DB_PASS == "your_password":
        print("⚠ WARNING: Using default password!")
        print("  Please update DB_PASS in this script with your actual MySQL password.")
        print()
        response = input("Continue anyway? (yes/no): ")
        if response.lower() != 'yes':
            print("Exiting. Please update the password first.")
            sys.exit(0)
    
    success = create_database()
    sys.exit(0 if success else 1)
