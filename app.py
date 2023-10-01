from helper import save_missing_videos_to_database
from youtube import get_channel_videos
import schedule
import time
import streamlit as st
import logging

st.title('Hamza-AI')

def job():
    logging.info("Running a daily videos check job, please wait.")
    try:
        videos = get_channel_videos() 
        if videos:
            save_missing_videos_to_database()
            logging.info("Adding missing videos to the database...")
        else:
            logging.info("No new videos found!")
    except Exception as e:
        logging.error(f"Error in job: {str(e)}")

# Define the time you want to run the job (e.g., 10:00 AM)
desired_time = "19:10"

# Schedule the job to run at the desired time
schedule.every().day.at(desired_time).do(job)

# Run the scheduler in a loop
while True:
    schedule.run_pending()
    time.sleep(1)