# EmotiveVoice — Emotion-Sensitive Voice Chatbot

Welcome to **EmotiveVoice**, a modern, voice-enabled, emotion-sensitive chatbot application. It blends voice recognition, natural language understanding, and empathetic response generation into a sleek, user-friendly experience.

---

## 🌟 Project Overview

**EmotiveVoice** is an AI-powered chatbot that:

* Listens to your voice input (Speech-to-Text)
* Understands your emotions using a fine-tuned OpenAI model
* Responds empathetically through text and voice (Text-to-Speech)
* Offers a polished, mobile-responsive UI with modern glassmorphism design

---

## 🛠️ Key Features

* **Voice Input:** Speech-to-Text via Web Speech API
* **Voice Output:** Text-to-Speech via Web SpeechSynthesis
* **Emotion Detection & Response:** Custom fine-tuned GPT model
* **Modern UI:** Glassmorphism design for a sleek look
* **Responsive Design:** Mobile-optimized interface
* **Dynamic Background:** Changes according to voice theme
* **Attention Grabber:** Tooltip — “Click me to chat!”

---

## 🧰 Technology Stack

* **Frontend:** React.js, Tailwind CSS
* **Backend:** FastAPI (Python)
* **APIs:** OpenAI GPT-4o-mini (fine-tuned for emotion classification)
* **Deployment:** Static host for frontend + containerized or serverless backend

---

## ⚙️ Installation & Setup

### Clone the repository

```bash
git clone https://github.com/your-username/emotivevoice-chatbot.git
cd emotivoice-chatbot/frontend
```

### Install Frontend Dependencies

```bash
npm install
npm start
```

> The React app will launch at [http://localhost:3000](http://localhost:3000)

### Setup and Start Backend

```bash
cd ../backend
python3.11 -m venv .venv
source .venv/bin/activate  # For Linux/macOS
.venv\Scripts\activate     # For Windows
pip install -r requirements.txt
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

> The FastAPI server will listen at [http://localhost:8000](http://localhost:8000)

### Proxy Configuration

Ensure the frontend proxies `/chat` and `/classify` to `http://localhost:8000` (see `package.json` proxy setting).

---

## 📂 Folder Structure

```
EmotiveVoice/
├── backend/
│   ├── app.py
│   ├── models.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── ChatApp.jsx
│   │   ├── index.js
│   │   └── index.css
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── package.json
├── data/
│   └── Images/what-are-chatbots.jpg
├── scripts/
│   ├── convert_to_jsonl.py
│   ├── split_dataset.py
│   └── prepare_finetune_data.py
├── .env
├── README.md
└── LICENSE
```

---

## 🎨 Customization Options

* **Background Image:** Replace `public/images/what-are-chatbots.jpg` or update the URL in `ChatApp.jsx`
* **Project Branding:** Modify the header title, chat button icon, and tooltip text in `ChatApp.jsx`
* **Emotion Labels:** Customize the list of emotions in `backend/app.py` or training scripts

---

## 🖼️ Screenshots

*(Include some screenshots of the app interface here)*

---

## 🚀 Roadmap & Future Enhancements

* Typing animation for bot responses
* Fullscreen chat mode on mobile devices
* Multi-language voice support
* Live deployment on Vercel, AWS, or Azure
* User feedback analytics and model retraining pipeline

---

## 🙏 Acknowledgments

* Background images from [Unsplash](https://unsplash.com)
* Iconography via `react-icons` (FontAwesome)
* Powered by OpenAI GPT models

Thank you for using **EmotiveVoice** — your voice-driven, empathetic conversational companion!
