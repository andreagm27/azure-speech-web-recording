from flask import Flask, render_template, request, send_file
import azure.cognitiveservices.speech as speechsdk
import tempfile
import os
import subprocess
import time

app = Flask(__name__)

AZURE_KEY = "YOUR_KEY"
AZURE_REGION = "YOUR_REGION"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return 'No audio file uploaded', 400

    file = request.files['audio']
    temp_webm = tempfile.mktemp(suffix='.webm')
    temp_wav = tempfile.mktemp(suffix='.wav')
    file.save(temp_webm)

    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', temp_webm,
        '-ac', '1',
        '-ar', '16000',
        '-f', 'wav',
        temp_wav
    ]
    try:
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        os.remove(temp_webm)
        return "FFmpeg conversion failed", 500
    os.remove(temp_webm)

    speech_config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=temp_wav)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = recognizer.recognize_once()
    recognized_text = result.text if result.reason == speechsdk.ResultReason.RecognizedSpeech else None
    time.sleep(0.2)

    try:
        os.remove(temp_wav)
    except PermissionError:
        print("Warning: could not delete temporary file.")

    if recognized_text:
        return recognized_text
    else:
        return "Speech not recognized", 500

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    text = request.form.get('text', '')
    voice = request.form.get('voice', 'es-ES-ElviraNeural')
    if not text:
        return 'Empty text', 400

    speech_config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION)
    speech_config.speech_synthesis_voice_name = voice

    temp_path = tempfile.mktemp(suffix=".wav")
    audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result is not None and result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return send_file(temp_path, mimetype="audio/wav", as_attachment=False)
    else:
        return "Speech synthesis error", 500

if __name__ == '__main__':
    app.run(debug=True)
