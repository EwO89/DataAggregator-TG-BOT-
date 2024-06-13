import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()


class BaseSettings:
    def __init__(self):
        self.MONGODB_URI = os.getenv("MONGODB_URI")
        self.MONGODB_DB = os.getenv("MONGODB_DB")
        self.USERS_COLLECTION = os.getenv("USERS_COLLECTION")
        self.DATA_COLLECTION = os.getenv("DATA_COLLECTION")
        self.TOKEN = os.getenv("TOKEN")


class Settings(BaseSettings):
    def __init__(self):
        super().__init__()
        self.client = AsyncIOMotorClient(self.MONGODB_URI)
        self.db = self.client[self.MONGODB_DB]
        self.users_collection = self.db[self.USERS_COLLECTION]
        self.my_collection = self.db[self.DATA_COLLECTION]


settings = Settings()
