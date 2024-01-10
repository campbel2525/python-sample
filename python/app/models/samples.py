from datetime import datetime

from pytz import timezone  # type: ignore
from sqlalchemy import BigInteger, Column, DateTime, String

from config.settings import TIME_ZONE, Base


def current_timestamp():
    jst = timezone(TIME_ZONE)
    return datetime.now(jst)


class Test(Base):
    __tablename__ = "tests"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=True, comment="名前")

    created_at = Column(DateTime, nullable=True, default=current_timestamp)
    updated_at = Column(
        DateTime, nullable=True, default=current_timestamp, onupdate=current_timestamp
    )
