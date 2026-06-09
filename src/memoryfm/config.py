import os
import urllib.parse
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DB_USER = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD", "password")
DB_PASSWORD = urllib.parse.quote_plus(password)
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
LOG_FILE = os.getenv("LOG_FILE", "logs/memoryfm.log")
APP_NAME = "memoryfm"

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DEBUG_DIR = os.getenv("DEBUG_DIR", None)

if DEBUG_DIR is not None:
    Path(DEBUG_DIR).mkdir(exist_ok=True)

Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
Path(LOG_FILE).touch(exist_ok=True)
