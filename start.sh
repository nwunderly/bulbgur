git pull
docker build . --tag bulbgur:latest

docker run -d \
 --network prod \
 -p 127.0.0.1:9001:9000 \
 --name bulbgur_static \
 -v $PWD/logs/static:/bulbgur/logs \
 -v $PWD/data:/bulbgur/data \
 -v $PWD/assets:/bulbgur/assets \
 --restart unless-stopped \
 bulbgur static

docker run -d \
 --network prod \
 -p 127.0.0.1:9000:9000 \
 --name bulbgur_main \
 -v $PWD/logs/static:/bulbgur/logs \
 -v $PWD/data:/bulbgur/data \
 --restart unless-stopped \
 bulbgur main

docker run -d \
 --network prod \
 -p 127.0.0.1:9004:9000 \
 --name bulbgur_bb \
 -v $PWD/logs/bb:/bulbgur/logs \
 -v $PWD/bb:/bulbgur/bb \
 --restart unless-stopped \
 bulbgur bb