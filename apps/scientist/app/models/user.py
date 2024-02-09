import hashlib

from sqlalchemy import exists
from sqlalchemy.orm import Session

from config.settings import Base
from common.database.model_mixins.user_mixins import UserMixin


class User(Base, UserMixin):
    __tablename__ = "users"

    @classmethod
    def exist_user(cls, db: Session, email: str) -> bool:
        return db.query(exists().where(User.email == email)).scalar()

    @classmethod
    def password_to_hash(cls, password: str) -> str:
        return hashlib.sha512(password.encode("utf-8")).hexdigest()

    def check_password(self, raw_password: str) -> bool:
        return self.password == User.password_to_hash(raw_password)
