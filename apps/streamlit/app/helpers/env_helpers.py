from config import settings


def is_local():
    return settings.APP_ENV == "local"


def is_production():
    return settings.APP_ENV == "prod"
