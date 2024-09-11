import os
from flask import Flask, render_template, request, send_file
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    recognition_result = recognize_speech(file)

    return render_template('index.html', recognition_result=recognition_result)

@app.route('/download', methods=['POST'])
def download():
    text = request.form.get('text')
    if not text:
        return "No text provided"

    file_path = 'recognized_text.txt'
    with open(file_path, 'w') as file:
        file.write(text)

    return send_file(file_path, as_attachment=True)

def recognize_speech(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

if __name__ == '__main__':
    app.run(debug=True)
