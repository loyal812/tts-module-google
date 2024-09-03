from google.cloud import texttospeech

def tts(text):
    credentials_file = "config/credentials_file.json"
    
    client = texttospeech.TextToSpeechClient.from_service_account_json(credentials_file)

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    file_name = "output.mp3"

    with open(file_name, "wb") as file:
        file.write(response.audio_content)
        print(f"Audio content written to file {file_name}")

tts("this is test")