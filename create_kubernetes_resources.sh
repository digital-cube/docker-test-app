#!/bin/bash
set -e

kubectl apply -f kubernetes/db-deployment.yaml
kubectl apply -f kubernetes/db-service.yaml

kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/frontend-service.yaml

kubectl apply -f kubernetes/app-deployment.yaml
kubectl apply -f kubernetes/app-service.yaml

