from google.cloud import texttospeech

class Utils():

    def synthesize_speech(text, lang, gender, model, speaking_rate):
        credentials_file = "config/credentials_file.json"
    
        client = texttospeech.TextToSpeechClient.from_service_account_json(credentials_file)

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang,
            ssml_gender=gender,  # texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED
            name=model
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate  # Set the desired speaking rate here
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return response.audio_content
    
    def get_model_list():
        credentials_file = "config/credentials_file.json"
    
        client = texttospeech.TextToSpeechClient.from_service_account_json(credentials_file)

        voices = client.list_voices().voices

        # Filter by gender
        female_models = []
        male_models = []
        
        for voice in voices:
            if voice.ssml_gender == texttospeech.SsmlVoiceGender.FEMALE:
                female_models.append(voice.name)
            elif voice.ssml_gender == texttospeech.SsmlVoiceGender.MALE:
                male_models.append(voice.name)

        print("Female Models:")
        for model in sorted(female_models):
            print(f"- {model}")

        print("\nMale Models:")
        for model in sorted(male_models):
            print(f"- {model}")

        return "success"