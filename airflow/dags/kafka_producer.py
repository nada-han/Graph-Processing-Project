from kafka import KafkaProducer
import pandas as pd
import json
import numpy as np



# Configurer le producteur Kafka
producer = KafkaProducer(
    bootstrap_servers='broker:9092',
    value_serializer=lambda v: json.dumps(v, default=lambda x: x.tolist() if isinstance(x, (np.ndarray, pd.Series)) else x).encode('utf-8')
)

# Charger le dataset Parquet
df = pd.read_parquet('proteins-train.parquet')

# Diffuser les données dans Kafka
for idx, row in df.iterrows():
    result = producer.send('api-topic', value=row.to_dict())
    print(f"Message {idx} envoyé, résultat : {result}")
    
print("Dataset envoyé à Kafka.")
producer.close()