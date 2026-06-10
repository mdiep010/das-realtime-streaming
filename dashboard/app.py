import streamlit as st
import psycopg2
import pandas as pd
import os

st.title("Project Dashboard")
st.write("Visualize data!")

# TO DO: Add connection to postgres and visualizations

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)

# Query data
query = "SELECT * FROM predictions ORDER BY created_at DESC LIMIT 20;"
df = pd.read_sql(query, conn)

# Show data
st.subheader("Latest Data")
st.dataframe(df)