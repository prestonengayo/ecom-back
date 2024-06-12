#!/bin/bash

# Variables
PUBLIC_IP=$(curl -H Metadata:true "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01&format=text")

echo "Mise à jour du système et installation de Docker, Git, Nginx"
sudo apt-get update
sudo apt-get install -y docker.io git nginx

echo "Installation de Docker Compose"
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "Vérification de l'installation de Docker Compose"
docker-compose --version

echo "Ajout de l'utilisateur azureuser au groupe docker"
sudo usermod -aG docker azureuser

echo "Clonage du dépôt Git"
git clone https://github.com/prestonengayo/ecom-back.git

echo "Déplacement dans le dossier du projet"
cd ecom-back

echo "Mise à jour des paquets et installation de dos2unix"
sudo apt-get update
sudo apt-get install -y dos2unix

echo "Conversion du fichier entrypoint.sh"
sudo dos2unix entrypoint.sh

echo "Rendre le fichier entrypoint.sh exécutable"
chmod +x entrypoint.sh

echo "Lancement des services avec Docker Compose en définissant ALLOWED_HOSTS"
sudo ALLOWED_HOSTS=$PUBLIC_IP docker-compose up -d

echo "Génération du certificat auto-signé"
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj "/CN=$PUBLIC_IP"

echo "Création du fichier de paramètres Diffie-Hellman"
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

echo "Création du fichier de configuration Nginx pour HTTP"
sudo bash -c "cat > /etc/nginx/sites-available/ecommerce <<EOF
server {
    listen 80;
    server_name $PUBLIC_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF"

echo "Activation de la configuration Nginx"
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
sudo systemctl start nginx
sudo systemctl enable nginx

echo "Création du fichier de configuration Nginx pour HTTPS"
sudo bash -c "cat > /etc/nginx/sites-available/ecommerce-ssl <<EOF
server {
    listen 443 ssl;
    server_name $PUBLIC_IP;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256';
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF"

echo "Activation de la configuration Nginx pour HTTPS"
sudo ln -s /etc/nginx/sites-available/ecommerce-ssl /etc/nginx/sites-enabled/
sudo systemctl restart nginx

echo "Script terminé"
