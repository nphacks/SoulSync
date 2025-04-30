import json
import os
import io
import numpy as np
import librosa
from keras.models import load_model

def init():
    global model, scaler_mean, scaler_std
    model_dir = os.getenv('AZUREML_MODEL_DIR', 'SER/registry')
    print(f"Model dir contents: {os.listdir(model_dir)}")

    model = load_model(os.path.join(model_dir, 'emotion_model.h5'))
    scaler_mean = np.load(os.path.join(model_dir, 'scaler.npy'))
    scaler_std = np.load(os.path.join(model_dir, 'scaler_std.npy'))

def preprocess(audio_bytes):
    # Your feature extraction logic (must match training)
    # y, sr = librosa.load(audio_path, duration=3)
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None, mono=True, duration=3)
    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40), axis=1)
    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=y))
    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1)
    features = np.concatenate([mfccs, [centroid, zcr], chroma])
    features = (features - scaler_mean) / scaler_std
    return features.reshape(1, -1)

def run(raw_data):
    try:
        if isinstance(raw_data, str):
            input_data = json.loads(raw_data)
            audio_bytes = bytes(input_data['data'])  # depends how frontend sends it
        else:
            audio_bytes = raw_data
    
        features = preprocess(raw_data)
        probas = model.predict(features)[0]
        emotion_labels = ['neutral', 'happy', 'sad', 'angry', 'fear', 'disgust', 'surprise', 'calm']
        return {emotion: float(prob) for emotion, prob in zip(emotion_labels, probas)}
    except Exception as e:
        return {"error": str(e)}