# Use Redis Stack image
# FROM redis/redis-stack:latest
FROM redis/redis-stack-server:latest

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 wget

# Install Python3
RUN apt-get install -y python3

# Install pip and redis-py library for python3
RUN apt-get install -y python3-pip
RUN pip3 install redis

# Install pandas, plotly, and sqlparse libraries
# RUN pip3 install pandas plotly sqlparse

# Expose Redis port
EXPOSE 6379

# Expose SQLite port (optional)
EXPOSE 8001

# Start the Redis server with Redis Stack modules enabled
CMD []

# How to use this Dockerfile
# docker build -t redis-sqlite-python .

# Host port 6380 mapped to container port 6379

# docker run -d \
#   --name redis-sqlite-container \
#   -p 6379:6379 \
#   -p 8001:8001 \
#   -v /Users/israelgonzalez/Documents/Development/nmsu/nmsu-cs582-db2-group-project/project:/mnt \
#   redis-sqlite-python redis-server --dir /mnt/data --dbfilename dump.rdb --protected-mode no --appendonly no --loadmodule /opt/redis-stack/lib/redisearch.so

# redis-cli FT.CREATE idx SCHEMA name TEXT age NUMERIC
# docker exec -it redis-sqlite-container /bin/bash
