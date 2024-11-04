# Here code the creation and import of database Sakila 
# In Redis and in SQLite

import sqlite3
import redis
import json
import sqlparse
import os
# Complete create databases and import ../../data/redis_data.json (Zheng Cui)


# Define file paths
schema_path = "/mnt/data/sakila-db/sakila-schema.sql"
data_path = "/mnt/data/sakila-db/sakila-data.sql"
db_path = "/mnt/data/sakila.db"

# Create or connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def execute_sql_file(filepath):
    """Read SQL file and execute all SQL statements"""
    with open(filepath, 'r') as file:
        sql_content = file.read()
        # Use sqlparse to split the SQL file content into individual statements
        statements = sqlparse.split(sql_content)
        for statement in statements:
            # Skip empty statements
            if statement.strip():
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"Error executing statement: {statement}")
                    print(f"Error message: {e}")

# Execute schema file and data file
print("Importing schema...")
execute_sql_file(schema_path)
print("Schema imported successfully.")

print("Importing data...")
execute_sql_file(data_path)
print("Data imported successfully.")

# Commit changes and close connection
conn.commit()
conn.close()
print("Database setup completed successfully.")
