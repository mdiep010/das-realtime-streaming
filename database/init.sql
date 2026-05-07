CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    temperature FLOAT,
    windspeed FLOAT,
    winddirection FLOAT,
    weathercode INT,
    weather_time TEXT,
    prediction TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TO DO: Update table schema