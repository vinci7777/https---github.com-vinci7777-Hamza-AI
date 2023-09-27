from database import check_and_initialize_database, initialize_database
from apiclient.discovery import build
# from youtube import fetch_and_save_transcript
from config import YOUTUBE_API_KEY, HAMZA_CHANNEL_ID
from youtube import extract_video_id_from_url, get_video_data_by_url, get_video_upload_date_by_url, get_video_id, get_channel_videos, get_video_title, get_video_url, get_video_transcription, get_video_description, get_video_upload_date, get_video_id_from_data

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

video_url = 'https://www.youtube.com/watch?v=qNzl12g0Dd8'

video_id = get_video_id_from_data(video_url)
title = get_video_title(video_url)
description = get_video_description(video_url)
url = video_url
upload_date = get_video_upload_date_by_url(video_url)

check_and_initialize_database()
get_channel_videos(HAMZA_CHANNEL_ID, youtube)


