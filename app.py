from helper import save_missing_videos_to_database
from youtube import get_channel_videos
import schedule
import time
import streamlit as st

st.title('Hamza-AI')

def job():
    print("Running a daily videos check job, please wait.")
    videos = get_channel_videos() 
    if videos:
        save_missing_videos_to_database()
        print("Addidng missing videos to database...")
    else:
        print("No new videos found!")

# Run the scheduler in a loop
schedule.every().day.do(job)

# Run the scheduler in a loop
while True:
    schedule.run_pending()
    time.sleep(1)