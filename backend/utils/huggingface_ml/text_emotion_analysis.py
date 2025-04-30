from transformers import pipeline
import numpy as np

def text_emotion_analysis(text: str):
    # Load the emotion classification model
    classifier = pipeline(
        "text-classification",
        model="SamLowe/roberta-base-go_emotions",
        top_k=None
    )
    
    # Get raw predictions
    results = classifier(text)[0]
    
    # Map to your desired emotion categories
    emotion_map = {
        'admiration': 'happy',
        'amusement': 'happy',
        'anger': 'angry',
        'annoyance': 'angry',
        'approval': 'happy',
        'caring': 'happy',
        'confusion': 'fearful',
        'curiosity': 'surprised',
        'desire': 'happy',
        'disappointment': 'sad',
        'disapproval': 'disgust',
        'disgust': 'disgust',
        'embarrassment': 'fearful',
        'excitement': 'happy',
        'fear': 'fearful',
        'gratitude': 'happy',
        'grief': 'sad',
        'joy': 'happy',
        'love': 'happy',
        'nervousness': 'fearful',
        'neutral': 'neutral',
        'optimism': 'happy',
        'pride': 'happy',
        'realization': 'surprised',
        'relief': 'calm',
        'remorse': 'sad',
        'sadness': 'sad',
        'surprise': 'surprised'
    }
    
    # Aggregate scores
    emotion_scores = {
        "calm": 0.0,
        "angry": 0.0,
        "happy": 0.0,
        "fearful": 0.0,
        "neutral": 0.0,
        "disgust": 0.0,
        "sad": 0.0,
        "surprised": 0.0
    }
    
    for emotion in results:
        mapped_emotion = emotion_map.get(emotion['label'], 'neutral')
        emotion_scores[mapped_emotion] += emotion['score']
    
    # Normalize scores to sum to 1
    total = sum(emotion_scores.values())
    return {k: v/total for k, v in emotion_scores.items()}