import os
import psycopg2
import pandas as pd
import streamlit as st
import base64

def set_bg(image_path):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    encoded = base64.b64encode(img_bytes).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def weatherDecode(code):
    if code is None:
        return None
    if code == 0:
        return "Clear sky"
    elif code == 1:
        return "Mainly clear"
    elif code == 2:
        return "Partly cloudy"
    elif code == 3:
        return "Overcast"
    elif code == 21:
        return "Rain"
    elif code == 41:
        return "Fog"
    elif code == 48:
        return "Depositing rime fog"
    elif code == 50:
        return "Light drizzle"
    elif code == 60:
        return "Rain"
    elif code == 70:
        return "Snow"
    elif code == 80:
        return "Rain showers"
    elif code == 95:
        return "Thunderstorm"
    else:
        return "Unknown"

def degToDir(degrees):
    if degrees is None:
        return None
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return directions[round(degrees / 45) % 8]

st.title("ACM DAS Project Dashboard")
st.write("Weather Data from UCR!")

st.markdown("""
<style>     
.block-container {
    background-color: rgba(0, 0, 0, 0.55);
    margin-top: 2rem;
    padding: 2rem;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

set_bg("UCR_Aerial-0039-(1)-optimized.jpg")

conn = psycopg2.connect(os.getenv("DATABASE_URL"))

query = """
SELECT
    temperature,
    windspeed,
    winddirection,
    weathercode,
    weather_time,
    prediction,
    created_at
FROM predictions
ORDER BY created_at DESC
LIMIT 20;
"""

df = pd.read_sql(query, conn)

df = df.rename(columns={
    "temperature": "Temperature (F)",
    "windspeed": "Wind Speed (m/s)",
    "winddirection": "Wind Direction (°)",
    "weathercode": "Weather Code",
    "weather_time": "Weather Time",
    "prediction": "Prediction",
    "created_at": "Created"
})

df["Wind Direction (Cardinal)"] = df["Wind Direction (°)"].apply(degToDir)
df["Weather"] = df["Weather Code"].apply(weatherDecode)
df = df.drop(columns=["Weather Time"])

df = df[
    [
        "Temperature (F)",
        "Prediction",
        "Wind Speed (m/s)",
        "Wind Direction (°)",
        "Wind Direction (Cardinal)",
        "Weather",
        "Weather Code",
        "Created"
    ]
]

st.subheader("Latest Data")
st.dataframe(df)