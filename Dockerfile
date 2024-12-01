# Utiliser une image Python officielle comme base
FROM python:3.8-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY app/requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source de l'application dans le conteneur
COPY app/ .

# Exposer le port 5000 pour l'application Flask
EXPOSE 5000

# Lancer l'application Flask
CMD ["python", "app.py"]