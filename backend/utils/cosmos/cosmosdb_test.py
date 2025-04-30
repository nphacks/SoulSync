import json
import os
import sys
import uuid

from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
from pymongo import MongoClient  

client = MongoClient(os.getenv("MONGODB_URI"))

print(client)

db = client["voice-journal-data"]  
# collection = db["user"]  

# # Insert one document
# data = {"name": "John", "age": 30, "city": "New York"}
# collection.insert_one(data)  

# # Insert multiple documents
# multiple_data = [
#     {"name": "Alice", "age": 25},
#     {"name": "Bob", "age": 35}
# ]
# collection.insert_many(multiple_data) 

# # Fetch all documents
# for doc in collection.find():
#     print(doc)

# # Fetch with filter (e.g., name = "John")
# print(collection.find_one({"name": "John"}))

collection = db['journal-entry']
journal_multiple_data = [
    {"name": "Alice", "entryTime": '22/04/2025', "entryText": "The sunrise painted the sky in soft hues of pink and gold as I sat by the window with a cup of coffee. The world outside was still waking up—birds chirping lazily, a gentle breeze rustling the leaves. For the first time in weeks, my mind felt calm, unburdened by deadlines or noise. I scribbled a few thoughts in my notebook, grateful for this rare moment of stillness."},
    {"name": "Alice", "entryTime": '23/04/2025', "entryText": "The city was alive tonight—neon lights, laughter spilling from bars, strangers brushing past me on the sidewalk. Yet, surrounded by so many, I’ve never felt more invisible. I wondered how many of them carried the same weight I did, hiding behind smiles or hurried steps. Sometimes loneliness doesn’t need solitude; it thrives in crowds."},
    {"name": "Alice", "entryTime": '24/04/2025', "entryText": "After months of hesitation, I finally submitted my short story to a literary magazine. The moment I hit “send,” my hands shook—part terror, part exhilaration. Even if it’s rejected, I’m proud of pushing past the fear. Growth happens in these tiny, defiant acts. Today, I chose courage over comfort."},
]
collection.insert_many(journal_multiple_data) 

for doc in collection.find():
    print(doc)