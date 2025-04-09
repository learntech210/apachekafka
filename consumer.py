from kafka import KafkaConsumer
import json
import requests

# Elasticsearch endpoint
ELASTICSEARCH_URL = "http://localhost:9200/twitter/_doc/"

# Kafka Consumer
consumer = KafkaConsumer(
    "twitter-stream",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Listening for tweets...")

for message in consumer:
    tweet = message.value
    print(f"Received tweet: {tweet}")

    # Send tweet to Elasticsearch
    response = requests.post(ELASTICSEARCH_URL, json=tweet)
    print(f"Elasticsearch response: {response.json()}")

