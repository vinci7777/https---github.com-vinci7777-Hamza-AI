import sqlite3

def initialize_database():
    # Create a database (or connect to an existing one)
    conn = sqlite3.connect('youtube_transcripts.db')
    cursor = conn.cursor()

    # Create Video and Transcript tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Video (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            url TEXT,
            upload_date DATE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transcript (
            transcript_id INTEGER PRIMARY KEY,
            video_id TEXT,
            timestamp TEXT,
            text TEXT,
            FOREIGN KEY (video_id) REFERENCES Video(video_id)
        )
    ''')

   # Commit changes and close the connection
    conn.commit()
    conn.close()

# Function to check if the database exists and initialize if not
def check_and_initialize_database():
    try:
        # Attempt to connect to the database
        conn = sqlite3.connect('youtube_transcripts.db')
        conn.close()
    except sqlite3.OperationalError:
        # If the database doesn't exist, initialize it
        initialize_database()
