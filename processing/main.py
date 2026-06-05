import os
from confluent_kafka import Consumer
import psycopg2
import json 
from dotenv import load_dotenv

load_dotenv()

def make_prediction(temp, windspeed, weathercode):
    if temp is None:
        return "unknown"

    if weathercode is not None and weathercode >= 50:
        return "rainy"
    elif temp > 30 and windspeed is not None and windspeed > 20:
        return "hot and windy"
    elif temp > 30:
        return "hot"
    elif temp < 0:
        return "freezing"
    elif temp < 10:
        return "cold"
    elif windspeed is not None and windspeed > 25:
        return "windy"
    elif temp < 20:
        return "mild"
    else:
        return "normal"

def clean_data(data):
    temperature = float(data.get("temperature")) if data.get("temperature") is not None else None
    windspeed = float(data.get("windspeed")) if data.get("windspeed") is not None else None
    winddirection = int(data.get("winddirection")) if data.get("winddirection") is not None else None
    weathercode = int(data.get("weathercode")) if data.get("weathercode") is not None else None

    return {
        "temperature": temperature,
        "windspeed": windspeed,
        "winddirection": winddirection,
        "weathercode": weathercode,
        "weather_time": data.get("time"),
        "prediction": make_prediction(temperature, windspeed, weathercode)
    }

def main():
    print("Processing service started...")
    
    consumer = Consumer({
        "bootstrap.servers": "localhost:19092",
        "group.id": "weather-consumer-group",
        "auto.offset.reset": "earliest"
    })
    consumer.subscribe(["weather"])

    conn = psycopg2.connect(
    host="localhost",
    database="project_db",
    user="username",
    password="password"
    )

    cur = conn.cursor()

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print("Consumer error:", msg.error())
                continue

            raw = msg.value().decode("utf-8")
            data = json.loads(raw)

            cleaned = clean_data(data)

            print("Received message:")
            print(data)
            cur.execute("""
                INSERT INTO predictions 
                (temperature, windspeed, winddirection, weathercode, weather_time, prediction)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                cleaned["temperature"],
                cleaned["windspeed"],
                cleaned["winddirection"],
                cleaned["weathercode"],
                cleaned["weather_time"],
                cleaned["prediction"]
            ))

            conn.commit()
            print("Inserted into database")

    except KeyboardInterrupt:
        print("Stopping consumer...")

    finally:
        consumer.close()

if __name__ == "__main__":
    main()