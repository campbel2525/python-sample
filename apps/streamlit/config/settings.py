import os
from pathlib import Path

from dotenv import load_dotenv

# .envを読み込む
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
APP_ENV = os.getenv("APP_ENV", "local")
DEBUG = os.getenv("DEBUG", False) == "True"
TIME_ZONE = "UTC"
