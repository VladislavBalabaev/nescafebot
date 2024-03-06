#### 1. First of all, we need to make a docker file redis. Let name it: '_redis_test_':
> docker run --name _redis_test_ -d redis

#### 1.1 If you want to create redis server with your configurations on _redis.conf_ use this command:
> docker run --name redis_DB -v _redis.conf_:_/absolute/path/to/your/redis_conf/redis.conf_ -d redis

To check, that you run a docker file, write:
> docker ps -a

#### 2. Make a network in docker and name it: '_redis_network_'.
> docker network create -d bridge _redis_network_ 

To check, that you have a docker network, write:
> docker network ls

#### 3. Connect to the docker network via docker container:

> docker network connect _redis_network_ _CONTAINER_ID_or_CONTAINER_NAME_

With everything working as expected, the next step is to verify your Redis server running inside Docker is ready to accept connections. To do so, use:
> docker logs _CONTAINER_ID_or_CONTAINER_NAME_

#### 4. Next, you must create a database because you need a way to connect to the Redis container to run commands on the server. To do this, type:
> docker exec -it _CONTAINER_ID_or_CONTAINER_NAME_ bash

#### 5. In the container, use the CLI to run commands. Note that Redis automatically installed Docker hosts. To use the Redis-CLI, type:
> redis-cli

To check, that you are connected to redis, type:
> ping

You should have:
> PONG

#### 5. If you want to make a security password for your new database, type this command:
> config set requirepass _your_password_

#### Then, exit from the redis-cli and reconnect to it. You will see, that you don't have a permission for your databse:
> exit
> redis_cli
> keys *
Redis: (error) NOAUTH Authentication required.

#### To get a permission, you should make authentication:
> auth _your_password_
#### Congratulation, you have an access to database!

#### Check again:
> keys *

#### 6. Well, you have connected to the server and you can do whatever you want! Don't forget to use command _MONITOR_ for checking changes:
> MONITOR

#### 7. To close all, you should do exit from redis-cli, using command:
> exit 

#### Also, leave from container:
> exit 

#### Finally, stop the Redis container from running by typing:
> docker stop _CONTAINER_ID_
> docker network rm _redis_network_



