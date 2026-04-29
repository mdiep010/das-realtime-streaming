import requests # lets us talk to APIs
import time # allows a pause
import os
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Ingestion service started...")
    
    # TO DO: Add data source API connection
    url = "https://api.open-meteo.com/v1/forecast"     # Weather API 
    
    params = {
        "latitude": 33.9533,
        "longitude": -117.3962,
        "current_weather": True
    }

    while True:
        r = requests.get(url, params=params)

        if r.status_code == 200:
            print(r.json())
        else:
            print("Error:", r.status_code)

        time.sleep(10)
    # TO DO: Add redpanda connection

if __name__ == "__main__":
    main()
