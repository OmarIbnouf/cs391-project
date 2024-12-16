from flask import Flask, render_template, jsonify, request, session
from dotenv import load_dotenv
import os
import openai
import base64
from werkzeug.utils import secure_filename
import tempfile

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'secret_key_for_sessions'

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Card data for gallery
cards = [
    {"id": 1, "name": "Pele Card", "price": "$50", "image": "/static/images/pele-card.jpg"},
    {"id": 2, "name": "Messi Card", "price": "$75", "image": "/static/images/messi-card.jpg"}
]

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# API route to get gallery cards
@app.route('/api/cards', methods=['GET'])
def get_cards():
    return jsonify(cards)

# Generate Pele Card using DALL·E
@app.route('/api/generate-pele-card', methods=['POST'])
def generate_pele_card():
    prompt = "A vintage trading card featuring Pele in Brazil's yellow jersey with detailed soccer stats."
    response = openai.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
    return jsonify({"url": response.data[0].url})

# Generate Messi Card using DALL·E
@app.route('/api/generate-messi-card', methods=['POST'])
def generate_messi_card():
    prompt = "A vintage trading card featuring Lionel Messi in Argentina's blue and white jersey with soccer stats."
    response = openai.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
    return jsonify({"url": response.data[0].url})

# Whisper API for audio transcription
@app.route('/api/transcribe-audio', methods=['POST'])
def transcribe_audio():
    audio = request.files['audio']
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    audio.save(temp_file.name)

    with open(temp_file.name, "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)
    os.unlink(temp_file.name)
    return jsonify({"transcription": response['text']})

# Vision API for image analysis
@app.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    image = request.files['image']
    base64_image = base64.b64encode(image.read()).decode('utf-8')

    response = openai.Image.create_edit(
        image=base64_image,
        prompt="Extract text and analyze this trading card.",
        n=1,
        size="1024x1024"
    )
    return jsonify({"analysis": response.data[0]['url']})

# Assistants API: Chatbot interaction
@app.route('/api/ask-chatbot', methods=['POST'])
def ask_chatbot():
    user_message = request.json['message']
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Answer as a soccer trading card assistant: {user_message}",
        max_tokens=150
    )
    return jsonify({"reply": response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(debug=True)
