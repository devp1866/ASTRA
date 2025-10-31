import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

db = None
try:
    client = MongoClient(MONGO_URI)
    db = client["customer_support_agent"]
    print("✅ MongoDB connection successful.")
except Exception as e:
    print(f"❌ MongoDB connection failed: {str(e)}")


#  Helper function to get a specific collection
def get_collection(name: str):
    if db is not None:
        return db[name]
    else:
        raise ConnectionError("Database connection not established.")
