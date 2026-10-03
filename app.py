"""
EduGenie: Google Gemini Powered Learning Assistant
Naan Mudhalvan Project
Run:  streamlit run app.py
"""
import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

st.set_page_config(page_title="EduGenie", page_icon="🧞", layout="wide")


# ---------- Gemini helpers ----------
@st.cache_resource
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


def ask_gemini(client, prompt: str, system: str = "", json_mode: bool = False) -> str:
    config = types.GenerateContentConfig(
        system_instruction=system or None,
        response_mime_type="application/json" if json_mode else "text/plain",
        temperature=0.6,
    )
    response = client.models.generate_content(model=MODEL, contents=prompt, config=config)
    return response.text


TUTOR_SYSTEM = (
    "You are EduGenie, a friendly and accurate AI tutor for students. "
    "Explain clearly, use simple examples, and keep answers well structured."
)

# ---------- Sidebar ----------
st.sidebar.title("🧞 EduGenie")
st.sidebar.caption("Google Gemini Powered Learning Assistant")
api_key = st.sidebar.text_input(
    "Gemini API Key", value=os.getenv("GEMINI_API_KEY", ""), type="password",
    help="Get a free key from https://aistudio.google.com/api-keys",
)
level = st.sidebar.selectbox("Your level", ["Beginner", "Intermediate", "Advanced"])
language = st.sidebar.selectbox("Answer language", ["English", "Tamil", "Hindi", "Telugu", "Malayalam"])

st.title("🧞 EduGenie – Your AI Learning Assistant")

if not api_key:
    st.info("👈 Enter your Gemini API key in the sidebar to begin.")
    st.stop()

client = get_client(api_key)

tab_explain, tab_quiz, tab_plan, tab_summary, tab_chat = st.tabs(
    ["📘 Explain Topic", "📝 Quiz", "🗓️ Study Plan", "📄 Summarizer", "💬 Ask Tutor"]
)

# ---------- 1. Explain ----------
with tab_explain:
    topic = st.text_input("Topic to learn", placeholder="e.g. Photosynthesis, Binary Search, Newton's Laws")
    if st.button("Explain", key="explain") and topic:
        with st.spinner("EduGenie is thinking..."):
            prompt = (
                f"Explain '{topic}' for a {level} learner in {language}. "
                "Include: 1) simple definition, 2) key points, 3) a real-life example, "
                "4) a 3-line quick revision summary."
            )
            st.markdown(ask_gemini(client, prompt, TUTOR_SYSTEM))

# ---------- 2. Quiz ----------
with tab_quiz:
    q_topic = st.text_input("Quiz topic", key="q_topic")
    num_q = st.slider("Number of questions", 3, 10, 5)
    if st.button("Generate Quiz") and q_topic:
        with st.spinner("Creating quiz..."):
            prompt = (
                f"Create {num_q} multiple choice questions on '{q_topic}' for a {level} learner in {language}. "
                'Return ONLY JSON: a list of objects with keys "question", "options" (list of 4 strings), '
                '"answer" (the exact correct option text), "explanation".'
            )
            try:
                st.session_state["quiz"] = json.loads(ask_gemini(client, prompt, json_mode=True))
                st.session_state["quiz_done"] = False
            except Exception as e:
                st.error(f"Could not generate quiz, please try again. ({e})")

    quiz = st.session_state.get("quiz")
    if quiz:
        answers = {}
        for i, q in enumerate(quiz):
            answers[i] = st.radio(f"Q{i+1}. {q['question']}", q["options"], index=None, key=f"qa{i}")
        if st.button("Submit Answers"):
            score = 0
            for i, q in enumerate(quiz):
                correct = answers[i] == q["answer"]
                score += correct
                icon = "✅" if correct else "❌"
                st.write(f"{icon} **Q{i+1}** – Correct answer: {q['answer']}")
                st.caption(q["explanation"])
            st.success(f"Your score: {score} / {len(quiz)}")

# ---------- 3. Study plan ----------
with tab_plan:
    goal = st.text_input("Learning goal", placeholder="e.g. Learn Python basics")
    days = st.slider("Days available", 3, 60, 14)
    hours = st.slider("Hours per day", 1, 8, 2)
    if st.button("Create Study Plan") and goal:
        with st.spinner("Planning..."):
            prompt = (
                f"Create a day-by-day study plan to achieve: '{goal}' in {days} days, "
                f"{hours} hours/day, for a {level} learner. Answer in {language}. "
                "Use a table with columns Day | Topics | Activities | Revision."
            )
            st.markdown(ask_gemini(client, prompt, TUTOR_SYSTEM))

# ---------- 4. Summarizer ----------
with tab_summary:
    text = st.text_area("Paste your notes or text", height=220)
    if st.button("Summarize") and text.strip():
        with st.spinner("Summarizing..."):
            prompt = (
                f"Summarize the following text in {language} for a {level} learner: "
                "5 bullet points, then 3 important keywords with meanings.\n\n" + text
            )
            st.markdown(ask_gemini(client, prompt, TUTOR_SYSTEM))

# ---------- 5. Chat ----------
with tab_chat:
    if "history" not in st.session_state:
        st.session_state["history"] = []
    for role, msg in st.session_state["history"]:
        st.chat_message(role).markdown(msg)
    user_msg = st.chat_input("Ask EduGenie anything about your studies...")
    if user_msg:
        st.chat_message("user").markdown(user_msg)
        convo = "\n".join(f"{r}: {m}" for r, m in st.session_state["history"][-8:])
        prompt = f"{convo}\nuser: {user_msg}\nAnswer in {language} for a {level} learner."
        with st.spinner("Thinking..."):
            reply = ask_gemini(client, prompt, TUTOR_SYSTEM)
        st.chat_message("assistant").markdown(reply)
        st.session_state["history"] += [("user", user_msg), ("assistant", reply)]
