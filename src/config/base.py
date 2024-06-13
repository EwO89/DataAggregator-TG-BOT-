import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()


class BaseSettings:
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DB = os.getenv("MONGODB_DB")
    USERS_COLLECTION = os.environ.get("USERS_COLLECTION")
    DATA_COLLECTION = os.getenv("DATA_COLLECTION")


class Settings(BaseSettings):
    client = AsyncIOMotorClient(BaseSettings.MONGODB_URI)
    db = client[BaseSettings.MONGODB_DB]
    users_collection = db[BaseSettings.USERS_COLLECTION]
    my_collection = db[BaseSettings.DATA_COLLECTION]


settings = Settings()
