import psycopg2
import os 
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

def get_pending_audio_path():
    conn = psycopg2.connect(database_url)
     
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, s3_path FROM record
        WHERE status = 'SAVED'
    """)
    
    rows = cur.fetchall()
    conn.close()
    return [{'record_id': row[0], 's3_path': row[1]} for row in rows]
