import redis
import sqlite3
import time
import random

def queries_by_key (num_queries):

  print(f"Average runtime of {num_queries:,} queries:")

  customer_id = random.randint(1, 100)

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

print()
print("Redis vs SQLite")
print("Equi queries by key")
print("===================\n")
queries_by_key(1000)
print()
