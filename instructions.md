# 1. How to use Dockerfile

#### 1.1. You have to install docker by yourself.
#### 1.2. You should be in your venv where you have NESCAFEBOT_TOKEN, to do that:

> \$ python -m venv venv_bot
> \$ nano venv_bot/bin/activate

at the end of the file place (instead of _token_ place actual token):
> \> export NESCAFEBOT_TOKEN="_token_"

then activate it:
> \$ source venv_bot/bin/activate

then build an image:
> \$ docker build --tag nescafebot --build-arg name=$NESCAFEBOT_TOKEN .

to run the image within a container
> \> docker run -it nescafebot

to be sure that your token has been passed:
> \> echo $NESCAFEBOT_TOKEN

to exit the container: 
> \> exit