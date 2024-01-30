import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

def create_connection():
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("PORT")

    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        print("connected successfully!")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
