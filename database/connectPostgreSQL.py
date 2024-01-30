import os
from dotenv import load_dotenv
import psycopg2
load_dotenv()

def create_connection():
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("PORT")

    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        print("התחברת בהצלחה למסד הנתונים!")
        return conn
    except Exception as e:
        print(f"שגיאה במהלך התחברות: {e}")
        return None