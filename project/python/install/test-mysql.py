import mysql.connector
from mysql.connector import Error

def test_mariadb_connection():
    connection = None
    try:
        # Connect to MariaDB server
        connection = mysql.connector.connect(
            host='localhost',  # MariaDB is running on the same container
            port=3306,         
            user='root',       # Default user
            password='root',       # Default password, change if necessary
            database='test'    # You can create this test database if needed
        )

        if connection.is_connected():
            print("Connected to MariaDB!")
            # Test the connection by querying the server version
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            print(f"MariaDB Version: {db_version[0]}")

    except Error as e:
        print(f"Error while connecting to MariaDB: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MariaDB connection closed.")

if __name__ == "__main__":
    test_mariadb_connection()
