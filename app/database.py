from pymongo import MongoClient
from app.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["subtrack_sentinel"]

users_collection = db["users"]
subscriptions_collection = db["subscriptions"]
