from pymongo import MongoClient
import os
from database.database import db
# Connect to Cosmos DB Mongo API
from pymongo import MongoClient  

JOURNAL_COLLECTION = "journal-entry"
USER_COLLECTION = "user"
journal_collection = db[JOURNAL_COLLECTION]
user_collection = db[USER_COLLECTION]

if JOURNAL_COLLECTION not in db.list_collection_names():
    db.create_collection(JOURNAL_COLLECTION)
    print("Created collection '{}'.\n".format(JOURNAL_COLLECTION))
else:
    print("Using collection: '{}'.\n".format(JOURNAL_COLLECTION))

if USER_COLLECTION not in db.list_collection_names():
    db.create_collection(USER_COLLECTION)
    print("Created collection '{}'.\n".format(USER_COLLECTION))
else:
    print("Using collection: '{}'.\n".format(USER_COLLECTION))

# Reset db and collection
# journal_collection.drop_indexes()
# client.drop_database(JOURNAL_COLLECTION)

db.command({
  'createIndexes': 'journal-entry',
  'indexes': [
    {
      'name': 'VectorSearchIndex',
      'key': {
        "text_embeddings": "cosmosSearch"
      },
      'cosmosSearchOptions': {
        'kind': 'vector-ivf',
        'numLists': 1,
        'similarity': 'COS',
        'dimensions': 512
      }
    }
  ]
})