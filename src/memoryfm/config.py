import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD", "password")
DB_PASSWORD = urllib.parse.quote_plus(password)
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
