import os
import re
import json
import time
import random
import nltk
import openai
import pyttsx3
import requests
import speech_recognition as sr
from datetime import datetime, timezone
from nltk.corpus import wordnet
from spellchecker import SpellChecker

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("tf_keras").setLevel(logging.ERROR)

from transformers import pipeline
from dotenv import load_dotenv

# ================== Load API Keys ==================
load_dotenv("C:\\Nitesh\\Git work\\chat-bot\\API.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# ================== Init Components ==================
spell = SpellChecker()
history = []
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Load emotion detection model
print("Loading emotion detection model...")
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
print("Emotion model loaded ✅")

# ================== Load Responses ==================
try:
    with open('C:\\Nitesh\\Git work\\chat-bot\\responses.json', 'r') as f:
        responses = json.load(f)
except FileNotFoundError:
    responses = {"bye": ["Goodbye!"], "neutral": ["I'm listening. Tell me more."]}
    print("responses.json not found — using fallback responses.")

# ================== Utility Functions ==================
def speak(text):
    tts_engine = pyttsx3.init()
    tts_engine.say(text)
    tts_engine.runAndWait()

def bot_typing():
    print("Bot is typing...", end="", flush=True)
    time.sleep(1.2)
    print("\r" + " " * 20 + "\r", end="")

def log_conversation(user_message, bot_response, log_file='chat_log.jsonl'):
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_message": user_message,
        "bot_response": bot_response
    }
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + "\n")

def detect_emotion(text):
    try:
        result = emotion_model(text)[0]
        return result['label'].lower()
    except Exception as e:
        print("Emotion detection error:", e)
        return "neutral"

# ================== Perplexity API ==================
def get_perplexity_response(user_input):
    if not PERPLEXITY_API_KEY:
        print("Perplexity API key missing!")
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
            print(f"Perplexity API error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print("Perplexity API exception:", e)
        return None

# ================== OpenAI Fallback ==================
def get_openai_fallback(user_input):
    if not OPENAI_API_KEY:
        print("OpenAI API key missing!")
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

# ================== Core Response Logic ==================
def chatbot_response(user_input, use_speech=True):
    user_input_clean = re.sub(r'[^\w\s]', '', user_input.lower())
    tokens = [spell.correction(word) for word in nltk.word_tokenize(user_input_clean)]

    history.append(user_input.lower())
    response_found = False

    for word in tokens:
        if word in responses:
            bot_reply = random.choice(responses[word])
            if not use_speech:
                bot_typing()
            print("\nBot:", bot_reply)
            if use_speech:
                speak(bot_reply)
            log_conversation(user_input, bot_reply)
            response_found = True
            break

    if not response_found:
        for word in tokens:
            syns = wordnet.synsets(word)
            for syn in syns:
                for lemma in syn.lemmas():
                    lemma_name = lemma.name().lower()
                    if lemma_name in responses:
                        bot_reply = random.choice(responses[lemma_name])
                        if not use_speech:
                            bot_typing()
                        print("\nBot:", bot_reply)
                        if use_speech:
                            speak(bot_reply)
                        log_conversation(user_input, bot_reply)
                        response_found = True
                        break
                if response_found:
                    break
            if response_found:
                break

    # ========== Perplexity (Primary) + OpenAI (Fallback) ==========
    if not response_found:
        bot_reply = get_perplexity_response(user_input)
        if not bot_reply:
            bot_reply = get_openai_fallback(user_input)

        if not use_speech:
            bot_typing()
        print("\nBot:", bot_reply)
        if use_speech:
            speak(bot_reply)
        log_conversation(user_input, bot_reply)

# ================== Voice Input ==================
def get_audio_input():
    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError:
        print("Speech service unavailable.")
        return None

# ================== Chat Interface ==================
print("\nWelcome! You can chat by typing or speaking.")
mode = ''
while mode not in ['full', 'text']:
    mode = input("Choose chat mode:\n"
                 "  type 'full' for voice input/output\n"
                 "  or 'text' for typing only\n"
                 "Your choice: ").strip().lower()

use_speech = (mode == 'full')
print(f"Chat mode set to '{mode}'. Say or type 'bye' to exit.\n")

initial_bot_message = "Hello! I'm here if you need someone to talk to."
if not use_speech:
    bot_typing()
print("Bot:", initial_bot_message)
if use_speech:
    speak(initial_bot_message)
log_conversation("", initial_bot_message)

# ================== Main Chat Loop ==================
try:
    while True:
        if use_speech:
            user_input = get_audio_input()
            if user_input is None:
                user_input = input("Please type your message: ")
        else:
            user_input = input("Type your message: ")

        if user_input.lower() == "bye":
            bot_reply = random.choice(responses.get("bye", ["Goodbye! Take care."]))
            if not use_speech:
                bot_typing()
            print("\nBot:", bot_reply)
            if use_speech:
                speak(bot_reply)
            log_conversation(user_input, bot_reply)
            break

        emotion = detect_emotion(user_input)
        print(f"(Detected emotion: {emotion})")

        if emotion in responses:
            bot_reply = random.choice(responses[emotion])
            if not use_speech:
                bot_typing()
            print("\nBot:", bot_reply)
            if use_speech:
                speak(bot_reply)
            log_conversation(user_input, bot_reply)
        else:
            chatbot_response(user_input, use_speech=use_speech)

except KeyboardInterrupt:
    print("\nBot: Take care! Exiting chat.")
