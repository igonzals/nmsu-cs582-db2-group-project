import redis
import sqlite3
import time
from redis.commands.search.query import Query
from redis.commands.search.field import NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

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
    
    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    # Create index if it doesn't exist
    try:
        r.ft("rentalIndex").create_index(
            [
                NumericField("rental_id"),
                NumericField("inventory_id"),
                NumericField("customer_id"),
                NumericField("staff_id")
            ],
            definition=IndexDefinition(prefix=["rental:"], index_type=IndexType.HASH)
        )
    except redis.exceptions.ResponseError as e:
        if "Index already exists" in str(e):
            # print("Index already exists")
            a = 1
        else:
            print(f"An error occurred: {e}")
            exit()

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

# Get execution time in format yyyy-mmm-dd hh:mm:ss
execution_group_time = time.strftime("%Y-%b-%d %H:%M:%S")
query_counts = [10, 100, 1000]

for count in query_counts:
    # Run Redis query query_counts times and calculate the average time
    redis_times = [time_redis_query() for _ in range(count)]
    avg_redis_time = sum(redis_times) / len(redis_times)
    print(f"Average Redis Query Time ({count} queries): {avg_redis_time:.5f} seconds")
    with open("../data/runtimes-group.tsv", "a") as f:
        f.write(f"{execution_group_time}\tRange-query\tRedis\t{avg_redis_time}\n")

    # Run SQLite query query_counts times and calculate the average time
    sqlite_times = [time_sqlite_query() for _ in range(count)]
    avg_sqlite_time = sum(sqlite_times) / len(sqlite_times)
    print(f"Average SQLite Query Time ({count} queries): {avg_sqlite_time:.5f} seconds")
    with open("../data/runtimes-group.tsv", "a") as f:
        f.write(f"{execution_group_time}\tRange-query\tSQLite\t{avg_sqlite_time}\n")

