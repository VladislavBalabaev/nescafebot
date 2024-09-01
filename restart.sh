docker compose stop
docker compose down

docker container prune
docker image prune
docker system prune -a --volumes

docker compose build #--no-cache
docker compose up --detach
docker exec -it tg_bot bash