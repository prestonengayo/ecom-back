# Utiliser l'image Python officielle
FROM python:3.12.3

# Install Dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Définir le répertoire de travail dans le conteneur
WORKDIR /code

# Ajouter les fichiers de dépendances et installer ces dépendances
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers du projet
COPY . /code/

# Copier le script d'entrée
COPY entrypoint.sh /code/entrypoint.sh

# Rendre le script exécutable
RUN chmod +x /code/entrypoint.sh

# Exposer le port sur lequel l'application va écouter
EXPOSE 8000

# Commande pour démarrer l'application
ENTRYPOINT ["/code/entrypoint.sh"]
