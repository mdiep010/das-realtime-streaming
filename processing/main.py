import os
from confluent_kafka import Consumer
#import psycopg2
import json 
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Processing service started...")
    
    consumer = Consumer({
        "bootstrap.servers": "localhost:19092",
        "group.id": "weather-consumer-group",
        "auto.offset.reset": "earliest"
    })
    consumer.subscribe(["weather"])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print("Consumer error:", msg.error())
                continue

            data = json.loads(msg.value().decode("utf-8"))

            print("Received message:")
            print(data)

    except KeyboardInterrupt:
        print("Stopping consumer...")

    finally:
        consumer.close()

if __name__ == "__main__":
    main()