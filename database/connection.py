import os

from pymongo import MongoClient
from pymongo.database import Database


MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://127.0.0.1:27017",
)

MONGODB_DB_NAME = os.getenv(
    "MONGODB_DB_NAME",
    "ai_booking_agent",
)


client = MongoClient(MONGODB_URI)
database: Database = client[MONGODB_DB_NAME]