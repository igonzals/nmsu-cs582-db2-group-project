import redis
import sqlite3
import time
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

query_text = "Action"

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Create an index on Redis if it doesn't exist
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

# SQLite setup
conn = sqlite3.connect('/data/sakila.db')
cursor = conn.cursor()

# Regular Table Setup in SQLite
cursor.execute("DROP TABLE IF EXISTS film_regular")
cursor.execute("CREATE TABLE film_regular AS SELECT title, description FROM film")
conn.commit()

# FTS5 Virtual Table Setup in SQLite
cursor.execute("DROP TABLE IF EXISTS film_fts")
cursor.execute("CREATE VIRTUAL TABLE film_fts USING fts5(title, description)")
cursor.execute("INSERT INTO film_fts (title, description) SELECT title, description FROM film")
conn.commit()

# SQLite full-text search function using regular table
def sqlite_regular_search(query_text):
    cursor.execute("SELECT title, description FROM film_regular WHERE title LIKE ? OR description LIKE ?", 
                   (f"%{query_text}%", f"%{query_text}%"))
    return cursor.fetchall()

# SQLite full-text search function using virtual table
def sqlite_fts_search(query_text):
    cursor.execute("SELECT title, description FROM film_fts WHERE film_fts MATCH ?", (query_text,))
    return cursor.fetchall()

# Function to run queries multiple times and calculate average time
def measure_query_time(query_function, query_text, num_iterations):
    runtimes = []
    for _ in range(num_iterations):
        start_time = time.time()
        query_function(query_text)
        runtimes.append(time.time() - start_time)
    return sum(runtimes) / len(runtimes)

# Test query time with increasing query counts
query_counts = [1, 10, 100, 1000,10000]   

print("Testing Redis, SQLite (Regular Table), and SQLite (VIRTUAL TABLE) query times:\n")

for count in query_counts:
    redis_time = measure_query_time(redis_full_text_search, query_text, count)
    sqlite_regular_time = measure_query_time(sqlite_regular_search, query_text, count)
    sqlite_fts_time = measure_query_time(sqlite_fts_search, query_text, count)

    print(f"For {count} queries:")
    print(f"  Redis Average Query Time: {redis_time:.5f} seconds")
    print(f"  SQLite (Regular Table) Average Query Time: {sqlite_regular_time:.5f} seconds")
    print(f"  SQLite (VIRTUAL TABLE) Average Query Time: {sqlite_fts_time:.5f} seconds\n")

# Close SQLite connection
conn.close()
