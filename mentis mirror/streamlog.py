import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Mentis Mirror Logs Viewer", layout="wide")

# Display logo
st.image("logo.png", width=100)  # Adjust width if needed

# Title
st.title(" Mentis Mirror – Logs Viewer")

# Database connection config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "survi09mukh",  # Update this if needed
    "database": "mentis_mirror"
}

# Connect to MySQL database
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    st.success("✅ Connected to Mentis Mirror database!")
except mysql.connector.Error as err:
    st.error(f"❌ Database connection failed: {err}")
    st.stop()

# Fetch logs
cursor.execute("SELECT * FROM mirror_logs ORDER BY timestamp DESC")
logs = cursor.fetchall()

if not logs:
    st.info("ℹ️ No logs found in the database.")
    st.stop()

# Convert logs to DataFrame
df = pd.DataFrame(logs)

# Complete emotion list
all_possible_emotions = ["happy", "sad", "angry", "surprise", "fear", "disgust", "neutral"]

# Sidebar Filters
with st.sidebar:
    st.header("📅 Filter Logs")

    # Emotion filter
    selected_emotions = st.multiselect("Select emotions:", all_possible_emotions, default=all_possible_emotions)
    df = df[df["emotion"].isin(selected_emotions)]

    # Date range filter
    date_range = st.date_input("Select date range:", [])
    if len(date_range) == 2:
        start_date = datetime.combine(date_range[0], datetime.min.time())
        end_date = datetime.combine(date_range[1], datetime.max.time())
        df = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)]

# Emotion to Emoji mapping
emotion_emoji_map = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "surprise": "😲",
    "fear": "😨",
    "disgust": "🤢",
    "neutral": "😐"
}

# Show logs
st.subheader(f"📋 Showing {len(df)} log(s)")
for _, row in df.iterrows():
    emotion = row["emotion"]
    emoji = emotion_emoji_map.get(emotion.lower(), "😊")
    with st.expander(f"🕒 {row['timestamp']} | {emoji} {emotion.capitalize()}"):
        st.markdown(f"🧠 **Emotion**: `{row['emotion']}`")

        st.markdown(f"🌡️ **Temperature**: `{row['temperature']} °C`" if pd.notna(row.get("temperature")) else "🌡️ **Temperature**: `N/A`")
        st.markdown(f"🔊 **Sound Level**: `{row['sound']} dB`" if pd.notna(row.get("sound")) else "🔊 **Sound Level**: `N/A`")
        st.markdown(f"🧪 **TVOC**: `{row['tvoc']} ppb`" if pd.notna(row.get("tvoc")) else "🧪 **TVOC**: `N/A`")
        st.markdown(f"🫁 **CO₂ Level**: `{row['co2']} ppm`" if pd.notna(row.get("co2")) else "🫁 **CO₂ Level**: `N/A`")

# Close DB connection
cursor.close()
conn.close()
st.markdown("""
    <a href="http://localhost:8502/mentis_mirror_app.py" target="_self">
        <button style='font-size:18px;padding:8px 16px;border-radius:10px;background:#6c63ff;color:white;border:none;cursor:pointer;'>📊 Back to Home Page </button>
    </a>
""", unsafe_allow_html=True)
