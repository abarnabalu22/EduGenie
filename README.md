# 🧞 EduGenie: Google Gemini Powered Learning Assistant

An AI-powered learning assistant built with **Python, Streamlit and Google Gemini API** as part of the **Naan Mudhalvan** program.

## Features
- 📘 **Explain Topic** – level-based explanations with examples and quick revision
- 📝 **Quiz Generator** – auto MCQs with scoring and explanations
- 🗓️ **Study Plan** – day-by-day personalised plan
- 📄 **Summarizer** – bullet summaries and keywords from your notes
- 💬 **Ask Tutor** – chat-style doubt clearing
- 🌐 Answers in English, Tamil, Hindi, Telugu or Malayalam

## Tech Stack
Python 3.10+ · Streamlit · Google Gemini API (`google-genai`) · python-dotenv

## Setup
```bash
git clone https://github.com/<your-username>/EduGenie.git
cd EduGenie
python -m venv venv
venv\Scripts\activate          # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
```
1. Get a free API key: https://aistudio.google.com/api-keys
2. Copy `.env.example` to `.env` and paste your key (or enter it in the app sidebar).
3. Run:
```bash
streamlit run app.py
```
Open http://localhost:8501

## Project Structure
```
EduGenie/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## How it works
User input → prompt built per feature (topic, level, language) → Gemini API → response rendered in Streamlit. Quiz uses JSON output mode so questions can be graded in the app.

> ⚠️ Never upload your real `.env` / API key to GitHub.
