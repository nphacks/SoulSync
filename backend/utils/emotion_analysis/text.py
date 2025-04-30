from utils.azure.speech_to_text import transcribe_audio_file
from utils.azure.sentiment_analysis import sentiment_analysis
from utils.huggingface_ml.text_emotion_analysis import text_emotion_analysis

import os

def text_task(file_location, audio_input, text = ''):
    speech_text = ''
    if audio_input:
        speech_text = transcribe_audio_file(
            audio_file_path=file_location,
            subscription_key=os.getenv("YOUR_AZURE_SPEECH_KEY"),
            region="eastus2"
        )

        sentiment_analysis_data = sentiment_analysis(speech_text)    
        
        text_analysis_data = text_emotion_analysis(speech_text)
    
    else:
        sentiment_analysis_data = sentiment_analysis(text)    
    
        text_analysis_data = text_emotion_analysis(text)
    
    return speech_text, sentiment_analysis_data, text_analysis_data