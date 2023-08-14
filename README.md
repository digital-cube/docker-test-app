# Simple test service

### Table of content

+ [Structure of the project](#structure-of-the-project)
+ [Installing project using_dockerhub](#installing-using-dockerhub)
+ [Installing project on empty virtual machine](#installing-project-on-empty-virtual-machine)
  - [Bootstrapping host virtual machine](#bootstrapping-host-virtual-machine)
  - [Login to VM and install docker / docker-compose and this project](#login-to-vm-and-install-docker---docker-compose-and-this-project)
  - [Install Docker](#install-docker)
  - [Add user to docker group](#add-user-to-docker-group)
  - [Install docker compose](#install-docker-compose)
  - [Install and run application](#install-and-run-application)


## Introduction

The goal of this project is to describe the procedure for running a simple microservice-oriented project written in Python, along with its frontend written in Angular and Vanilla JS.

The first step is to describe and run the program using docker-compose.

### Installing using dockerhub

The project described below can be installed without building Docker images, using pre-built images already pushed on DockerHub. To do this, you can follow the steps below:

Create a docker-compose.yaml file with the following content:

```yaml
services:

  db:
    restart: always
    image: postgres
    
    environment:
      - POSTGRES_USER=$POSTGRES_USER
      - POSTGRES_PASSWORD=$POSTGRES_PASSWORD
      - POSTGRES_DB=$POSTGRES_DB
  
  app:
    image: igorjeremic/testapp

    environment:
      - POSTGRES_HOST=db
      - POSTGRES_USER=$POSTGRES_USER
      - POSTGRES_PASSWORD=$POSTGRES_PASSWORD
      - POSTGRES_DB=$POSTGRES_DB

    depends_on:
      - db

    volumes:
      - ./logs:/var/log/app/

  nginx:
    image: igorjeremic/testnginx
    
    depends_on:
      - app

    ports:
      - $NGINX_EXPOSED_ON:80
```

Create a .env file and populate it with the following information:

```.env
NGINX_EXPOSED_ON=8822
POSTGRES_DB=db
POSTGRES_USER=app
POSTGRES_PASSWORD=xyz
```

Run the project by executing the following command in your terminal:

```bash
docker compose up -d
```

This command will start the containers in detached mode, meaning they will run in the background. The PostgreSQL database, the application container, and the Nginx container will be up and running, and the application should be accessible at http://localhost:8822.

### Structure of the project

- README.md  (this file)
- .env.sample (environment sample file, need to be copied and edited)
- Dockerfile.app (instructions for building app image)
- Dockerfile.nginx (instructions for building nginx image)
- docker-compose.yaml (docker compose configuration)
- config/nginx.conf (configuration for nginx)
- app/app.py (backend application)
- web/index.html (web application)

### Installing project on empty virtual machine

For documentation purposes, I am using DigitalOcean as the VM provider. However, please note that this procedure is almost the same for any other provider. I am also using the latest Ubuntu
LTS (at the moment, version 22.04) and providing instructions for Docker installation on this OS. The steps may vary slightly for other Unix systems, but the overall process remains similar.

#### Bootstrapping host virtual machine

To create a virtual machine on your DigitalOcean account, follow these steps:

- Sign in to your DigitalOcean account at https://www.digitalocean.com/.
- Once logged in, click on the "Create" button in the top-right corner of the dashboard.
- Select "Droplets" from the dropdown menu.
- In the "Choose an image" section, select "Distributions" tab and choose "Ubuntu 22.04 x64" as the operating system. This is the latest Ubuntu LTS version at the moment.
- In the "Choose a plan" section, select the smallest available machine size. For example, choose the one with 1 CPU, 1 GB RAM, and 25 GB SSD.
- In the "Add backups" and "Add block storage" sections, for this test, you can skip these options.
- In the "Choose a datacenter region" section, select the datacenter region closest to your location or the one that suits your needs.
- Under the "Select additional options" section you can leave default options.
- In the "Authentication" section, choose either an SSH key (if you have one) or a root password to access your virtual machine. SSH key-based authentication is more secure, so if you have an SSH key, it's recommended to use that.
- Finally, give your virtual machine a hostname or leave it as the default.
- Click on the "Create Droplet" button at the bottom of the page to start creating the virtual machine.
- DigitalOcean will now create your virtual machine with the specified configuration. Once the creation process is complete, 
- You can then access your virtual machine using SSH (or other methods) and proceed with the rest of the installation and setup for your microservice-oriented project.

#### Login to VM and install docker / docker-compose and this project

for example IP of this machine is aa.bb.cc.dd
```bash
ssh root@aa.bb.cc.dd
```

Update and upgrade your server to apply latest OS updates
```bash
apt update
apt upgrade
```

Create which will run service (let call him user in this test), add this user to sudoers

```bash
adduser user
usermod -a -G sudo user
```

#### Install Docker 

More details about this installation you can find at

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

```bash
apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt-cache policy docker-ce
sudo apt install docker-ce -y
```

#### Add user to docker group
```bash
usermod -aG docker user
```

#### Install docker compose

Docker compose plugin will be installed on users account

more details about this installation you can find at 

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04

```bash
su - user
mkdir -p ~/.docker/cli-plugins/
```

Fetch the latest version of Docker Compose to check which version is the most recent. You can visit https://github.com/docker/compose/releases/ to find the latest version. As of now, the latest version is v2.20.2. If a newer version is available, try with the newer one. Simply replace the version in the following CURL request.

```bash
curl -SL https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
```
To make this script executable, use the following command:

```bash
chmod +x ~/.docker/cli-plugins/docker-compose
```

#### Install and run application
```
git clone https://github.com/digital-cube/docker-test-app.git
cd docker-test-app
```

setup environments by copying and editing env file

In the .env file, set up the port, username, password, and database name, or leave them as default values. 

Remember not to push the .env file to .git as it contains specific installation credentials (this file is .gitignored)

```bash
cp .env.sample .env
```

Build docker images
```bash
docker compose build
```

Start docker images
```bash
docker compose up -d
```

follow logs in logs/app
```bash
tail -f logs/app.log
```
you can find log in logs/app/

also you should be able to access to web application using browser at

http://aa.bb.cc.dd:8822


---

# Deploying Application on Minikube

This guide will walk you through the process of setting up Minikube, installing necessary dependencies, and deploying an application on a Kubernetes cluster running locally via Minikube.

## Installation Steps

### 1. Install Dependencies

Before you install Minikube, ensure that you have `virtualbox` installed:

Ubuntu:
```bash
sudo apt update
sudo apt-get install virtualbox
```
[installation tutorial for macOS](https://www.virtualbox.org/wiki/Downloads)

### 2. Install Minikube

Ubuntu:
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb
```
[Installation tutorial for macOS](https://minikube.sigs.k8s.io/docs/start/)

### 3. Install kubectl

`kubectl` is a command-line tool for interacting with Kubernetes clusters. Download and install it:

Ubuntu:
```bash
snap install kubectl --classic
kubectl version --client
```
[Installation tutorial for macOS](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/)

### 4. Start Minikube

Initialize a Minikube cluster:

```bash
minikube start --driver=virtualbox
```

This will set up a single-node Kubernetes cluster on your local machine.

### 5. Deploying the Application

With Minikube running, you can create kubernetes resources using the script

```bash
./create_kubernetes_resources.sh
```

Check if resources are created and if pods are ready:

```bash
kubectl get pods
```


```bash
NAME                                   READY   STATUS    RESTARTS   AGE
app-deployment-6d9f8f7df7-ls5kx        1/1     Running   0          2m13s
frontend-deployment-6955cbf458-4zc5b   1/1     Running   0          2m12s
postgres-deployment-76c545898-bv799    1/1     Running   0          2m13s
```
if all pods have status "Running" application is ready, you can start it using the script

```bash
./start.sh
```

## Cleanup

To stop Minikube:

```bash
minikube stop
```

To delete the Minikube cluster:

```bash
minikube delete
```

## Conclusion

You've now set up Minikube and deployed an application on a local Kubernetes cluster. This setup is ideal for local development and testing. For production deployments, consider a managed Kubernetes service or a dedicated Kubernetes cluster.

---
