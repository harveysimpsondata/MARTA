import requests
import json
from config import api_key, k
import pandas as pd
import requests
import json
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer


bootstrap_servers=k.get('kafka').get('bootstrap_servers')
sasl_username=k.get('kafka').get('sasl_username')
sasl_password=k.get('kafka').get('sasl_password')

# Step 1: Fetch data
marta_trains_url = f"https://developerservices.itsmarta.com:18096/railrealtimearrivals?apiKey={api_key}"
response = requests.get(marta_trains_url, verify=False)
data = response.json()['RailArrivals']

# Step 2: Set up Kafka producer
producer_conf = {
    'bootstrap.servers': bootstrap_servers,  # You can get these from your Confluent Cloud Dashboard
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': sasl_username,  # API key
    'sasl.password': sasl_password,  # API secret
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': StringSerializer('utf_8')
}

producer = SerializingProducer(producer_conf)


# Step 3: Send data to Kafka
for item in data:
    producer.produce(topic='marta-train-topic', key=str(item['TRAIN_ID']), value=json.dumps(item))

# Wait for all messages to be delivered
producer.flush()