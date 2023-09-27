from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY
import requests
import json
import os
import sqlite3
import urllib.parse as urlparse
from urllib.parse import parse_qs

def extract_video_id_from_url(url):
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    video_id = query["v"][0]
    return video_id

def get_channel_videos(channel_id, youtube):
    print("Gathering channel videos...")

    # File to store the video list
    file_path = 'channel_videos.json'

    # Initialize existing_videos as an empty list
    existing_videos = []

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            # Try to load the existing video list from the file
            with open(file_path, 'r') as file:
                existing_videos = json.load(file)
        except json.JSONDecodeError:
            # Handle the case where the file is empty or contains invalid JSON
            print("Error loading existing video list. Using an empty list instead.")

    res = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    uploads_playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    next_page_token = None

    while True:
        res = youtube.playlistItems().list(playlistId=uploads_playlist_id,
                                           part='snippet',
                                           pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    # Extract video IDs from the fetched videos
    new_video_ids = set(video['snippet']['resourceId']['videoId'] for video in videos)
    print(f"Number of videos in the list: {len(existing_videos)}")
    print(f"Number of videos gathered from the channel: {len(new_video_ids)}")

    # Check if the new video IDs are different from the existing ones
    if new_video_ids == set(existing_videos):
        print("Checking if there are any new videos...")
        print("NOTHING NEW ADDED!")
        print("Closing the gathering videos method.")
        return []

    print("Checking if there are any new videos...")
    print("NEW VIDEOS FOUND and added to the list!")

    # Update the existing video list with the new video IDs
    existing_videos = list(new_video_ids)
    print(f"Number of videos in the list: {len(existing_videos)}")

    # Save the updated video list to the file
    with open(file_path, 'w') as file:
        json.dump(existing_videos, file)

    print("Closing the gathering videos method.")
    return videos

def get_video_id(video_data):
    return video_data['snippet']['resourceId']['videoId']

def get_video_url(video_data):
    return f"https://www.youtube.com/watch?v={get_video_id(video_data)}"

def get_youtube_video_data(video_url):
    video_id = extract_video_id_from_url(video_url)
    url = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id=' + video_id + '&key=' + YOUTUBE_API_KEY
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def get_video_title(video_url):
    video_data = get_youtube_video_data(video_url)
    items = video_data.get('items', [])
    if items:
        return items[0].get('snippet', {}).get('title')
    return None

def get_video_description(video_url):
    video_data = get_youtube_video_data(video_url)
    items = video_data.get('items', [])
    if items:
        return items[0].get('snippet', {}).get('description')
    return None

def get_video_id_from_data(video_url):
    video_data = get_youtube_video_data(video_url)
    items = video_data.get('items', [])
    if items:
        return items[0].get('id')
    return None

def get_video_upload_date(video_data):
    return video_data['snippet']['publishedAt']

def get_video_upload_date_by_url(video_url):
    video_data = get_youtube_video_data(video_url)
    items = video_data.get('items', [])
    if items:
        return items[0].get('snippet', {}).get('publishedAt')
    return None

def get_channel_videos_titles(channel_id, youtube):
    videos = get_channel_videos(channel_id, youtube)
    video_titles = [get_video_title(video) for video in videos]
    return video_titles

def get_channel_videos_urls(channel_id, youtube):
    videos = get_channel_videos(channel_id, youtube)
    video_urls = [get_video_url(video) for video in videos]
    return video_urls

#to jest dobrze tylko ze arugmentem powinien byc video id a nie url
def get_video_data_by_url(video_url):
    video_id = extract_video_id_from_url(video_url)
    url = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id=' + video_id + '&key=' + YOUTUBE_API_KEY
    response = requests.get(url)
    data = json.loads(response.text)

    items = data.get('items', [])
    for item in items:
        snippet = item.get('snippet', {})
        title = snippet.get('title')
        description = snippet.get('description')
        id = snippet.get('id')

        print(f'Title: {title}')
        print(f'Description: {description}')
        print(f'ID: {id}')

    return data
    
# Function to fetch and save a YouTube video's transcript
def get_video_transcription(video_url):
    # Extract video_id from the URL
    video_id = video_url.split('v=')[1]
    # Fetch the transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript

#funkcjonalnosc zapisywania transkrypcji wideo do bazy danych

    # # Connect to the database
    # conn = sqlite3.connect('youtube_transcripts.db')
    # cursor = conn.cursor()

    # # Insert video details into the Video table
    # cursor.execute
    # ('''
    # INSERT OR IGNORE INTO Video (video_id, title, url)
    # VALUES (?, ?, ?, ?, ?)
    # ''', 
    #     (
    #     video_id,
    #     title,
    #     video_url,
    #     )
    # )

    #     # Insert transcript data into the Transcript table
    # for entry in transcript:
    #     cursor.execute('''
    #         INSERT INTO Transcript (video_id, timestamp, text)
    #         VALUES (?, ?, ?)
    #     ''', (video_id, entry['start'], entry['text']))

    # # Commit changes and close the connection
    # conn.commit()
    # conn.close()