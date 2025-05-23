

import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Connect to Google Sheet
SHEET_NAME = "Mood Tracker"
sheet = client.open(SHEET_NAME).sheet1

# Mood options
moods = {
    "😊": "Happy",
    "😠": "Frustrated",
    "😕": "Confused",
    "🎉": "Joyful"
}

st.title("Mood of the Queue")
st.write("Log and track the emotional vibe of the support queue.")

# Mood logger
st.header("Log a Mood")
selected_mood = st.radio("Select your mood:", list(moods.keys()), horizontal=True)
note = st.text_input("Optional note")
if st.button("Submit"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, selected_mood, note])
    st.success("Mood logged!")

# Mood visualization
st.header("Today's Mood Trend")
data = sheet.get_all_records()
df = pd.DataFrame(data,columns=['timestamp', 'mood', 'note'])
df["datetime"] = pd.to_datetime(df["timestamp"])
df["date"] = df["datetime"].dt.date

# Filter for today
today = date.today()
df_today = df[df["date"] == today]

if not df_today.empty:
    mood_counts = df_today["mood"].value_counts().reset_index()
    mood_counts.columns = ["mood", "count"]
    fig = px.bar(mood_counts, x="mood", y="count", title="Mood Count Today", labels={"count": "Number of Logs"})
    st.plotly_chart(fig)
else:
    st.info("No mood entries yet today.")
