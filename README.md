# Group Project - Redis and SQLite

## Installation with Docker

First, install docker in your Operating System. You can follow the instructions in the following link: https://docs.docker.com/get-docker/

Then, proceed with the following steps:

1. Clone this Github project. You need authorization since it is a private repository:
```
git clone nmsu-cs582-db2-group-project
```
2. Build Redis image
```
docker build -t redis-server .
```
3. Run Redis container mounting the data shared folder:
```
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest -v /mnt/nmsu-cs582-db2-group-project/project:/mnt/project:rw
```
4. Previously installing redis-cli in your Operating system, go to console and run the following command:
```
redis & PING
```
5. You should see the following output: PONG

Useful information in: 
  
https://chatgpt.com/share/67244d75-9498-8004-9b31-6ca261d83adc