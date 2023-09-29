import psycopg2
import json
from youtube import get_video_id_from_data, get_video_title, get_video_description, get_video_upload_date_by_url, get_video_transcription
from config import JSON_FILE_PATH

def get_all_videos_ids_from_database():
    conn = psycopg2.connect(host="localhost", dbname="youtube_transcripts", user="postgres", password="postgres", port=5432)

    cur = conn.cursor()

    # Actual database work
    cur.execute("""
                SELECT video_id FROM video;
                 """)

    # Fetch all the results into a list
    video_ids = [row[0] for row in cur.fetchall()]

    conn.commit()
    cur.close()
    conn.close()

    return video_ids

def find_missing_video_ids(database_video_ids, json_file_path):
    # Load the video IDs from the JSON file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        json_video_ids = json_data

    # Convert both lists to sets for efficient comparison
    database_video_set = set(database_video_ids)
    json_video_set = set(json_video_ids)

    # Find the video IDs that are in the JSON file but not in the database
    missing_video_ids = json_video_set - database_video_set

    if not missing_video_ids:
        print("No missing video IDs found.")

    return list(missing_video_ids)

def save_video_data_to_database(video_id):
    conn = psycopg2.connect(
        host="localhost",
        dbname="youtube_transcripts",
        user="postgres",
        password="postgres",
        port=5432
    )

    cur = conn.cursor()

    # Check if the video already exists in the database
    cur.execute("SELECT COUNT(*) FROM video WHERE video_id = %s;", (video_id,))
    count = cur.fetchone()[0]

    if count == 0:
        # If it doesn't exist, fetch video data and insert a new record
        video_url = 'https://www.youtube.com/watch?v=' + video_id

        video_id = get_video_id_from_data(video_url)
        title = get_video_title(video_url)
        description = get_video_description(video_url)
        url = video_url
        upload_date = get_video_upload_date_by_url(video_url)

        cur.execute("INSERT INTO video (video_id, title, description, url, upload_date) VALUES (%s, %s, %s, %s, %s);",
                    (video_id, title, description, url, upload_date))
        print(video_id + " successfully saved into the Video database table.")
        
        # Fetch the transcript data
        transcript = get_video_transcription(video_url)
        
        # Iterate through the transcript and insert each row into the transcript table
        for row in transcript:
            timestamp = int(row['start'] * 1000)  # Convert start time to milliseconds
            text = row['text']
            cur.execute("INSERT INTO transcript (video_id, timestamp, text) VALUES (%s, %s, %s);",
                        (video_id, timestamp, text))
        print(video_id + " successfully saved into the Transcript database table.")
        
        conn.commit()

    cur.close()
    conn.close()

def save_missing_videos_to_database():
    database_video_ids = get_all_videos_ids_from_database()
    missing_video_ids = find_missing_video_ids(database_video_ids, JSON_FILE_PATH)

    for video_id in missing_video_ids:
        save_video_data_to_database(video_id)

    print("*** SAVING MISSING VIDEOS IN DATABASE COMPLETED ***")
