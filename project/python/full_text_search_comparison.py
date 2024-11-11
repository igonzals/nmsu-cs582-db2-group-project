import redis
import sqlite3
import time
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

query_text = "Action"

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Create index if it doesn't exist
try:
    r.ft("filmIndex").create_index(
        [TextField("title", weight=1.0), TextField("description", weight=1.0)],
        definition=IndexDefinition(prefix=["film:"], index_type=IndexType.HASH)
    )
except redis.exceptions.ResponseError as e:
    if "Index already exists" in str(e):
        print("Index already exists")
    else:
        print(f"An error occurred: {e}")

# Redis full-text search function
def redis_full_text_search(query_text):
    query = f'@title|description:{query_text}'
    result = r.ft("filmIndex").search(query)
    return result

# SQLite  data setting
conn = sqlite3.connect('../data/sakila.db')  
cursor = conn.cursor()

# Create FTS5  insert data
cursor.execute("DROP TABLE IF EXISTS film_fts")
cursor.execute("CREATE VIRTUAL TABLE film_fts USING fts5(title, description)")
cursor.execute("INSERT INTO film_fts (title, description) SELECT title, description FROM film")
conn.commit()

# SQLite full-text search function
def sqlite_full_text_search(query_text):
    cursor.execute("SELECT title, description FROM film_fts WHERE film_fts MATCH ?", (query_text,))
    return cursor.fetchall()

# Function to run queries multiple times and calculate average time
def measure_query_time(system, query_function, query_text, num_iterations):
    runtimes = []
    for _ in range(num_iterations):
        start_time = time.time()
        query_function(query_text)
        duration = time.time() - start_time
        runtimes.append(duration)
    return sum(runtimes) / len(runtimes)

print("Testing Redis and SQLite query times with increasing iteration counts:\n")

# Test query time with increasing query counts 1 to 1000
query_counts = [10, 100, 1000]   

for num_queries in query_counts:
    execution_group_time = time.strftime("%Y-%b-%d %H:%M:%S")
    redis_time = measure_query_time("Redis", redis_full_text_search, query_text, num_queries)
    sqlite_time = measure_query_time("SQLite", sqlite_full_text_search, query_text, num_queries)
    print(f"For {num_queries} queries:")
    print(f"  Redis Average Query Time: {redis_time:.5f} seconds")
    print(f"  SQLite Average Query Time: {sqlite_time:.5f} seconds\n")
    with open("../data/runtimes-group.tsv", "a") as f:
        f.write(f"{execution_group_time}\tRedis\tFull-text\t{num_queries}\t{redis_time:.5f}\n")
        f.write(f"{execution_group_time}\tSQLite\tFull-text\t{num_queries}\t{sqlite_time:.5f}\n")

# Close SQLite connection
conn.close()
