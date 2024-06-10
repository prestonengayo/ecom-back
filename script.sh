#!/bin/bash

echo "Mise à jour du système et installation de Docker, Git, Nginx, et Certbot"
sudo apt-get update
sudo apt-get install -y docker.io git nginx certbot python3-certbot-nginx

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

echo "Récupération de l'adresse IP publique via les métadonnées d'Azure"
PUBLIC_IP=$(curl -H Metadata:true "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01&format=text")

echo "Lancement des services avec Docker Compose en définissant ALLOWED_HOSTS"
sudo ALLOWED_HOSTS=$PUBLIC_IP docker-compose up -d

echo "Configuration de Nginx pour HTTP"
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

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
}
EOF"

echo "Activation de la configuration Nginx"
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
sudo systemctl restart nginx

echo "Obtention du certificat SSL"
sudo certbot --nginx -d $PUBLIC_IP --non-interactive --agree-tos --email your-email@example.com

echo "Configuration de Nginx pour rediriger HTTP vers HTTPS"
sudo bash -c "cat > /etc/nginx/sites-available/ecommerce <<EOF
server {
    listen 80;
    server_name $PUBLIC_IP;

    location / {
        return 301 https://\$host\$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name $PUBLIC_IP;

    ssl_certificate /etc/letsencrypt/live/$PUBLIC_IP/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$PUBLIC_IP/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF"

echo "Redémarrage de Nginx pour appliquer les modifications"
sudo systemctl restart nginx

echo "Script terminé"
