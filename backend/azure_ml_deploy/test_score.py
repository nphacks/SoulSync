import os
import json
import numpy as np
from SER.registry.score import init, run, preprocess  # Import your functions

# 1. Set up mock Azure paths
os.environ["AZUREML_MODEL_DIR"] = "SER/registry"  # Points to current folder

# 2. Call init() to load model/scaler
init()  # Should NOT crash

# 3. Test run() with dummy audio data (adjust to match your input format)
dummy_data = {
    "data": "test3.wav"  # Replace with a real short audio file (or mock array)
}
# features = preprocess("test3.wav") 
# print(f"Feature shape: {features.shape}")  
with open("test3.wav", "rb") as f:
    audio_data = f.read()
result = run(audio_data)  # JSON input expected
print("Test Result:", result)