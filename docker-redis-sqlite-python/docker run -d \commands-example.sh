# To build and run the container as a service, execute the following commands:
docker build -t redis-sqlite-python .
docker run -d \
  --name redis-sqlite-container \
  -p 6379:6379 \
  -p 8001:8001 \
  -v /home/kraken2/songlab/igonzalez/db2/nmsu-cs582-db2-group-project/project:/mnt:rw \
  redis-sqlite-python redis-server --dir /mnt/data --dbfilename dump.rdb --protected-mode no --appendonly no --loadmodule /opt/redis-stack/lib/redisearch.so --loadmodule /opt/redis-stack/lib/redistimeseries.so --loadmodule opt/redis-stack/lib/rejson.so --loadmodule /opt/redis-stack/lib/redisbloom.so

# To run the container as a interactive shell, execute the following command:
docker exec -it redis-sqlite-container /bin/bash