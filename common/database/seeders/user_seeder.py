from app import models
from database import factories


class UserSeeder:
    default_password = "test1234"

    def handle(self) -> None:
        password = models.User.password_to_hash(self.default_password)

        factories.UserFactory.create(
            name="test1",
            email="test1@example.com",
            password=password,
        )
