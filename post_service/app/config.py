from pymongo import AsyncMongoClient

MONGO_URI = "mongodb://localhost:27017/"

client = AsyncMongoClient(MONGO_URI)
db = client["blog_mgmt"]
