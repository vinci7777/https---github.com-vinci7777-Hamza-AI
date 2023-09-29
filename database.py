import psycopg2
from psycopg2 import sql

def create_database_if_not_exists():
    try:
        # Connect to the default PostgreSQL database (e.g., "postgres")
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if the database exists; if not, create it
        db_name = "youtube_transcripts"
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("CREATE DATABASE " + db_name)
            print(f'Created database: {db_name}')
        else:
            print(f'Database already exists: {db_name}')

        conn.close()
    except Exception as e:
        print('Error creating database:', e)

def initialize_database():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            database="youtube_transcripts",  # Use the same name as specified in create_database_if_not_exists
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
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
                transcript_id SERIAL PRIMARY KEY,
                video_id TEXT,
                timestamp TEXT,
                text TEXT,
                FOREIGN KEY (video_id) REFERENCES Video(video_id)
            )
        ''')

        # Commit changes and close the connection
        conn.commit()
        conn.close()
    except Exception as e:
        print('Error initializing database:', e)

# Function to check if the database exists and initialize if not
def check_and_initialize_database():
    try:
        # Attempt to connect to the PostgreSQL database
        conn = psycopg2.connect(
            database="youtube_transcripts",  # Use the same name as specified in create_database_if_not_exists
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print('Connected to the PostgreSQL database.')
    except psycopg2.OperationalError as e:
        # If the database doesn't exist, create it and initialize tables
        if "does not exist" in str(e):
            try:
                create_database_if_not_exists()
                initialize_database()
                print('Database created and initialized successfully!')
            except Exception as ex:
                print('Error:', ex)
        else:
            print('Error:', e)



