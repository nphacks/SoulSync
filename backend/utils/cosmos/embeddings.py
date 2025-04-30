from pymongo import MongoClient
import requests
import json
import os
from database.database import db
 
collection = db['journal-entry']

def create_embeddings(text: str):
    print('Reached create embeddings')
    # Create embeddings
    url = 'https://api.jina.ai/v1/embeddings'
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {os.getenv('JINA_API')}"
    }
    data = {
        "model": "jina-clip-v2",
        "dimensions": 512,
        "normalized": True,
        "embedding_type": "float",
        "input": [ {"text": text} ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()['data'][0]['embedding']

def vector_search(query, user_id, num_results=50):
    query_embedding = create_embeddings(query)
    pipeline = [
        {
            '$search': {
                "cosmosSearch": {
                    "vector": query_embedding,
                    "path": "text_embeddings",
                    "k": num_results,
                    # "filter": {"user_id": user_id}
                },
                "returnStoredSource": True 
            }
        },
        {
            '$match': {
                'user_id': user_id
            }
        },
        {
            '$project': { 
                'similarityScore': { 
                    '$meta': 'searchScore' 
                }, 
                'document' : '$$ROOT' 
            } 
        }
    ]
    results = collection.aggregate(pipeline)
    return results