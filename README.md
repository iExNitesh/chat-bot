# 🎙️ Emotion Chatbot (Voice + Text AI Assistant)

An intelligent **emotion-aware chatbot** built with Python.  
It can **listen, talk, detect emotions**, and respond empathetically using **Perplexity AI** and **OpenAI** APIs.

---

## 🚀 Features

- 🧠 **Emotion Detection:** Uses a Hugging Face model to detect emotions in text.  
- 🗣️ **Speech Recognition & TTS:** Supports voice input and output using `speech_recognition` and `pyttsx3`.  
- 🤖 **Hybrid Logic:** Combines keyword responses, synonym matching, and large language model APIs.  
- 🔄 **Fallback Handling:** Uses **Perplexity AI** primarily, and **OpenAI GPT** as a backup.  
- 💾 **Conversation Logging:** Automatically saves chats with timestamps.  
- ✍️ **Spell Correction:** Fixes common typing errors with `pyspellchecker`.

---

## 🧩 Project Structure

EmotionChatbot/
├── main.py # Main chatbot program
├── responses.json # Predefined responses for emotions/keywords
├── API.env # Environment variables (API keys) — not uploaded
├── requirements.txt # Python dependencies
└── README.md # This file

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/EmotionChatbot.git
cd EmotionChatbot
2️⃣ Install dependencies
It’s recommended to use a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
3️⃣ Add your API keys
Create a file named API.env in the root folder:

ini
Copy code
OPENAI_API_KEY=your_openai_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here
⚠️ Do NOT upload this file — it’s ignored via .gitignore.

🧠 Usage
Option 1 — Text Mode
Run the chatbot in typing mode:

bash
Copy code
python main.py
Then choose text when prompted.

Option 2 — Full Voice Mode
Run with speech input/output:

bash
Copy code
python main.py
Then choose full when prompted.

🧩 Example Interaction
vbnet
Copy code
Choose chat mode:
  type 'full' for voice input/output
  or 'text' for typing only
Your choice: text

Bot: Hello! I'm here if you need someone to talk to.
Type your message: I'm feeling sad today
(Detected emotion: sadness)

Bot: I'm sorry to hear that. Want to talk about it?
💬 Logging
All conversations are saved automatically in chat_log.jsonl with timestamps.

🛠️ Technologies Used
Python 3.10+

Transformers (Hugging Face)

SpeechRecognition

Pyttsx3

OpenAI & Perplexity APIs

WordNet (NLTK)

PySpellChecker

🧾 License
This project is open-source under the MIT License.

🌟 Author
Developed by Nitesh — a personal project exploring emotional AI assistants.

yaml
Copy code

---

Would you like me to also generate a matching **`requirements.txt`** file (so others can install dependencies easily)?