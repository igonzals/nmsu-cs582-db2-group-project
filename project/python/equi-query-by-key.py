import redis
import sqlite3
import time
import random

def queries_by_key (num_queries):

  print(f"Average runtime of {num_queries:,} queries:")

  customer_id = random.randint(1, 100)

  # Get execution time in format yyyy-mmm-dd hh:mm:ss
  execution_group_time = time.strftime("%Y-%b-%d %H:%M:%S")

  # Redis
  runtimes = []
  for i in range(1, num_queries):
    r = redis.StrictRedis(host='localhost', port=6379)
    start_time = time.time()
    first_name = r.hget("customer:" + str(customer_id), "first_name")
    end_time = time.time()
    duration = end_time - start_time
    runtimes.append(duration)
    r.close()
  print(f"  Average Runtime: {sum(runtimes) / len(runtimes):.5f} seconds in Redis")
  with open("../data/runtimes-group.tsv", "a") as f:
    f.write(f"{execution_group_time}\tRedis\tEquality\t{num_queries}\t{sum(runtimes) / len(runtimes):.5f}\n")

  # SQLite
  runtimes = []
  for i in range(1, num_queries):
    conn = sqlite3.connect('../data/sakila.db')
    cursor = conn.cursor()
    start_time = time.time()
    cursor.execute("SELECT first_name FROM customer WHERE customer_id = ?", (customer_id,))
    first_name = cursor.fetchone()[0]
    end_time = time.time()
    duration = end_time - start_time
    runtimes.append(duration)
    conn.close()
  print(f"  Average Runtime: {sum(runtimes) / len(runtimes):.5f} seconds in SQLite")
  with open("../data/runtimes-group.tsv", "a") as f:
    f.write(f"{execution_group_time}\tSQLite\tEquality\t{num_queries}\t{sum(runtimes) / len(runtimes):.5f}\n")

print()
print("Redis vs SQLite")
print("Equi queries by key")
print("===================\n")
query_counts = [10, 100, 1000]  
for count in query_counts:
  queries_by_key(count)
print()
