import requests
import time
import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

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
    temperature_c = float(data.get("temperature")) if data.get("temperature") is not None else None
    windspeed = float(data.get("windspeed")) if data.get("windspeed") is not None else None
    winddirection = int(data.get("winddirection")) if data.get("winddirection") is not None else None
    weathercode = int(data.get("weathercode")) if data.get("weathercode") is not None else None

    temperature_f =  (temperature_c * 9/5 + 32) if temperature_c is not None else None
    
    return {
        "temperature": temperature_f,
        "windspeed": windspeed,
        "winddirection": winddirection,
        "weathercode": weathercode,
        "weather_time": data.get("time"),
        "prediction": make_prediction(temperature_c, windspeed, weathercode)
    }

def fetch_weather(): #weather at UCR 
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 33.9737,
        "longitude": -117.3281,
        "current_weather": True
    }
    return requests.get(url, params=params).json()

def connect_db(): #supabase connection 
    return psycopg2.connect(DB_URL)

def main():
    print("Ingestion started to Supabase...")

    conn = connect_db()
    cur = conn.cursor()

    while True:
        data = fetch_weather()
        payload = data.get("current_weather")

        if not payload:
            print("No data")
            continue 

        cleaned = clean_data(payload)

        prediction = make_prediction(
            cleaned["temperature"],
            cleaned["windspeed"],
            cleaned["weathercode"])

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
            prediction
        ))

        conn.commit()
        print("Inserted into Supabase")

        time.sleep(10)

if __name__ == "__main__":
    main()