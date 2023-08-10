#!/bin/bash
set -e

kubectl delete -f kubernetes/db-deployment.yaml
kubectl delete -f kubernetes/db-service.yaml

kubectl delete -f kubernetes/frontend-deployment.yaml
kubectl delete -f kubernetes/frontend-service.yaml

kubectl delete -f kubernetes/app-deployment.yaml
kubectl delete -f kubernetes/app-service.yaml

