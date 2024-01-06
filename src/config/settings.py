import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import logging

# from pathlib import Path


# .envを読み込む
load_dotenv()

# app
# BASE_DIR = Path(__file__).resolve().parent


TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
# DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# データベースの接続情報
DATABASE = {
    "DB_DIALECT": os.getenv("DB_DIALECT"),
    "DB_DRIVER": os.getenv("DB_DRIVER"),
    "DB_HOST": os.getenv("DB_HOST"),
    "DB_PORT": os.getenv("DB_PORT"),
    "DB_DATABASE": os.getenv("DB_DATABASE"),
    "DB_USERNAME": os.getenv("DB_USERNAME"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    "DB_CHARSET_TYPE": os.getenv("DB_CHARSET_TYPE"),
}
d = DATABASE
DATABASE_URL = f"{d['DB_DIALECT']}+{d['DB_DRIVER']}://{d['DB_USERNAME']}:{d['DB_PASSWORD']}@{d['DB_HOST']}:{d['DB_PORT']}/{d['DB_DATABASE']}?charset={d['DB_CHARSET_TYPE']}"  # noqa: E501

# ロガーの設定
logging.basicConfig(filename="logs/sqlalchemy.log")
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

DB_DEBUG = os.getenv("DB_DEBUG", False) == "True"
engine = create_engine(DATABASE_URL, echo=DB_DEBUG, pool_recycle=3600)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = Session()
Base = declarative_base()
