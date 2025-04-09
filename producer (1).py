import tweepy
from kafka import KafkaProducer
import json
import time

# Twitter API credentials
BEARER_TOKEN = "Your-Bearer-Token"

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

# Authenticate Twitter API
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_tweets():
    query = "#AI OR #Tech -is:retweet"  # Search for tweets with these hashtags, excluding retweets
    tweets = client.search_recent_tweets(query=query, tweet_fields=["created_at", "text", "id"], max_results=10)

    if tweets.data:
        for tweet in tweets.data:
            tweet_data = {
                "id": tweet.id,
                "text": tweet.text,
                "timestamp": str(tweet.created_at)
            }
            producer.send("twitter-stream", value=tweet_data)  # Send to Kafka
            print(f"Tweet sent: {tweet_data}")

# Run every 30 seconds to fetch new tweets
while True:
    fetch_tweets()
    time.sleep(30)  # Wait before fetching again
