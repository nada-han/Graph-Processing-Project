# **Projet Data Engineering : Traitement de graphe**

## **Description**
Ce projet implémente un pipeline de data engineering pour traiter un dataset de graphe. Il utilise les technologies suivantes :
- **Apache Kafka** : Pour la diffusion et la consommation des données.
- **Apache Spark GraphX** : Pour le traitement et l'analyse des graphes.
- **Neo4j** : Pour le stockage des résultats du traitement.
- **Streamlit** : Pour visualiser les résultats de manière interactive.
- **Apache Airflow** : Pour orchestrer l'ensemble du pipeline.

## **Architecture**
1. **Docker** :
   - L'ensemble des services nécessaires (Kafka, Spark, Neo4j, Airflow) est conteneurisé avec Docker Compose pour simplifier le déploiement.
   - Chaque service s'exécute dans son propre conteneur, assurant l'isolation et la portabilité.
     
2. **Kafka** :
   - Un producteur diffuse les données depuis un fichier Parquet dans un topic Kafka.
   - Un consommateur Kafka consomme ces données et les expose via une API Flask.

3. **Spark GraphX** :
   - Les données sont récupérées depuis Kafka et traitées dans Spark GraphX.
   - Les algorithmes de traitement sont : PageRank, Connected Components, Triangle Counting.

4. **Neo4j** :
   - Les résultats des traitements sont stockés dans Neo4j via des requêtes Cypher.

5. **Streamlit** :
   - Une interface interactive permet de visualiser les résultats depuis Neo4j.

6. **Airflow** :
   - Orchestration complète du pipeline pour une exécution automatisée.
  
![workflow](https://github.com/user-attachments/assets/613d7ce0-d545-4315-b37e-fc91b77f0518)

## **Prérequis**
- Docker et Docker Compose
- Python 3.8+
- Bibliothèques Python :
  - `pandas`, `flask`, `kafka-python`, `pyspark`

## **Installation**
1. **Cloner le dépôt** :
   - Clone le projet depuis le dépôt Git :
     ```bash
     git clone https://github.com/nada-han/Graph-Processing-Project.git
     cd Graph-Processing-Project
     ```

2. **Démarrer les services avec Docker Compose** :
   - Lance tous les conteneurs en arrière-plan :
     ```bash
     docker-compose up -d
     ```
3. **Accéder à l'application Streamlit** :
   - Ouvre un navigateur et accède à l'application Streamlit via l'URL suivante :
     ```
     http://localhost:8501
     ```
https://github.com/user-attachments/assets/543ce862-f615-4b0e-9639-83fb1b72d7a6
