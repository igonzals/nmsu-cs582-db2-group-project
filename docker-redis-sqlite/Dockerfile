# Use Redis Stack image
FROM redis/redis-stack

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3

# Install Python3
RUN apt-get install -y python3

# Install python3 sql3 library and redis-py library
RUN apt-get install -y python3-pip
RUN pip3 install redis
RUN pip3 install sqlite3

# Install pandas library and plotly library
RUN pip3 install pandas
RUN pip3 install plotly

# Disable Redis persistence
RUN sed -i 's/appendonly yes/appendonly no/' /etc/redis/redis.conf

# Expose Redis port
EXPOSE 6379

# Expose SQLite port (optional)
EXPOSE 8001
