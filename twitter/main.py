import os
import sys
import time
import signal
import requests
from kafka import KafkaProducer
from kafka.errors import KafkaError


API_ENDPOINT = "https://api.twitter.com/2"


def sigint_handler(*_):
    print("\n\nExiting...")
    sys.exit(0)


def get_bearer_token():
    return os.environ.get("TWITTER_API_TOKEN", None)


def recent_tweets():
    headers = {
        "Authorization": f"Bearer {get_bearer_token()}",
        "User-Agent": "TwitterAPIEssential",
    }

    request = requests.get(
        f"{API_ENDPOINT}/tweets/search/recent?query=(%23meme)lang%3Aen&tweet.fields=created_at",
        headers=headers,
    )

    request.raise_for_status()

    return request.json()


def tweet_message(tweet_data):
    return tweet_data["text"]


def get_tweets_messages(tweets_response):
    return list(map(tweet_message, tweets_response["data"]))


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)

    token = os.environ.get("TWITTER_API_TOKEN", None)

    if token is None:
        print("You must add the token to the environment variable TWITTER_API_TOKEN")

        sys.exit(0)

    while True:
        try:
            tweets = get_tweets_messages(recent_tweets())

            print("\n\n", tweets, "\n\n")

            producer = KafkaProducer(bootstrap_servers=["kafka-server:9092"])

            for tweet in tweets:
                producer.send("sentences", tweet.encode("utf-8"))

            time.sleep(5)
        except KafkaError as e:
            print(e)
            break
