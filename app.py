import os
import re
import json
import random
import nltk
import openai
import requests
from datetime import datetime, timezone
from nltk.corpus import wordnet
from spellchecker import SpellChecker
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Suppress warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

from transformers import pipeline
import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("tf_keras").setLevel(logging.ERROR)

# Get the base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Initialize Flask app
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')
CORS(app)

# Load API Keys
# Try loading from .env file first, then fall back to environment variables
# This works both locally (with API.env) and on Railway (with injected env vars)
api_env_path = os.path.join(BASE_DIR, "API.env")
if os.path.exists(api_env_path):
    load_dotenv(api_env_path)
else:
    load_dotenv()  # Try loading from any .env file

# Get API keys from environment (works for both local and Railway deployment)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Initialize components
spell = SpellChecker()
history = []

# Emotion model - loaded lazily on first use to avoid startup delays
emotion_model = None
emotion_model_loading = False

def load_emotion_model():
    """Load emotion detection model on first use"""
    global emotion_model, emotion_model_loading
    if emotion_model is not None:
        return emotion_model
    if emotion_model_loading:
        return None  # Model is currently loading
    
    emotion_model_loading = True
    try:
        print("Loading emotion detection model...")
        model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
        emotion_model = model
        print("Emotion model loaded ✅")
        return model
    except Exception as e:
        print(f"Error loading emotion model: {e}")
        emotion_model = None
        return None
    finally:
        emotion_model_loading = False

# Load responses
responses_path = os.path.join(BASE_DIR, "responses.json")
try:
    with open(responses_path, 'r') as f:
        responses = json.load(f)
    print("Responses loaded successfully ✅")
except FileNotFoundError:
    responses = {"bye": ["Goodbye!"], "neutral": ["I'm listening. Tell me more."]}
    print("responses.json not found — using fallback responses.")

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

# Utility Functions
def log_conversation(user_message, bot_response, log_file='chat_log.jsonl'):
    """Log conversation to file"""
    log_path = os.path.join(BASE_DIR, log_file)
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_message": user_message,
        "bot_response": bot_response
    }
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + "\n")

def detect_emotion(text):
    """Detect emotion in text"""
    model = load_emotion_model()
    if not model:
        return "neutral"
    try:
        result = model(text)[0]
        return result['label'].lower()
    except Exception as e:
        print("Emotion detection error:", e)
        return "neutral"

def get_perplexity_response(user_input):
    """Get response from Perplexity API"""
    if not PERPLEXITY_API_KEY:
        return None

    try:
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "You are a helpful and friendly assistant."},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"Perplexity API error: {response.status_code}")
            return None
    except Exception as e:
        print("Perplexity API exception:", e)
        return None

def get_openai_fallback(user_input):
    """Get response from OpenAI API as fallback"""
    if not OPENAI_API_KEY:
        return "Sorry, I'm unable to respond right now."

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly and empathetic chatbot."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI fallback error:", e)
        return "I'm here, but having trouble understanding. Could you try rephrasing?"

def chatbot_response(user_input):
    """Core chatbot response logic"""
    user_input_clean = re.sub(r'[^\w\s]', '', user_input.lower())
    tokens = [spell.correction(word) for word in nltk.word_tokenize(user_input_clean)]

    history.append(user_input.lower())
    response_found = False
    bot_reply = None

    # Check for keyword matches
    for word in tokens:
        if word in responses:
            bot_reply = random.choice(responses[word])
            response_found = True
            break

    # Check synonyms if no direct match
    if not response_found:
        for word in tokens:
            syns = wordnet.synsets(word)
            for syn in syns:
                for lemma in syn.lemmas():
                    lemma_name = lemma.name().lower()
                    if lemma_name in responses:
                        bot_reply = random.choice(responses[lemma_name])
                        response_found = True
                        break
                if response_found:
                    break
            if response_found:
                break

    # Use API if no keyword match found
    if not response_found:
        bot_reply = get_perplexity_response(user_input)
        if not bot_reply:
            bot_reply = get_openai_fallback(user_input)

    return bot_reply

# API Routes
@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Handle goodbye
        if user_input.lower() == "bye":
            bot_reply = random.choice(responses.get("bye", ["Goodbye! Take care."]))
            log_conversation(user_input, bot_reply)
            return jsonify({
                'response': bot_reply,
                'emotion': 'neutral'
            })

        # Detect emotion
        emotion = detect_emotion(user_input)
        
        # Check if emotion has a specific response
        if emotion in responses:
            bot_reply = random.choice(responses[emotion])
        else:
            # Use core chatbot logic
            bot_reply = chatbot_response(user_input)

        # Log conversation
        log_conversation(user_input, bot_reply)

        return jsonify({
            'response': bot_reply,
            'emotion': emotion
        })

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'An error occurred processing your message'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'emotion_model_loaded': emotion_model is not None,
        'emotion_model_available': load_emotion_model() is not None
    })

if __name__ == '__main__':
    # Railway provides PORT env variable, default to 5000 for local development
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

