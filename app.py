from database import check_and_initialize_database, initialize_database
from apiclient.discovery import build
# from youtube import fetch_and_save_transcript
from config import YOUTUBE_API_KEY, HAMZA_CHANNEL_ID
from youtube import extract_video_id_from_url, get_video_data_by_url, get_video_upload_date_by_url, get_video_id, get_channel_videos, get_video_title, get_video_url, get_video_transcription, get_video_description, get_video_upload_date, get_video_id_from_data


youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# videos = get_channel_videos(HAMZA_CHANNEL_ID, youtube)

# print(f"Total videos fetched: {len(videos)}")

#przyklad dla wideo Hubermana jakiegos
video_url = 'https://www.youtube.com/watch?v=qNzl12g0Dd8'

# print(get_video_transcription(video_url))

# print('######################## ID ########################')
video_id = get_video_id_from_data(video_url)
title = get_video_title(video_url)
description = get_video_description(video_url)
url = video_url
upload_date = get_video_upload_date_by_url(video_url)

# print(get_video_id_from_data(video_url))
# print('######################## TITLE ########################')
# print(get_video_title(video_url))
# print('######################## DESCRIPTION ########################')
# print(get_video_description(video_url))
# print('######################## URL ########################')
# print(video_url)
# print('######################## UPLOAD DATE ########################')
# print(get_video_upload_date_by_url(video_url))

# print(get_video_data_by_url(video_url))
# initialize_database()

check_and_initialize_database()

# db_manager.is_video_in_database(extract_video_id_from_url(video_url))
# print(db_manager.get_video_description(video_url))

