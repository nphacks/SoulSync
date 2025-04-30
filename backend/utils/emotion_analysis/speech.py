
from utils.audio_entry.audio_processor import chop_audio
from utils.huggingface_ml.speech_emotion_analysis import speech_emotion_analysis

def speech_task(file_location):
    parts = chop_audio(file_location)
    speech_emotions = speech_emotion_analysis(parts)
   
    return speech_emotions, parts