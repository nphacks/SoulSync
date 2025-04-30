# database.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))  # Get from environment variable
print('Mongo DB connected!')
db = client[os.getenv("MONGODB_DB_NAME")] 