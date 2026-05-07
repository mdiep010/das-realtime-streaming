import streamlit as st
import psycopg2
import pandas as pd
import os

st.title("Project Dashboard")
st.write("Visualize data!")

# TO DO: Add connection to postgres and visualizations

conn = psycopg2.connect(
    host="postgres",
    database="project_db",
    user="username",
    password="password"
)

# Query data
query = "SELECT * FROM predictions ORDER BY created_at DESC LIMIT 20;"
df = pd.read_sql(query, conn)

# Show data
st.subheader("Latest Data")
st.dataframe(df)