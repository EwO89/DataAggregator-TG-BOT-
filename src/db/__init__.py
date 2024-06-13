from src.config.base import settings


def get_db_collections():
    return settings.db, settings.susers_collection, settings.my_collection
