# Group Project - Redis and SQLite Comparison

## Installation with Docker

First, install the [Docker engine](https://docs.docker.com/engine/install/) in your Operating System. 

Then, proceed with the following steps:

1. Clone this Github project. You need authorization since it is a private repository:
```
git clone nmsu-cs582-db2-group-project
```
2. Build Redis image (check you have Docker running first in your machine)
```
cd docker-redis-sqlite
docker build -t redis-sqlite-python .
```
3. Run Redis (without persistance) container mounting the data shared folder:
```
docker run -d \
  --name redis-sqlite-container \
  -p 6379:6379 \
  -p 8001:8001 \
  -v /Users/israelgonzalez/Documents/Development/nmsu/nmsu-cs582-db2-group-project/project:/mnt \
  redis-sqlite-python redis-server --appendonly no

```

You must replace "/Users/israelgonzalez/Documents/Development/nmsu/nmsu-cs582-db2-group-project/project" with your own path in your machine according you cloned the repo and have the "project" folder.
4. Now, we will check Redis is answering correcty making a Redis PING:
(Note: Previously make sure you have installed redis-cli in your machine, and then go to your console and run the following command)
```
redis-cli -h 127.0.0.1 -p 6379 ping
```
You should see the following output: 
```
PONG
```
5. Now, we will check that SQLite is answering correctly:
```
docker exec -it redis-sqlite-container python3 /mnt/python/install/test-sqlite.py
```
You should see:
```
(1, 'SQLite is well!')
```
If SQLite answers correctly

Important: For the following steps make sure you put manually the files of the Sakila database in folder "data":

6. Now, we will install the Sakila database in SQLite and in Redis by executing:

```
docker exec -it redis-sqlite-container python3 /mnt/python/install/install-sakila.py
```


This has been built with help of ChatGpt and minor adaptations. You can check the thread here: 
  
https://chatgpt.com/share/67244d75-9498-8004-9b31-6ca261d83adc