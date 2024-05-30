#!/bin/sh

# Attendre que la base de données soit disponible
dockerize -wait tcp://db:3306 -timeout 120s

# Appliquer les migrations
python manage.py migrate

# Créer un super utilisateur si aucun n'existe
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gmail.com', 'adminpass');
"

# Démarrer le serveur
python manage.py runserver 0.0.0.0:8000
