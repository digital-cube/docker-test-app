#!/bin/bash
set -e

kubectl delete secret secret-envs --ignore-not-found

kubectl delete -f kubernetes/db-deployment.yaml --ignore-not-found
kubectl delete -f kubernetes/db-service.yaml --ignore-not-found

kubectl delete -f kubernetes/frontend-deployment.yaml --ignore-not-found
kubectl delete -f kubernetes/frontend-service.yaml --ignore-not-found

kubectl delete -f kubernetes/app-deployment.yaml --ignore-not-found
kubectl delete -f kubernetes/app-service.yaml --ignore-not-found

