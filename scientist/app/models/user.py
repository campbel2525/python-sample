from config.settings import Base
from database.model_mixins.user_mixin import UserMixin


class User(Base, UserMixin):
    __tablename__ = "users"
