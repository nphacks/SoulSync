# routes/journal_entry.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from datetime import date
import aiofiles
import os
from concurrent.futures import ThreadPoolExecutor
from models.journal import JournalEntry
from utils.azure.blob_storage import AzureBlobStorage
from utils.azure.handwrittenOrDocument import analyze_read
from utils.cosmos.embeddings import create_embeddings
from utils.cosmos.journal_entry import add_journal_entry
from utils.emotion_analysis.text import text_task
from utils.emotion_analysis.speech import speech_task
from utils.emotion_analysis.topic_extraction import extract_topics
from dotenv import load_dotenv
import uuid
from typing import List, Dict
import json

load_dotenv()

router = APIRouter()
blob_storage = AzureBlobStorage(
    os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
    os.getenv("AZURE_STORAGE_CONTAINER")
)

def get_top_score(data: dict) -> tuple:
    top_key = max(data, key=data.get)
    top_value = round(data[top_key], 4)
    return (top_key, top_value)

@router.post("/audio/")
async def upload_audio_with_metadata(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    journal = JournalEntry(
        journal_type="audio",
        user_id=user_id,  
        timestamp=date.today(),  
        sentiment="",
        sentiment_score=0.0,
        sentiment_metric={},
        text_emotion="",
        text_emotion_score=0.0,
        text_emotion_metric={},
        speech_emotion="",
        speech_emotion_score=0.0,
        speech_emotion_metric={},
        blob_url="",
        text="",
        text_embeddings=[],
        topics=[],
    )

    try:
        # Save Audio file locally
        file_location = f"audio/{file.filename}"
        async with aiofiles.open(file_location, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        # Upload to Azure Blob Storage (main thread)
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        blob_url = blob_storage.upload_file(file_location, unique_name)
        journal.blob_url = blob_url

        with ThreadPoolExecutor() as executor:
            # Thread for Sentiment Analysis and Text Emotion Recognition
            future_text = executor.submit(text_task, file_location=file_location, audio_input=True)
            # Thread for Speech Emotion Recognition
            future_speech = executor.submit(speech_task, file_location=file_location)
            
            # Text Processing
            speech_text, sentiment_analysis_data, text_analysis_data = future_text.result()
            # Audio Transcribed text
            journal.text = speech_text
            journal.text_embeddings = create_embeddings(speech_text)

            #Extract Topics
            journal.topics = extract_topics(speech_text)

            # Sentiment Anaylsis Data
            journal.sentiment = sentiment_analysis_data.sentiment
            confidence_scores = {
                "positive": float(sentiment_analysis_data.confidence_scores.positive),
                "neutral": float(sentiment_analysis_data.confidence_scores.neutral),
                "negative": float(sentiment_analysis_data.confidence_scores.negative)
            }
            journal.sentiment_metric = confidence_scores

            # Text Emotion Recognition Data
            top_emotion = get_top_score(text_analysis_data)
            journal.text_emotion = top_emotion[0]
            journal.text_emotion_score = top_emotion[1]
            journal.text_emotion_metric = text_analysis_data

            #  Audio Speech Processing
            speech_emotions, parts = future_speech.result()

            # Speech Emotion Recognition Data
            top_emotion = get_top_score(speech_emotions)
            journal.speech_emotion = top_emotion[0]
            journal.speech_emotion_score = top_emotion[1]
            journal.speech_emotion_metric = speech_emotions

        journal_entry_status = add_journal_entry(journal)

        # Cleanup (Remove local audio files)
        if os.path.exists(file_location):
            os.remove(file_location)

        for part in parts:
            if os.path.exists(part):
                os.remove(part)

        return {
            "journal_id": journal_entry_status["inserted_id"],
            "message": "Success",
            "status": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Text journal entry route
@router.post("/text/")
async def create_text_entry(
    user_id: str = Form(...),
    text: str = Form(...)
    ):
    journal = JournalEntry(
        journal_type="text",
        user_id=user_id,  
        timestamp=date.today(),  
        sentiment="",
        sentiment_score=0.0,
        sentiment_metric={},
        text_emotion="",
        text_emotion_score=0.0,
        text_emotion_metric={},
        speech_emotion=None,
        speech_emotion_score=None,
        speech_emotion_metric=None,
        blob_url="",
        text=text,
        text_embeddings=[],
        topics=[],
    )
    try:
        journal.text_embeddings = create_embeddings(text)
        #Extract Topics
        journal.topics = extract_topics(text)
        speech_text, sentiment_analysis_data, text_analysis_data = text_task(None, False, text)

        # Sentiment Anaylsis Data
        journal.sentiment = sentiment_analysis_data.sentiment
        confidence_scores = {
            "positive": float(sentiment_analysis_data.confidence_scores.positive),
            "neutral": float(sentiment_analysis_data.confidence_scores.neutral),
            "negative": float(sentiment_analysis_data.confidence_scores.negative)
        }
        journal.sentiment_metric = confidence_scores

        # Text Emotion Recognition Data
        top_emotion = get_top_score(text_analysis_data)
        journal.text_emotion = top_emotion[0]
        journal.text_emotion_score = top_emotion[1]
        journal.text_emotion_metric = text_analysis_data

        journal_entry_status = add_journal_entry(journal)

        return {
            "journal_id": journal_entry_status["inserted_id"],
            "message": "Success",
            "status": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image journal entry route
@router.post("/image/")
async def upload_image_with_metadata(
    document: UploadFile = File(...),
    user_id: str = Form(...),
):
    journal = JournalEntry(
        journal_type="handwritten",
        user_id=user_id,  
        timestamp=date.today(),  
        sentiment="",
        sentiment_score=0.0,
        sentiment_metric={},
        text_emotion="",
        text_emotion_score=0.0,
        text_emotion_metric={},
        speech_emotion=None,
        speech_emotion_score=None,
        speech_emotion_metric=None,
        blob_url="",
        text="",
        text_embeddings=[],
        topics=[],
    )
    try:
        # Save the document locally
        image_location = f"images/{document.filename}"
    
        async with aiofiles.open(image_location, 'wb') as out_file:
            content = await document.read()
            await out_file.write(content)

        # Store the document in blob storage
        unique_name = f"{uuid.uuid4()}_{document.filename}"
        blob_url = blob_storage.upload_file(image_location, unique_name)

        doc_to_text = analyze_read(blob_url)
        journal.text = doc_to_text
        #Extract Topics
        journal.topics = extract_topics(doc_to_text)
        journal.text_embeddings = create_embeddings(doc_to_text)
        speech_text, sentiment_analysis_data, text_analysis_data = text_task(None, False, doc_to_text)

        # Sentiment Anaylsis Data
        journal.sentiment = sentiment_analysis_data.sentiment
        confidence_scores = {
            "positive": float(sentiment_analysis_data.confidence_scores.positive),
            "neutral": float(sentiment_analysis_data.confidence_scores.neutral),
            "negative": float(sentiment_analysis_data.confidence_scores.negative)
        }
        journal.sentiment_metric = confidence_scores

        # Text Emotion Recognition Data
        top_emotion = get_top_score(text_analysis_data)
        journal.text_emotion = top_emotion[0]
        journal.text_emotion_score = top_emotion[1]
        journal.text_emotion_metric = text_analysis_data

        journal_entry_status = add_journal_entry(journal)

        return {
            "journal_id": journal_entry_status["inserted_id"],
            "message": "Success",
            "status": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Chatbot journal entry route
@router.post("/chatbot/")
async def create_text_entry(
    user_id: str = Form(...),
    conversation: str = Form(...)
    ):
    journal = JournalEntry(
        journal_type="chatbot",
        user_id=user_id,  
        timestamp=date.today(),  
        sentiment="",
        sentiment_score=0.0,
        sentiment_metric={},
        text_emotion="",
        text_emotion_score=0.0,
        text_emotion_metric={},
        speech_emotion=None,
        speech_emotion_score=None,
        speech_emotion_metric=None,
        blob_url="",
        text=conversation,
        text_embeddings=[],
        topics=[],
    )
    try:
        try:
            conv_list = json.loads(conversation) # Parse JSON
            text = " ".join(m["content"] for m in conv_list if m["role"] == "user")
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid conversation format")
        journal.text_embeddings = create_embeddings(text)
        #Extract Topics
        journal.topics = extract_topics(text)
        speech_text, sentiment_analysis_data, text_analysis_data = text_task(None, False, text)

        # Sentiment Anaylsis Data
        journal.sentiment = sentiment_analysis_data.sentiment
        confidence_scores = {
            "positive": float(sentiment_analysis_data.confidence_scores.positive),
            "neutral": float(sentiment_analysis_data.confidence_scores.neutral),
            "negative": float(sentiment_analysis_data.confidence_scores.negative)
        }
        journal.sentiment_metric = confidence_scores

        # Text Emotion Recognition Data
        top_emotion = get_top_score(text_analysis_data)
        journal.text_emotion = top_emotion[0]
        journal.text_emotion_score = top_emotion[1]
        journal.text_emotion_metric = text_analysis_data

        journal_entry_status = add_journal_entry(journal)

        return {
            "journal_id": journal_entry_status["inserted_id"],
            "message": "Success",
            "status": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))