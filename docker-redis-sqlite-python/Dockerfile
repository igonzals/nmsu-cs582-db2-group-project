FROM redis/redis-stack-server:latest


# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 wget

# Install Python3
RUN apt-get install -y python3

# Install pip and redis-py library for python3
RUN apt-get install -y python3-pip
RUN pip3 install redis
RUN pip3 install mysql-connector-python
RUN pip3 install sqlparse

# Install MariaDB and dependencies
RUN apt-get install -y mariadb-server mariadb-client

# Expose ports
EXPOSE 6379   
EXPOSE 8001   
EXPOSE 3307   

# Set root password for MariaDB
ENV MYSQL_ROOT_PASSWORD=root

# Start Redis and MariaDB services
CMD ["redis-server", "--loadmodule", "/opt/redis-stack/lib/redisearch.so", "--loadmodule", "/opt/redis-stack/lib/redistimeseries.so", "--loadmodule", "/opt/redis-stack/lib/rejson.so", "--loadmodule", "/opt/redis-stack/lib/redisbloom.so"]


# How to use this Dockerfile (uncomment the following lines)

# docker build -t redis-sqlite-python .

# docker run -d \
#   --name redis-sqlite-container \
#   -p 6379:6379 \
#   -p 8001:8001 \
#   -p 3306:3307 \
#   -v /Users/israelgonzalez/Documents/Development/nmsu/nmsu-cs582-db2-group-project/project:/mnt \
#   redis-sqlite-python \
#   bash -c "service mariadb start && redis-server --dir /mnt/data --dbfilename dump.rdb --protected-mode no --appendonly no --loadmodule /opt/redis-stack/lib/redisearch.so"

# docker exec -it redis-sqlite-container /bin/bash
