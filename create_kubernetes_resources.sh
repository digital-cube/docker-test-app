#!/bin/bash
set -e

kubectl delete secret secret-envs --ignore-not-found
kubectl create secret generic secret-envs --from-env-file=.env

kubectl apply -f kubernetes/db-deployment.yaml
kubectl apply -f kubernetes/db-service.yaml

kubectl apply -f kubernetes/app-deployment.yaml
kubectl apply -f kubernetes/app-service.yaml

kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/frontend-service.yaml