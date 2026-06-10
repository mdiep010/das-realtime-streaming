import os
import psycopg2
import pandas as pd
import streamlit as st

st.title("Project Dashboard")
st.write("Weather Data from UCR!")

conn = psycopg2.connect(os.environ["DATABASE_URL"])

query = """
SELECT * FROM predictions
ORDER BY created_at DESC
LIMIT 20;
"""

df = pd.read_sql(query, conn)

st.subheader("Latest Data")
st.dataframe(df)