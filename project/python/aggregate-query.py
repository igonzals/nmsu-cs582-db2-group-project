import redis
import sqlite3
import time
from functools import reduce

from redis.commands.search.field import NumericField
import redis.commands.search.reducers as reducers
import redis.commands.search.aggregation as aggregations


def redis_indexed_aggregate_query(num_queries):
  # Get execution time in format yyyy-mmm-dd hh:mm:ss
  execution_group_time = time.strftime("%Y-%b-%d %H:%M:%S")
  r = redis.Redis(host='localhost', port=6379, decode_responses=True)
  try:
    r.ft("paymentindex").create_index([NumericField("amount")])
    print("Index created successfully.")
  except Exception as e:
    print(e)

  r.close()

  print(f"Average runtime of {num_queries:,} queries:")
  runtimes = []
  for _ in range(num_queries):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    start_time = time.time()
    req = aggregations.AggregateRequest("*").group_by([], reducers.avg('amount').alias("avg_amount"))
    r.ft("paymentindex").aggregate(req)
    runtimes.append(time.time() - start_time)
  redis_avg_time = sum(runtimes) / len(runtimes)
  print(f"  Average Runtime: {redis_avg_time:.5f} seconds in Redis")
  with open("../data/runtimes-group.tsv", "a") as f:
    f.write(f"{execution_group_time}\tRedis\tAggregation\t{num_queries}\t{redis_avg_time:.5f}\n")
  return redis_avg_time


def redis_aggregate_query (num_queries):
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
  return redis_avg_time

def sql_aggregate_query(num_queries):
  # Get execution time in format yyyy-mmm-dd hh:mm:ss
  execution_group_time = time.strftime("%Y-%b-%d %H:%M:%S")
  # SQLite
  runtimes = []
  for _ in range(num_queries):
    conn = sqlite3.connect('/mnt/data/sakila.db')
    cursor = conn.cursor()
    start_time = time.time()
    cursor.execute("SELECT AVG(amount) FROM payment")
    sql_avg = cursor.fetchone()
    runtimes.append(time.time() - start_time)
    conn.close()
  sql_avg_time = sum(runtimes) / len(runtimes)
  print(f"  Average Runtime: {sum(runtimes) / len(runtimes):.5f} seconds in SQLite")
  with open("../data/runtimes-group.tsv", "a") as f:
    f.write(f"{execution_group_time}\tSQLite\tAggregation\t{num_queries}\t{sql_avg_time:.5f}\n")
  return sql_avg_time

print()
print("Redis vs SQLite")
print("aggregate queries by key")
print("===================\n")
query_counts = [10, 100, 1000] 
for count in query_counts:
  redis_indexed_aggregate_query(count)
  # redis_aggregate_query(count)
  sql_aggregate_query(count)
print()
