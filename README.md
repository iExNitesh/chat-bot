# 🤖 Emotion-Aware Chatbot - Web Application

An intelligent **emotion-aware chatbot** with a modern web interface. Built with Python Flask backend and vanilla JavaScript frontend. It can **detect emotions**, respond empathetically using **Perplexity AI** and **OpenAI** APIs, and is ready for deployment to share with anyone!

## ✨ Features

- 🧠 **Emotion Detection:** Uses Hugging Face model to detect emotions in text
- 🌐 **Modern Web Interface:** Beautiful, responsive chat UI
- 🤖 **Hybrid AI Logic:** Combines keyword responses, synonym matching, and large language model APIs
- 🔄 **Fallback Handling:** Uses **Perplexity AI** primarily, and **OpenAI GPT** as a backup
- 💾 **Conversation Logging:** Automatically saves chats with timestamps
- ✍️ **Spell Correction:** Fixes common typing errors with `pyspellchecker`
- 📱 **Responsive Design:** Works perfectly on desktop, tablet, and mobile
- 🚀 **Deployment Ready:** Easy to deploy to platforms like Heroku, Railway, or Render

---

## 📁 Project Structure

```
chat-bot/
├── app.py              # Flask backend API
├── main.py             # Original CLI chatbot (legacy)
├── responses.json      # Predefined responses for emotions/keywords
├── API.env             # Environment variables (API keys) — not uploaded
├── requirements.txt    # Python dependencies
├── static/             # Frontend files
│   ├── index.html      # Main HTML file
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic
└── README.md           # This file
```

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

### 2️⃣ Set Up API Keys

Create a file named `API.env` in the root folder:

```env
OPENAI_API_KEY=your_openai_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here
```

⚠️ **Important:** Do NOT upload this file — add it to `.gitignore`.

### 3️⃣ Run the Web Application

```bash
python app.py
```

The app will start on `http://localhost:5000`. Open this URL in your browser to use the chatbot!

---

## 🎯 Usage

### Web Interface (Text-Only)

> 🗨️ **Note:** The web version (`app.py`) currently supports **text chat only** — voice input is not available in the browser.

1. Start the server: `python app.py`
2. Open `http://localhost:5000` in your browser
3. Type your message and press Enter or click Send
4. The bot will detect your emotions and respond empathetically!

### CLI Chatbot (with Voice Support)

> 🎤 **Voice Feature:** The command-line chatbot (`main.py`) supports **voice input and output**, allowing you to **talk** with the bot instead of typing.

1. Run in your terminal:
   ```bash
   python main.py

### Web Interface

1. Start the server: `python app.py`
2. Open `http://localhost:5000` in your browser
3. Type your message and press Enter or click Send
4. The bot will detect your emotions and respond empathetically!

### API Endpoints

#### `POST /api/chat`
Send a chat message and get a response.

**Request:**
```json
{
  "message": "I'm feeling sad today"
}
```

**Response:**
```json
{
  "response": "I'm really sorry you're feeling this way. Want to talk about it?",
  "emotion": "sadness"
}
```

#### `GET /api/health`
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "emotion_model_loaded": true
}
```

---

## 🛠️ Technologies Used

- **Backend:**
  - Python 3.10+
  - Flask (Web Framework)
  - Transformers (Hugging Face) - Emotion Detection
  - OpenAI API
  - Perplexity AI API
  - NLTK (Natural Language Processing)
  - PySpellChecker

- **Frontend:**
  - HTML5
  - CSS3 (Modern Design)
  - Vanilla JavaScript (No frameworks!)

---

## 📝 Notes

- The emotion detection model will be downloaded automatically on first run (can take a few minutes)
- Make sure you have stable internet connection for API calls
- Chat logs are saved in `chat_log.jsonl` file
- The original CLI version (`main.py`) is still available if you prefer terminal-based interaction

---

## 🔒 Security

- Never commit `API.env` or `.env` files to version control
- Use environment variables in production deployments
- Consider adding rate limiting for production use

---

## 📄 License

This project is open-source under the MIT License.

---

## 👤 Author

Developed by **Nitesh** — A personal project exploring emotional AI assistants with modern web technologies.

---

## 🎉 Key Features

**Project Highlights:**
- ✅ Full-stack web application (Flask + JavaScript)
- ✅ RESTful API design
- ✅ Emotion detection using machine learning
- ✅ Integration with multiple AI APIs
- ✅ Responsive and modern UI/UX
- ✅ Production-ready deployment
- ✅ Real-time chat interface

Perfect for showcasing your Python, web development, and AI/ML skills!

---

## 🌐 Deployment

Want to deploy your chatbot online for free? Get a professional URL to share on your resume or with others!

**📖 Complete deployment guide available: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)**

### Quick Deployment Steps:
1. **Push your code to GitHub** (if not already done)
2. **Sign up on Render.com** (free tier - perfect for portfolios)
3. **Connect your GitHub repository**
4. **Set environment variables** (OPENAI_API_KEY, PERPLEXITY_API_KEY)
5. **Deploy!** Get your URL: `https://your-app.onrender.com`

**Recommended Platform:** **Render.com** - Free tier, professional URLs, auto-deploy from GitHub

For detailed step-by-step instructions, see **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)**

---

## 🐛 Troubleshooting

**Issue:** Emotion model not loading
- **Solution:** Ensure you have internet connection for first-time download. The model is ~500MB.

**Issue:** API calls failing
- **Solution:** Check your API keys in `API.env` and ensure they're valid.

**Issue:** Port 5000 already in use
- **Solution:** Change the port in `app.py` or kill the process using port 5000.

---

**Enjoy chatting with your emotion-aware bot! 🚀**
