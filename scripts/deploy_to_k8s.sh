#!/bin/bash


echo "Creating the volume..."

kubectl apply -f ../kubernetes/persistent-volume.yml
kubectl apply -f ../kubernetes/persistent-volume-claim.yml


echo "Creating the database credentials..."

kubectl apply -f ../kubernetes/secret.yml


echo "Creating the postgres deployment and service..."

kubectl create -f ../kubernetes/postgres-deployment.yml
kubectl create -f ../kubernetes/postgres-service.yml



echo "Creating the flask deployment and service..."

kubectl create -f ../kubernetes/flask-deployment.yml
kubectl create -f ../kubernetes/flask-service.yml

