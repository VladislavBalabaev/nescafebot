# 1. How to launch bot:

#### 1.1. You should create .env file in main directory and supply it with:
> \> NESCAFEBOT_TOKEN = "_token_"  
> \> MONGODB_USERNAME = "..."  
> \> MONGODB_PASSWORD = "..."  
> \> MONGODB_ABSOLUTE_PATH = "/../"  
> \> EMAIL_PASSWORD = "..."  


#### 1.2. Run docker compose:
First, start docker:
> \$ sudo systemctl start docker
   
Docker compose images and network between them:
> \$ docker compose build #--no-cache 
> \$ docker compose up --detach


#### 1.3. Start the bot:
Enter running container of bot in interactive mode:
> \$ docker exec -it tg_bot bash

> \$ python bot/start_bot.py

If the bot takes forever to launch:

1) check if your proxies are correct
> \$ env | grep -i proxy

2) check if you have access to telegram's API:
> \$ curl -I https://api.telegram.org  
> \$ ping api.telegram.org  


#### 1.4. Finish work:
To exit the container:
> \> exit

> \$ docker compose stop  
> \$ docker compose down  


#### If you use VPN:
In compose.yaml comment out network settings and bring back **network_mode: 'host'**.