import factory
from factory.alchemy import SQLAlchemyModelFactory

from app import models
from config.settings import db


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = db
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("name")
    email = factory.Sequence(lambda n: f"test{n}@example.com")
    password = factory.Faker("pystr", min_chars=10, max_chars=20)
