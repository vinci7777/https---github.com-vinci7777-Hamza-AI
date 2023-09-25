from youtube_transcript_api import YouTubeTranscriptApi
import sqlite3

# Function to fetch and save a YouTube video's transcript
def fetch_and_save_transcript(video_url):
    # Extract video_id from the URL
    video_id = video_url.split('v=')[1]

    # Fetch the transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Get video details (title, description, upload date)
    video_details = YouTubeTranscriptApi.get_transcript(video_id)

    # Connect to the database
    conn = sqlite3.connect('youtube_transcripts.db')
    cursor = conn.cursor()

    # Insert video details into the Video table
    cursor.execute('''
    INSERT OR IGNORE INTO Video (video_id, title, description, url, upload_date)
    VALUES (?, ?, ?, ?, ?)
''', (
    video_id,
    video_details.get('title', 'No Title'),
    video_details.get('description', 'No Description'),
    video_url,
    video_details.get('upload_date', 'Unknown Date')
    ))
 
    # Insert transcript data into the Transcript table
    for entry in transcript:
        cursor.execute('''
            INSERT INTO Transcript (video_id, timestamp, text)
            VALUES (?, ?, ?)
        ''', (video_id, entry['start'], entry['text']))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
