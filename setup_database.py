#!/usr/bin/env python
import pymysql
import sys

def create_database():
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            charset='utf8'
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS symptoms")
        cursor.execute("USE symptoms")
        
        # Create register table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS register(
                username VARCHAR(50) PRIMARY KEY,
                password VARCHAR(50),
                contact_no VARCHAR(20),
                email VARCHAR(50), 
                address VARCHAR(80)
            )
        """)
        
        # Create log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log(
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                symptoms_text VARCHAR(400),
                predicted_advice VARCHAR(60),
                checked_date VARCHAR(40)
            )
        """)
        
        connection.commit()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("Database created successfully!")
        print("Tables:", tables)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if create_database():
        print("Database setup completed successfully!")
    else:
        print("Database setup failed!")
        sys.exit(1)
