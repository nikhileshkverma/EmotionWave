# EmotionWave — Emotion-Sensitive Voice Chatbot

Welcome to **EmotionWave**, a modern voice-enabled chatbot that detects user emotions and responds empathetically. It combines voice recognition, natural language understanding, and AI-powered responses in a sleek, user-friendly interface.

---

## 🌟 Project Overview

EmotionWave is an AI-powered chatbot that:

- Listens to voice input using Speech-to-Text
- Detects emotions using a fine-tuned AI model
- Responds empathetically using text and voice
- Provides a modern, mobile-friendly interface

---

## 🛠️ Key Features

- 🎤 Voice Input (Web Speech API)
- 🔊 Voice Output (SpeechSynthesis)
- 🧠 Emotion Detection using AI
- 💬 Empathetic AI responses
- ✨ Glassmorphism UI design
- 📱 Mobile responsive interface

---

## 🧰 Technology Stack

Frontend  
- React.js  
- Tailwind CSS  

Backend  
- FastAPI (Python)

AI / APIs  
- OpenAI GPT-4o-mini (fine-tuned)

Deployment  
- Static frontend hosting
- Containerized or serverless backend

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/nikhileshkverma/EmotionWave.git
cd EmotionWave
````

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

App runs at:

```
http://localhost:3000
```

---

### Backend Setup

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

## 📂 Project Structure

```
EmotionWave
│
├── backend
├── frontend
├── scripts
├── notebooks
├── data
├── docs
├── README.md
└── requirements.txt
```

---

## 🚀 Future Improvements

* Typing animation for responses
* Multi-language voice support
* Fullscreen mobile chat mode
* Deployment to AWS / Vercel
* User feedback learning pipeline

---

## 🙏 Acknowledgements

* OpenAI
* Unsplash (background images)
* React Icons

---

⭐ If you like this project, consider giving it a star!

````

---

# Then Save and Push

Run:

```bash
git add README.md
git commit -m "Fix README merge conflicts"
git push origin main
````
