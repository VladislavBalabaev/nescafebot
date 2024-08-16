docker network create redis_network

docker stop tg_bot
docker rm tg_bot
docker stop redis_DB
docker rm redis_DB

docker build --tag nescafebot -f Dockerfile.py .
docker run -it --name tg_bot -d --net redis_network -p 8880:8880 nescafebot bash

source .env

docker run --name redis_DB -p 6379:6379 -d --net redis_network -v redis.conf:$REDIS_ABSOLUTE_PATH redis redis-server --requirepass $REDIS_PASSWORD

docker exec tg_bot bash -c "python bot/tester.py"