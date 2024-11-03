# Use Redis Stack image
FROM redis/redis-stack

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3

# Install Python3
RUN apt-get install -y python3

# Install pip and redis-py library for python3
RUN apt-get install -y python3-pip
RUN pip3 install redis

# Install pandas library and plotly library
RUN pip3 install pandas
RUN pip3 install plotly

# Expose Redis port
EXPOSE 6379

# Expose SQLite port (optional)
EXPOSE 8001

CMD []
