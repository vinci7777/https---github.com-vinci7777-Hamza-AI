from database import check_and_initialize_database
from youtube import fetch_and_save_transcript

# Initialize the database when the application starts
check_and_initialize_database()

# Example usage to fetch and save a YouTube video's transcript
video_url = 'https://www.youtube.com/watch?v=qNzl12g0Dd8&t=1s'
fetch_and_save_transcript(video_url)