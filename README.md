# RestaurantAPI
This is a simple API REST for a restaurant website

## Git clone:
First you need to git clone this repository:
```git clone git@github.com:havo2001/RestaurantAPI.git```
## Run API using docker: (You have to install docker first) (These commands are working for Windows, for other OS you should figure them yourself)
1. ```docker compose up --build```
2. Open another terminal, run ```docker ps```, now you can see the ```CONTAINER ID``` of the two images: ```restaurantapi-app```, ```postgres:13-alpine```.
3. Run command ```docker exec -it "CONTAINER ID" //bin//sh``` ( where CONTAINER ID is the container id of ```restaurantapi-app```)
4. Here the shell was opened, then run command ```flask db migrate```, ```flask db upgrade```
5. Go to the ```localhost:5000``` and then the docker container is working now
## Run API using Kubernetes:
### Kubernetes:
1. First you should have ```minikube``` working in your computer.
2. ```minikube start``` to start minikube, ```minikube dashboard``` to open the dashboard
3. ```kubectl apply -f .\kubernetes\postgres-deployment.yaml ```
4. ```kubectl apply -f kubernetes/api-deployment.yaml ```
5. ```kubectl get pod``` to show the pods, and copy the name of "api-deployment"
6. ```kubectl exec -it "api-deployment"  //bin//sh``` to open the shell
7. ```flask db upgrade```
8. ```exit```
9. ```minikube service api-service ``` and then it will work

