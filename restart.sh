# docker network create redis_network

# docker stop tg_bot redis_DB
# docker rm tg_bot redis_DB
docker compose stop
docker compose down

docker compose up --build -d
docker exec -it tg_bot bash
# docker exec -it tg_bot bash
