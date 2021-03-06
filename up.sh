git pull
docker build . --tag bulbgur:latest

docker run -d \
 --network prod \
 -p 127.0.0.1:9000:9000 \
 --name bulbgur_main \
 -v $PWD/data:/bulbgur/data \
 --restart unless-stopped \
 bulbgur main

docker run -d \
 --network prod \
 -p 127.0.0.1:9001:9000 \
 --name bulbgur_static \
 -v $PWD/data:/bulbgur/data \
 --restart unless-stopped \
 bulbgur static

docker run -d \
 --network prod \
 -p 127.0.0.1:9002:9000 \
 --name bulbgur_bb_api \
 -v $PWD/leaderboard:/bulbgur/leaderboard \
 --restart unless-stopped \
 bulbgur bb_api