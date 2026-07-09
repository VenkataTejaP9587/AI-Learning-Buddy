## ════════════════════════════════════════════════════════
## AI LEARNING BUDDY — Google Colab Deployment Notebook
## Run each cell in order (Shift+Enter)
## ════════════════════════════════════════════════════════

## ── CELL 1: Install Dependencies ──────────────────────
# !pip install -q streamlit pyngrok google-generativeai

## ── CELL 2: Write the app to app.py ──────────────────
# (Run %%writefile app.py followed by the full app code below)

APP_CODE = '''
import streamlit as st
import google.generativeai as genai

# ── Gemini Setup ─────────────────────────────────────────────────────────────
# IMPORTANT: Replace the string below with your actual Gemini API key
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ── Prompt Templates ─────────────────────────────────────────────────────────
PROMPTS = {
    "Explain Concept": lambda topic: f"""You are BinaryBot, a patient and encouraging AI tutor.
Explain {topic} in simple language for a complete beginner.
Structure: 1. One-sentence definition  2. Core idea with an analogy  3. Step-by-step breakdown.
Keep it warm, clear, and jargon-free.""",

    "Real-Life Example": lambda topic: f"""You are BinaryBot, a patient AI tutor.
Give ONE vivid real-life example that demonstrates {topic} in everyday life.
Format: Scene / How {topic} applies / Key takeaway.""",

    "Generate Quiz": lambda topic: f"""You are BinaryBot, an expert quiz generator.
Create a 5-question MCQ quiz on {topic}.
For each question: write the question, 4 options (A-D), mark the correct answer with checkmark, 
and give a 1-sentence explanation.""",

    "Evaluate My Answer": lambda topic, q, a: f"""You are BinaryBot, a constructive AI tutor.
Topic: {topic} | Question: {q} | Student answer: {a}
1. Correct or incorrect? State clearly.
2. If wrong, explain the right answer simply.
3. Give one encouraging tip. Be warm and specific.""",

    "Full Session": lambda topic: f"""You are BinaryBot, an enthusiastic AI tutor.
Run a complete learning session on: {topic}
1. Greet warmly  2. Explain simply  3. Give a real-life example  
4. Ask one comprehension question  5. Mini 3-question quiz with answers  6. Encouraging close.""",
}

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Learning Buddy", page_icon="🎓", layout="wide")

st.markdown("""
<style>
@import url(\'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap\');
html, body, [data-testid="stAppViewContainer"] {
    background: #0f1117 !important; color: #e8eaf6 !important;
    font-family: \'Inter\', sans-serif !important;
}
[data-testid="stSidebar"] { background: #12152a !important; }
.stButton > button {
    background: linear-gradient(135deg,#4f8ef7,#7c5cfc) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important; width: 100%;
}
.resp { background:#1a1d27; border:1px solid rgba(127,142,255,.2);
    border-radius:14px; padding:1.5rem; margin-top:1rem; line-height:1.75; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 AI Learning Buddy")
st.caption("Powered by Gemini 2.5 Flash — Your patient, encouraging AI tutor")

with st.sidebar:
    st.markdown("## 🎯 Topic")
    topic = st.text_input("Enter any topic", value="Binary Search", key="topic")
    st.markdown("---")
    st.markdown("""**BinaryBot** is a patient AI tutor that:\\n
- Explains concepts simply\\n- Gives real-life examples\\n
- Generates quizzes\\n- Evaluates your answers""")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📖 Explain","🌍 Example","📝 Quiz","💬 Ask Anything","🚀 Full Session"])

with tab1:
    st.markdown("#### Explain a Concept")
    if st.button("✨ Explain Now", key="b1"):
        if topic:
            with st.spinner("Thinking…"):
                r = model.generate_content(PROMPTS["Explain Concept"](topic))
                st.markdown(f\'<div class="resp">{r.text}</div>\', unsafe_allow_html=True)
        else:
            st.warning("Enter a topic in the sidebar.")

with tab2:
    st.markdown("#### Real-Life Example")
    if st.button("🌍 Get Example", key="b2"):
        if topic:
            with st.spinner("Finding example…"):
                r = model.generate_content(PROMPTS["Real-Life Example"](topic))
                st.markdown(f\'<div class="resp">{r.text}</div>\', unsafe_allow_html=True)
        else:
            st.warning("Enter a topic in the sidebar.")

with tab3:
    st.markdown("#### Interactive Quiz")
    if st.button("🎲 Generate Quiz", key="b3"):
        if topic:
            with st.spinner("Generating quiz…"):
                r = model.generate_content(PROMPTS["Generate Quiz"](topic))
                st.session_state["quiz"] = r.text
                st.markdown(f\'<div class="resp">{r.text}</div>\', unsafe_allow_html=True)
        else:
            st.warning("Enter a topic in the sidebar.")
    if st.session_state.get("quiz"):
        st.markdown("---")
        q = st.text_area("Paste a question here", key="q_input", height=70)
        a = st.text_area("Your answer", key="a_input", height=70)
        if st.button("✅ Evaluate", key="b_eval"):
            if q and a:
                with st.spinner("Evaluating…"):
                    r = model.generate_content(PROMPTS["Evaluate My Answer"](topic, q, a))
                    st.markdown(f\'<div class="resp">{r.text}</div>\', unsafe_allow_html=True)

with tab4:
    st.markdown("#### Ask BinaryBot Anything")
    question = st.text_area("Your question", height=90, key="fq")
    if st.button("🚀 Send", key="b4"):
        if topic and question:
            with st.spinner("Composing reply…"):
                p = f"You are BinaryBot, a knowledgeable tutor on {topic}. Student asks: {question}. Answer clearly in 3-5 sentences, then ask a follow-up question."
                r = model.generate_content(p)
                st.markdown(f\'<div class="resp">{r.text}</div>\', unsafe_allow_html=True)
        else:
            st.warning("Fill in topic and question.")

with tab5:
    st.markdown("#### Full Learning Session")
    if st.button("▶️ Start Session", key="b5"):
        if topic:
            with st.spinner("Preparing your session…"):
                r = model.generate_content(PROMPTS["Full Session"](topic))
                st.markdown(f\'<div class="resp">{r.text}</div>\', unsafe_allow_html=True)
        else:
            st.warning("Enter a topic in the sidebar.")

st.markdown("---")
st.caption("🎓 AI Learning Buddy | Built with Streamlit & Gemini 2.5 Flash")
'''

print("App code ready. Proceed to next cell.")

## ── CELL 3: Write app.py (run this cell as-is) ───────────────────────────────
# with open("app.py", "w") as f:
#     f.write(APP_CODE)
# print("✅ app.py written successfully!")

## ── CELL 4: Start Streamlit in background ────────────────────────────────────
# import subprocess, time
# subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8501"])
# time.sleep(10)
# print("✅ Streamlit server started on port 8501")

## ── CELL 5: Expose via ngrok ─────────────────────────────────────────────────
# from pyngrok import ngrok
# ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN_HERE")   # ← Replace this!
# public_url = ngrok.connect(8501)
# print(f"🌐 Your public app URL: {public_url}")
# print("Open the link above in a new browser tab!")
