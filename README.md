# Simple test service

### Table of conent

## Introducion

The goal of this project is to describe the procedure for running a simple microservice-oriented project written in Python, along with its frontend written in Angular and Vanilla JS.

The first step is to describe and run the program using docker-compose.

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

1. Bootstrapping host virtual machine

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

2. Login to VM and install docker / docker-compose and this project

for example IP of this machine is 10.135.18.221
```bash
ssh root@10.135.18.221
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

Install Docker 

More details about this installation you can find on https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

```bash
apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt-cache policy docker-ce
sudo apt install docker-ce -y
```

Add user to docker group
```bash
usermod -aG docker user
```

Install docker compose

Docker compose plugin will be installed on users account

more details about this installation you can find at https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04

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

### Install and run application
```
su - users
git clone https://github.com/digital-cube/docker-test-app.git
cd docker-test-app

```
```

docker compose build
docker compose up -d
```

you can find log in logs/app/

also you should be able to access to web application using browser at

http://10.135.18.221:8080
