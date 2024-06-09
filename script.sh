#!/bin/bash

# Mise à jour et installation de Docker et Git
sudo apt-get update
sudo apt-get install -y docker.io git

# Installer Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Vérifier l'installation de Docker Compose
docker-compose --version

# Ajouter l'utilisateur azureuser au groupe docker
sudo usermod -aG docker azureuser

# Cloner le dépôt
git clone https://github.com/prestonengayo/ecom-back.git

# Se déplacer dans le dossier du projet
cd ecom-back

# S'assurer que le fichier entrypoint.sh est exécutable
chmod +x entrypoint.sh

# Récupérer l'adresse IP publique via les métadonnées d'Azure
PUBLIC_IP=$(curl -H Metadata:true "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01&format=text")

# Lancer les services avec Docker Compose en définissant ALLOWED_HOSTS
sudo ALLOWED_HOSTS=$PUBLIC_IP docker-compose up -d
