from pymongo import MongoClient, mongo_client

conn = MongoClient("mongodb+srv://eminds:O12dgzw6kGJsTyxB@cluster0.eoirq45.mongodb.net/")
database = conn["mobility-seller"]