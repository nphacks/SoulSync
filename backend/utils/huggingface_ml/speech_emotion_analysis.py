from transformers import pipeline

# Initialize the model once
emotion_pipe = pipeline(
    "audio-classification", 
    model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
)

def speech_emotion_analysis(audio_paths: list):
    emotion_totals = {}
    emotion_counts = {}
    
    for path in audio_paths:
        results = emotion_pipe(path)
        for result in results:
            emotion = result['label']
            score = result['score']
            
            if emotion not in emotion_totals:
                emotion_totals[emotion] = 0
                emotion_counts[emotion] = 0
            
            emotion_totals[emotion] += score
            emotion_counts[emotion] += 1
    
    # Calculate averages
    emotion_averages = {
        emotion: total / emotion_counts[emotion]
        for emotion, total in emotion_totals.items()
    }
    
    return emotion_averages


# @misc {enrique_hernández_calabrés_2024,
#     author       = { {Enrique Hernández Calabrés} },
#     title        = { wav2vec2-lg-xlsr-en-speech-emotion-recognition (Revision 17cf17c) },
#     year         = 2024,
#     url          = { https://huggingface.co/ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition },
#     doi          = { 10.57967/hf/2045 },
#     publisher    = { Hugging Face }
# }
