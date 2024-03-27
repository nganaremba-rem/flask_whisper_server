import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from transcribeAudio import transcribeAudio

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ['http://localhost:3000', 'http://127.0.0.1:3000']}})

@app.route('/', methods=['GET', 'POST'])
def indexRoute():
     # Specifying the file path 
    return 'Server is running!'

@app.post('/api/transcribe')
def transcribeRoute():
    # Check if audio file is missing
    if 'audio_file' not in request.files:
        return jsonify({"error": "Audio file is missing!"}), 400
    
    language = "ja" # Default language Japanese
    
    # If language is set change the default language
    if 'language' in request.form:
        language = request.form['language']
    
    
    # Get the audio file
    audio_file = request.files['audio_file']
    
    # Check for filename
    if not audio_file.filename:
        return jsonify({"error": "Audio file is missing!"}), 400

    # Extract the extension
    _, extension = os.path.splitext(audio_file.filename)
    
    # Check if the extension is either .wav or .flac
    if extension.lower() not in [".wav", ".flac"]:
        return jsonify({"error": "Only .wav or .flac file extension is supported!"}), 400
    
    # Specifying the file path 
    file_path = os.path.abspath(os.path.join(os.getcwd(), "static/audio/audio"))
    
    print(file_path)

    # Remove the older audio if available
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Save the audio to the file path specified
    try:
        audio_file.save(file_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Transcribe the audio and return the text
    try:
        data = transcribeAudio(audio_url=file_path, language=language)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


