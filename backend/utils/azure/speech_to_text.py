import azure.cognitiveservices.speech as speechsdk


# Transcribes the given audio file using Azure Speech SDK.
#     Parameters:
#         audio_file_path (str): Path to the audio file.
#         subscription_key (str): Azure Speech service subscription key.
#         region (str): Azure service region (e.g., "eastus").
#         language (str): Language of the audio (default is "en-US").
#     Returns:
#         str: Transcribed text from the audio file.
def transcribe_audio_file(audio_file_path: str, subscription_key: str, region: str, language: str = "en-US") -> str:
    # Set up the speech configuration with your subscription key and region
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_recognition_language = language

    # Set up the audio configuration pointing to the audio file
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)

    # Create a speech recognizer with the given configurations
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Perform speech recognition
    result = speech_recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return f"Speech Recognition canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}"
