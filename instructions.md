# 1. How to use bot via docker:

#### 1.1. You have to install docker by yourself.
#### 1.2. You should create .env file in main directory and supply it with _token_:
> \> NESCAFEBOT_TOKEN = "_token_"

#### 1.3. Run docker container:
First, start docker:
> \$ sudo systemctl start docker

(At this stage you should be in directory with the Dockerfile [use 'cd'])   
Build an image:
> \$ docker build --tag nescafebot -f Dockerfile.py .

Run the image in interactive mode within a container:
> \$ docker run -it nescafebot

#### 1.4 Start the bot:
> \$ python bot/start_bot.py

To exit the container:
> \> exit