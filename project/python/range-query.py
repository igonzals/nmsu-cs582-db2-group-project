import redis
import sqlite3
import time
from redis.commands.search.query import Query

# Path to the SQLite database file
db_path = "/mnt/data/sakila.db"

# Function to set up an in-memory SQLite database from a disk backup
def setup_sqlite_memory():
    disk_conn = sqlite3.connect(db_path)
    mem_conn = sqlite3.connect(":memory:")
    disk_conn.backup(mem_conn)
    disk_conn.close()
    return mem_conn

# Define Redis and SQLite queries
redis_query = '@inventory_id:[100 5000] @rental_id:[100 5000] @staff_id:[1 1]'
sqlite_query = """
SELECT customer_id 
FROM rental 
WHERE inventory_id BETWEEN 100 AND 5000 
AND rental_id BETWEEN 100 AND 5000 
AND staff_id = 1;
"""

# Function to execute the Redis query and measure time
def time_redis_query():
    # Establish the Redis connection once
    r = redis.StrictRedis(host='localhost', port=6379)
    
    # Measure only the query execution time
    start_time = time.time()
    query = Query(redis_query).return_fields("customer_id")
    r.ft("rentalIndex").search(query)
    end_time = time.time()
    
    r.close()  # Close the Redis connection after the query
    # print(end_time - start_time)
    return end_time - start_time

# Function to execute the SQLite query and measure time
def time_sqlite_query():
    # Establish the SQLite connection once and load data into memory
    mem_conn = setup_sqlite_memory()
    cursor = mem_conn.cursor()
    
    # Measure only the query execution time
    start_time = time.time()
    cursor.execute(sqlite_query)
    cursor.fetchall()
    end_time = time.time()
    
    mem_conn.close()  # Close the SQLite connection after the query
    # print(end_time - start_time)
    return end_time - start_time

# Run Redis query 5 times and calculate the average time
redis_times = [time_redis_query() for _ in range(5)]
avg_redis_time = sum(redis_times) / len(redis_times)

# Run SQLite query 5 times and calculate the average time
sqlite_times = [time_sqlite_query() for _ in range(5)]
avg_sqlite_time = sum(sqlite_times) / len(sqlite_times)

# Display the results
print(f"Average Redis Query Time: {avg_redis_time:.5f} seconds")
print(f"Average SQLite Query Time: {avg_sqlite_time:.5f} seconds")
