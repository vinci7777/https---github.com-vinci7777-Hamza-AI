from helper import save_missing_videos_to_database
from youtube import get_channel_videos
import schedule
import time
import streamlit as st

st.title('Hamza-AI')

def job():
    videos = get_channel_videos() 
    if videos:
        save_missing_videos_to_database()

# Run the scheduler in a loop
schedule.every().day.do(job)

# Run the scheduler in a loop
while True:
    schedule.run_pending()
    time.sleep(1)