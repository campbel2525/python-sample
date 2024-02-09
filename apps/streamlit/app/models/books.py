from common.database.model_mixins.book_mixins import (
    BookContentMixin,
    BookContentSummaryMixin,
    BookMixin,
)
from config.settings import Base


class Book(Base, BookMixin):
    __tablename__ = "books"


class BookContent(Base, BookContentMixin):
    __tablename__ = "book_contents"


class BookContentSummary(Base, BookContentSummaryMixin):
    __tablename__ = "book_content_summaries"
