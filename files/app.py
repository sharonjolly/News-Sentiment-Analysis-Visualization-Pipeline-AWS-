from dotenv import load_dotenv
load_dotenv()

import os
import psycopg2
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Must be the first Streamlit command
st.set_page_config(page_title="News Sentiment Dashboard", layout="wide")

# Auto-refresh every 5 minutes (300,000 milliseconds)
st_autorefresh(interval=5 * 60 * 1000, key="newsdatarefresh")

st.title("📰 News Sentiment Dashboard")

# Cache and fetch data from PostgreSQL
@st.cache_data(ttl=300, show_spinner="Fetching latest news...")
def fetch_news_data():
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            dbname=os.getenv("PG_DATABASE"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD")
        )
        query = """
            SELECT title, description, source_name, published_at, sentiment_label
            FROM news_sentiment
            ORDER BY published_at DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return pd.DataFrame()

# Load data
df = fetch_news_data()

if not df.empty:
    # Format timestamp
    df['published_at'] = pd.to_datetime(df['published_at']).dt.strftime('%Y-%m-%d %H:%M')

    # Style function for sentiment column
    def highlight_sentiment(val):
        color = {
            'positive': 'lightgreen',
            'negative': '#ff9999',
            'neutral': 'lightgray'
        }.get(str(val).lower(), 'white')
        return f'background-color: {color}; color: black; font-weight: bold'

    # Apply style to the sentiment column
    styled_df = df.style.applymap(highlight_sentiment, subset=['sentiment_label'])

    # Display styled dataframe
    st.dataframe(styled_df, use_container_width=True, height=600)

else:
    st.info("No data available.")
