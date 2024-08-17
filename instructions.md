# 1. How to use bot via docker:

#### 1.1. You have to install docker by yourself.
#### 1.2. You should create .env file in main directory and supply it with:
> \> NESCAFEBOT_TOKEN = "_token_"
> \> REDIS_PASSWORD = "_token_"
> \> REDIS_ABSOLUTE_PATH = "_token_"

#### 1.3. Run docker container:
First, start docker:
> \$ sudo systemctl start docker

(At this stage you should be in directory with compose.yaml [use 'cd'])   
Build an image:
> \$ docker compose up --build -d

Run the image in interactive mode within a container:
> \$ docker run -it tg_bot bash

#### 1.4 Start the bot:
> \$ python bot/start_bot.py

#### 1.5 Finish work:
To exit the container:
> \> exit

> \$ docker compose stop
> \$ docker compose down