import requests
import time
import json
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()

# Redpanda producer
p = Producer({"bootstrap.servers": "localhost:19092"})

def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 33.9533,
        "longitude": -117.3962,
        "current_weather": True
    }

    return requests.get(url, params=params).json()

def main():
    print("Ingestion service started...")

    while True:
        data = fetch_weather()

        payload = data.get("current_weather")

        if payload:
            p.produce(
                topic="weather",
                value=json.dumps(payload),
            )

            p.poll(0)
            print("Sent data to redpanda")

        else:
            print("No weather data found")

        time.sleep(10)
        p.flush()

if __name__ == "__main__":
    main()
