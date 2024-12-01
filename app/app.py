from flask import Flask, jsonify
from kafka import KafkaConsumer
import json
import threading
import queue
import logging
import traceback

app = Flask(__name__)

# Créer une file d'attente pour stocker les messages Kafka
message_queue = queue.Queue()

# Configurer le consommateur Kafka
logging.basicConfig(level=logging.INFO)  # Réduire la quantité de logs affichés, en fixant le niveau à INFO

# Configurer le consommateur Kafka
def consume_kafka():
    try:
        consumer = KafkaConsumer(
            'api-topic',
            bootstrap_servers='broker:9092',  # Adresse pour les conteneurs Docker
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=None,  # Ajouter un group ID
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        logging.info("Consommateur connecté à Kafka.")
        for message in consumer:
            # logging.debug(f"Message reçu depuis Kafka : {message.value}")  # Garder les logs DEBUG ici si nécessaire pour un suivi détaillé
            message_queue.put(message.value)
            # logging.info(f"Nombre de messages dans la file après ajout : {message_queue.qsize()}")
    except Exception as e:
        logging.error(f"Erreur dans le consommateur Kafka : {e}")
        traceback.print_exc()

# Démarrer le thread Kafka
thread = threading.Thread(target=consume_kafka, daemon=True)
thread.start()

@app.route('/graph', methods=['GET'])
def get_graph_data():
    messages = []
    logging.info(f"Nombre de messages dans la file: {message_queue.qsize()}")
    while not message_queue.empty() and len(messages) < 10:
        message = message_queue.get()
        logging.debug(f"Message récupéré: {message}")  # Garder ce log au besoin, sinon vous pouvez le supprimer
        messages.append(message)
    logging.info(f"Messages envoyés à la réponse: {messages}")
    if not messages:
        logging.warning("Aucun message dans la file.")
    return jsonify(messages)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)