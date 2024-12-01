from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

# Fonction pour exécuter le producteur Kafka
def kafka_producer():
    subprocess.run(["python", "kafka_producer.py"])

# Fonction pour exécuter le consommateur Kafka dans Spark
def kafka_consumer_spark():
    subprocess.run(["python", "kafka_consumer_spark.py"])

# Fonction pour exécuter l'insertion dans Neo4j
def insert_neo4j():
    subprocess.run(["python", "insert_neo4j.py"])

# Fonction pour démarrer Streamlit
def start_streamlit():
    subprocess.run(["python", "run", "streamlit_app.py"])

# Définir le DAG
with DAG(
    'graph_processing_pipeline',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2024, 11, 30),
    },
    schedule_interval=None,  # Déclenchement manuel
    catchup=False,
) as dag:

    # Définir les tâches
    task_kafka_producer = PythonOperator(
        task_id='kafka_producer',
        python_callable=kafka_producer,
    )

    task_kafka_consumer_spark = PythonOperator(
        task_id='kafka_consumer_spark',
        python_callable=kafka_consumer_spark,
    )

    task_insert_neo4j = PythonOperator(
        task_id='insert_neo4j',
        python_callable=insert_neo4j,
    )

    task_start_streamlit = PythonOperator(
        task_id='start_streamlit',
        python_callable=start_streamlit,
    )

    # Définir l'ordre d'exécution
    task_kafka_producer >> task_kafka_consumer_spark >> task_insert_neo4j >> task_start_streamlit