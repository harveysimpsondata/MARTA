import requests
import json
from config import api_key, k
import time
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer

bootstrap_servers=k.get('kafka').get('bootstrap_servers')
sasl_username=k.get('kafka').get('sasl_username')
sasl_password=k.get('kafka').get('sasl_password')

def on_delivery(err, msg):
    if err:
        print(f'Message failed delivery: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

#Set up Kafka producer
producer_conf = {
    'bootstrap.servers': bootstrap_servers,
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': sasl_username,
    'sasl.password': sasl_password,
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': StringSerializer('utf_8')
}

producer = SerializingProducer(producer_conf)

try:
    while True:
        try:
            #Fetch data
            marta_trains_url = f"https://developerservices.itsmarta.com:18096/railrealtimearrivals?apiKey={api_key}"
            response = requests.get(marta_trains_url, verify=False)
            data = response.json()['RailArrivals']
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f'Error fetching or parsing data: {e}')
            time.sleep(10)
            continue

        #Send data to Kafka
        for item in data:
            producer.produce(topic='marta-train-topic', key=str(item['TRAIN_ID']), value=json.dumps(item), on_delivery=on_delivery)

        # Wait for all messages to be delivered
        producer.flush()

        # Wait 2.5 second
        time.sleep(2.5)

#Catch Ctrl-C
except KeyboardInterrupt:
    print('Flushing producer and exiting...')
    producer.flush()
