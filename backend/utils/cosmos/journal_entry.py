from fastapi import APIRouter, HTTPException
from bson import ObjectId, json_util
import json
from typing import List 
from pydantic import BaseModel
from datetime import date
from datetime import datetime
from utils.cosmos.embeddings import vector_search
from database.database import db

# Connect to Cosmos DB Mongo API 
collection = db['journal-entry']

class JournalEntry(BaseModel):
    journal_type: str
    user_id: str
    timestamp: date
    sentiment: str
    text_emotion: str
    speech_emotion: str
    blob_url: str
    text: str
    text_embeddings: list[float]
    text_emotion_metric: dict
    speech_emotion_metric: dict
    text_emotion_score: float
    speech_emotion_score: float
    sentiment_score: float
    sentiment_metric: dict

def add_journal_entry(data: JournalEntry) -> dict:
    # Prepare journal entries
    data_dict = data.dict()
    data_dict["timestamp"] = datetime.combine(data_dict["timestamp"], datetime.min.time())

    result = collection.insert_one(data_dict) 
    return {"success": result.acknowledged, "inserted_id": str(result.inserted_id)}

def get_user_entries(user_id: str) -> List[dict]:
    try:
        query = {"user_id": user_id}
        return list(collection.find(query))
    except Exception as e:
        raise ValueError(str(e))

def search_vector_embeddings(userid: str, query: str):
    results = vector_search(query, userid)
    combined_text = " ".join(
        result['document']['text'] 
        for result in results 
        if result['similarityScore'] > 6
    )
    return combined_text if combined_text else "No similar journal entries found"