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
# RUN apt-get install -y mariadb-server mariadb-client

# Expose ports
EXPOSE 6379   
EXPOSE 8001   

# Set root password for MariaDB
# ENV MYSQL_ROOT_PASSWORD=root

# Start Redis and MariaDB services
CMD []