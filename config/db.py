from pymongo import MongoClient, mongo_client

conn = MongoClient("mongodb://localhost:27017/")
database = conn["mobility-seller"]