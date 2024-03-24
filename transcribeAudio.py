import whisper

def transcribeAudio(audio_url, language = 'ja'):
    model = whisper.load_model('base')
    result = model.transcribe(audio_url, language=language)
    return result