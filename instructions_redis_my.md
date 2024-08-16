#### 1. First of all, we need to make a docker file redis. Let name it: '_redis_test_':
> docker run --name redis_DB -d redis

#### 1.1 If you want to create redis server with your configurations on _redis.conf_ use this command:
> docker run --name redis_DB -v redis.conf:/c/Users/madfu/Documents/big_projects/redis.conf -d redis

## To check, that you run a docker file, write:
> docker ps -a

#### 2. Make a network in docker and name it: '_redis_network_'.
> docker network create -d bridge redis_network

To check, that you have a docker network, write:
> docker network ls

#### 3. Connect to the docker network via docker container:

> docker network connect redis_network redis_DB

With everything working as expected, the next step is to verify your Redis server running inside Docker is ready to accept connections. To do so, use:
> docker logs

#### 4. Next, you must create a database because you need a way to connect to the Redis container to run commands on the server. To do this, type:
> docker exec -it redis_DB sh

#### 5. In the container, use the CLI to run commands. Note that Redis automatically installed Docker hosts. To use the Redis-CLI, type:
> redis-cli

To check, that you are connected to redis, type:
> ping

You should have:
> PONG

#### 5. If you want to make a security password for your new database, type this command:
> config set requirepass boris_redis

#### Then, exit from the redis-cli and reconnect to it. You will see, that you don't have a permission for your databse:
> exit
> redis_cli
> keys *
Redis: (error) NOAUTH Authentication required.

#### To get a permission, you should make authentication:
> auth boris_redis
#### Congratulation, you have an access to database!

#### 6. Well, you have connected to the server and you can do whatever you want! Don't forget to use command _MONITOR_ for checking changes:
> MONITOR

#### 7. To close all, you should do exit from redis-cli, using command:
> exit 

## Also, leave from container:
> exit 

## 8. Finally, stop the Redis container from running by typing:
> docker stop redis_DB
> docker network rm redis_network


#### FUCK THIS GUIDE ABOVE! THREE EASY STEPS NAHUI:

#### 1. Created docker network. It will be used to bridge docker containers!
> docker network create redis_netowrk

#### 2. Make a docker container of Redis database with name redis_DB, port 8880, configuration redis.conf, connected to redis_network!
> docker run --name redis_DB --net redis_network -p 80:8880 -v redis.conf:/c/Users/madfu/Documents/big_projects/redis.conf -d redis

#### 3. Make a docker container of telegram bot with name tg_bot, port 8888, connected to redis_network!

> docker run -it --name tg_bot -d --net redis_network -p 79:8888 nescafebot bash

