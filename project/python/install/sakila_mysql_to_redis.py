import mysql.connector
import redis
import datetime
from decimal import Decimal
from mysql.connector import Error

# MySQL connection configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '789789',   
    'database': 'sakila'
}

# Redis connection configuration
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0   
)

def convert_to_serializable(data):
    """
    Convert non-serializable data types (like datetime, Decimal, and set) to strings.
    Replace None with an empty string for Redis compatibility.
    """
    for key, value in data.items():
        if value is None:
            data[key] = ''  # Convert None to empty string
        elif isinstance(value, (datetime.datetime, datetime.date)):
            data[key] = value.isoformat()  # Convert datetime to string in ISO format
        elif isinstance(value, Decimal):
            data[key] = str(value)  # Convert Decimal to string
        elif isinstance(value, set):
            data[key] = ','.join(str(v) for v in value)  # Convert set to comma-separated string
    return data

def import_table_to_redis(cursor, table_name, primary_key):
    """
    Import data from a MySQL table to Redis as hashes.
    Each row in the table is stored as a Redis hash with key format: {table_name}:{primary_key_value}
    """
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    for row in rows:
        # Build a dictionary for each row, mapping column names to values
        row_data = dict(zip(columns, row))
        
        # Convert non-serializable types to Redis-compatible formats
        row_data = convert_to_serializable(row_data)
        
        # Use the primary key column value to generate a unique Redis key
        primary_key_value = row_data[primary_key]
        redis_key = f"{table_name}:{primary_key_value}"
        
        # Store row data as a Redis hash
        redis_client.hset(redis_key, mapping=row_data)
        print(f"Imported {redis_key} to Redis")

def main():
    try:
        # Connect to MySQL
        mysql_connection = mysql.connector.connect(**mysql_config)
        cursor = mysql_connection.cursor()

        # List of tables in the `sakila` database with their primary keys
        tables = {
            'actor': 'actor_id',
            'address': 'address_id',
            'category': 'category_id',
            'city': 'city_id',
            'country': 'country_id',
            'customer': 'customer_id',
            'film': 'film_id',
            'film_actor': 'actor_id',  # Composite primary keys are handled differently
            'film_category': 'film_id',
            'inventory': 'inventory_id',
            'language': 'language_id',
            'payment': 'payment_id',
            'rental': 'rental_id',
            'staff': 'staff_id',
            'store': 'store_id'
        }

        # Import each table
        for table_name, primary_key in tables.items():
            print(f"Importing table {table_name}...")
            import_table_to_redis(cursor, table_name, primary_key)

    except Error as e:
        print("Error while connecting to MySQL or importing data:", e)

    finally:
        # Close MySQL connection
        if mysql_connection.is_connected():
            cursor.close()
            mysql_connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    main()
