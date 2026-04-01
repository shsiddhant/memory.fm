from platformdirs import user_data_path

APP_NAME = "memoryfm"
USER_DIR = user_data_path(appname=APP_NAME, appauthor=False, ensure_exists=True)
DB_PATH = USER_DIR / f"{APP_NAME}-db.sqlite"
DB_URL = f"sqlite:///{DB_PATH}"
