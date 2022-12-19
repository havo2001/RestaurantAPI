# RestaurantAPI
This is a simple API REST for a restaurant website

## Git clone:
First you need to git clone this repository:
```git clone git@github.com:havo2001/RestaurantAPI.git```
## Run API using docker: (You have to install docker first)
1. ```docker compose up --build```
2. Open another terminal, run ```docker ps```, now you can see the ```CONTAINER ID``` of the two images: ```restaurantapi-app```, ```postgres:13-alpine```.
3. Run command ```docker exec -it "CONTAINER ID" //bin//sh``` ( where CONTAINER ID is the container id of ```restaurantapi-app```)
4. Here the shell was opened, then run command ```flask db migrate```, ```flask db upgrade```
5. Go to the ```localhost:5000``` and then the docker container is working now
