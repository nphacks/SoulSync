# utils/audio_processor.py
from pydub import AudioSegment
import math

def chop_audio(file_path: str):
    audio = AudioSegment.from_wav(file_path)
    chunk_length_ms = 30 * 1000  # 30 seconds in milliseconds
    parts = []
    
    for i, start in enumerate(range(0, len(audio), chunk_length_ms)):
        end = start + chunk_length_ms
        chunk = audio[start:end]
        chunk_path = f"{file_path}_part_{i+1}.wav"
        chunk.export(chunk_path, format="wav")
        parts.append(chunk_path)
    
    return parts