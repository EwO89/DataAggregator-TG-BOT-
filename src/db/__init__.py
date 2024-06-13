from src.config.base import settings
from src.db.index import create_indexes


def get_db_collections():
    return settings.db, settings.users_collection, settings.my_collection
