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
        print("Adding missing videos to the database...")
    else:
        print("No new videos found!")

# Define the time you want to run the job (e.g., 10:00 AM)
desired_time = "16:45"

# Schedule the job to run at the desired time
schedule.every().day.at(desired_time).do(job)

# Run the scheduler in a loop
while True:
    schedule.run_pending()
    time.sleep(1)