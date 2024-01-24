import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# .envを読み込む
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
APP_ENV = os.getenv("APP_ENV", "local")
DEBUG = os.getenv("DEBUG", False) == "True"
TIME_ZONE = "UTC"
# DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# データベースの接続情報
DB_DIALECT = os.getenv("DB_DIALECT")
DB_DRIVER = os.getenv("DB_DRIVER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CHARSET_TYPE = os.getenv("DB_CHARSET_TYPE")
DATABASE_URL = f"{DB_DIALECT}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset={DB_CHARSET_TYPE}"  # noqa: E501

# sqlのlog設定
DB_DEBUG = os.getenv("DB_DEBUG", False) == "True"
if APP_ENV == "local":
    logging.basicConfig(filename="logs/sqlalchemy.log")
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# DBセッション
engine = create_engine(DATABASE_URL, echo=False, pool_recycle=3600)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
db = Session()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# jwt
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
JWT_ACCESS_TOKEN_EXPIRES_SECONDS = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRES_SECONDS", 3600)
)
JWT_REFRESH_TOKEN_EXPIRES_SECONDS = int(
    os.getenv("JWT_REFRESH_TOKEN_EXPIRES_SECONDS", 864000)
)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "")
