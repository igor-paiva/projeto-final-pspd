import os
import sys
import signal
import discord
from kafka import KafkaProducer
from kafka.errors import KafkaError


def sigint_handler(*_):
    print("\n\nExiting...")
    sys.exit(0)


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    try:
        producer = KafkaProducer(bootstrap_servers=["kafka-server:9092"])

        producer.send("sentences", message.content.encode("utf-8"))
    except KafkaError as e:
        print(e)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)

    token = os.environ.get("BOT_TOKEN", None)

    if token is None:
        print("You must add the bot token to the environment variable BOT_TOKEN")

        sys.exit(0)

    client.run(token)
