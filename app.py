from flask import Flask, request
from flask_cors import CORS, cross_origin
import dotenv
import os
from utils import Utils
from datetime import datetime
from google.cloud import texttospeech

app = Flask(__name__)
CORS(app) #, support_credentials=True

dotenv.load_dotenv()

@app.route('/v2')
@cross_origin()
def test():
    return "TTS module server Python API"

@app.route('/v2/get_model_list')
@cross_origin()
def get_model_list():
    Utils.get_model_list()
    return "Success"

@app.route('/v2/set_config', methods=['POST'])
@cross_origin()
def set_config():
    try:
        gender = request.form['gender']
        model = request.form['model']
        rate = request.form['rate']
        # gender = request.json['gender']
        # model = request.json['model']
        # rate = request.json['rate']
    except KeyError as err:
        return f'Error: {err} is missing', 400

    try:
        with open('config/config.txt', 'w') as f:
            f.write(gender + " " + model + " " + rate)
    except IOError as err:
        return f'Error: {err}', 500

    return "Success", 200

@app.route('/v2/tts', methods=['POST'])
@cross_origin()
def tts():
    # get the text from discord new msg from node server
    text = request.json['text']
    print(text)

    # Open the file for reading
    with open('config/config.txt', 'r') as f:
        # Read the contents of the file
        data = f.read()
        # Print the contents of the file
        # print(data.split(" "))
        # print(data.split(" ")[0])
        # print(data.split(" ")[1])
        # print(data.split(" ")[2])

        gender = data.split(" ")[0].lower()
        model = data.split(" ")[1]
        rate = float(data.split(" ")[2])

    print("-----------------start------------------")
    current_dateTime = datetime.now()

    lang = "en-US"
    if gender.lower() == 'female':
        voice = texttospeech.SsmlVoiceGender.FEMALE
    else:
        voice = texttospeech.SsmlVoiceGender.MALE

    audio = Utils.synthesize_speech(text, lang, voice, model, rate)
    timestamp = current_dateTime.strftime("%Y-%m-%d_%H%M%S_%f")
    with open(f"output/{timestamp}_{gender}_{model}_{rate}_output.mp3", "wb") as f:
        f.write(audio)

    return text

@app.route('/v2/generate_test_audio', methods=['POST'])
@cross_origin()
def generate_test_audio():
    # get the text from discord new msg from node server
    gender = request.form['gender'].lower()
    model = request.form['model']
    rate = float(request.form['rate'])
    text = "Hi, This is test audio file."

    print("-----------------start------------------")
    current_dateTime = datetime.now()

    lang = "en-US"
    if gender.lower() == 'female':
        voice = texttospeech.SsmlVoiceGender.FEMALE
    else:
        voice = texttospeech.SsmlVoiceGender.MALE

    audio = Utils.synthesize_speech(text, lang, voice, model, rate)
    timestamp = current_dateTime.strftime("%Y-%m-%d_%H%M%S_%f")
    file_name = f"output/test_{timestamp}_{gender}_{model}_{rate}_output.mp3"
    with open(file_name, "wb") as f:
        f.write(audio)

    return file_name, 200

app.run(host='0.0.0.0', port=os.environ.get("PORT"))