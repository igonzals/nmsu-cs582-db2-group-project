import redis
import sqlite3
import time
from functools import reduce


def aggregate_query (num_queries):

  print(f"Average runtime of {num_queries:,} queries:")

  # Redis
  runtimes = []
  for _ in range(num_queries):
    r = redis.StrictRedis(host='localhost', port=6379) 
    start_time = time.time()
    payment_ids = r.keys('payment:*') # get keys first 
    pipe = r.pipeline()
    for payment_id in payment_ids:
        pipe.hget(payment_id, "amount")
    amounts = list(pipe.execute())
    redis_avg = reduce(lambda a, b: float(a) + float(b), amounts) / len(amounts)
    runtimes.append(time.time() - start_time)
    r.close()
  redis_avg_time = sum(runtimes) / len(runtimes)
  print(f"  Average Runtime: {redis_avg_time:.5f} seconds in Redis")

  # SQLite
  runtimes = []
  for _ in range(num_queries):
    conn = sqlite3.connect('../data/sakila.db')
    cursor = conn.cursor()
    start_time = time.time()
    cursor.execute("SELECT AVG(amount) FROM payment")
    sql_avg = cursor.fetchone()
    runtimes.append(time.time() - start_time)
    conn.close()
  
  sql_avg_time = sum(runtimes) / len(runtimes)
  print(f"  Average Runtime: {sum(runtimes) / len(runtimes):.5f} seconds in SQLite")
  return redis_avg_time, sql_avg_time

print()
print("Redis vs SQLite")
print("aggregate queries by key")
print("===================\n")
aggregate_query(100)
print()
