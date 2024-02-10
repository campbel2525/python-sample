from datetime import datetime

from pytz import timezone  # type: ignore
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_mixin, relationship

from config.settings import TIME_ZONE


def current_timestamp():
    jst = timezone(TIME_ZONE)
    return datetime.now(jst)


@declarative_mixin
class BookMixin:
    id = Column(BigInteger, primary_key=True)
    title = Column(String(255), nullable=False, comment="書籍名")
    category = Column(String(255), nullable=False, comment="カテゴリ")
    created_at = Column(DateTime, nullable=False, default=current_timestamp)
    updated_at = Column(
        DateTime, nullable=False, default=current_timestamp, onupdate=current_timestamp
    )

    # book_contents = relationship(
    #     "BookContent", backref="book", order_by="BookContent.id"
    # )
    @declared_attr
    def book_contents(cls):
        return relationship("BookContent", backref="book", order_by="BookContent.sort")


@declarative_mixin
class BookContentMixin:
    id = Column(BigInteger, primary_key=True)
    book_id = Column(BigInteger, ForeignKey("books.id"), nullable=False)
    sort = Column(Integer, nullable=False, comment="順番")
    title = Column(String(255), comment="章名")
    content = Column(LONGTEXT, nullable=False, comment="内容")
    file_name = Column(String(255), nullable=False, comment="ファイル名")
    file_type = Column(String(255), nullable=False, comment="ファイルタイプ")
    file_size = Column(Integer, nullable=False, comment="ファイルサイズ")
    created_at = Column(DateTime, nullable=False, default=current_timestamp)
    updated_at = Column(
        DateTime, nullable=False, default=current_timestamp, onupdate=current_timestamp
    )

    @declared_attr
    def book_content_summary(cls):
        return relationship(
            "BookContentSummary",
            backref="book_content",
            uselist=False,
            order_by="BookContentSummary.id",
        )


@declarative_mixin
class BookContentSummaryMixin:
    id = Column(BigInteger, primary_key=True)
    book_content_id = Column(
        BigInteger, ForeignKey("book_contents.id"), nullable=False, unique=True
    )
    content = Column(LONGTEXT, nullable=False, comment="内容")
    created_at = Column(DateTime, nullable=False, default=current_timestamp)
    updated_at = Column(
        DateTime, nullable=False, default=current_timestamp, onupdate=current_timestamp
    )
