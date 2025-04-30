from pydantic import BaseModel
from datetime import date
from typing import Optional

class JournalEntry(BaseModel):
    journal_type: str
    user_id: str
    timestamp: date
    sentiment: str
    text_emotion: str
    speech_emotion: Optional[str] = None
    blob_url: str
    text: str
    text_embeddings: list[float]
    text_emotion_metric: dict
    speech_emotion_metric: Optional[dict] = None
    text_emotion_score: float
    speech_emotion_score: Optional[float] = None
    sentiment_score: float
    sentiment_metric: dict
    topics: list[str]