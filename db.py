import os
import redis
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

mongo_url = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB_NAME")

client = AsyncIOMotorClient(mongo_url)
database = client[mongo_db_name]