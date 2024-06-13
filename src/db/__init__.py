from src.config.base import settings


def get_db_collections():
    return settings.db, settings.users_collection, settings.my_collection
