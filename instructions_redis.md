#### 1. First of all, we need to make a docker file redis. Let name it: 'redis_test':
> docker run --name _redis_test_ -d redis

To check, that you run a docker file, write:
> docker image ls

#### 2. Make a network in docker and name it: 'redis_network'.
> docker network create -d bridge _redis_network_ 

To check, that you have a docker network, write:
> docker network ls

#### 3. Connect to the docker network via docker container:

> docker network connect _redis_network_ _CONTAINER_ID_

With everything working as expected, the next step is to verify your Redis server running inside Docker is ready to accept connections. To do so, use:
> docker logs

#### 4. Next, you must create a database because you need a way to connect to the Redis container to run commands on the server. To do this, type:
> docker exec -it _CONTAINER_ID_ bash

#### 5. In the container, use the CLI to run commands. Note that Redis automatically installed Docker hosts. To use the Redis-CLI, type:
> redis-cli

To check, that you are connected to redis, type:
> ping

You should have:
> PONG

#### 6. Well, you have connected to the server and you can do whatever you want! Don't forget to use command _MONITOR_ for checking changes:
> MONITOR


#### 7. To close all, you should do exit from redis-cli, using command:
> exit 

#### Also, leave from bash:
> exit 

#### Finally, stop the Redis container from running by typing:
> docker stop _CONTAINER_ID_
> docker network rm _redis_network_



