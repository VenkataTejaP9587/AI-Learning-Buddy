# ============================================================
# AI LEARNING BUDDY — GRAND PRIZE EDITION 🏆
# Real-World EdTech Platform | Powered by Google Gemini 2.5
# Features: Multi-turn Chatbot · Real-World Apps · Interview
#   Prep · Study Plan · Flashcards · Code Examples · Gamification
# ============================================================

import streamlit as st
import google.generativeai as genai
import random
from datetime import datetime

# ── API Setup ────────────────────────────────────────────────────────────────
GEMINI_API_KEY = "YOUR_API_KEY_HERE" # Replace with your actual Gemini API key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Learning Buddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── STYLES ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Fira+Code:wght@400;500&family=Space+Grotesk:wght@400;500;600;700;800&display=swap');

:root {
    --bg:      #07090f;
    --bg2:     #0c0e1a;
    --card:    #101422;
    --card2:   #141828;
    --border:  rgba(99,120,255,0.14);
    --border2: rgba(99,120,255,0.28);
    --blue:    #4f8ef7;
    --violet:  #7c5cfc;
    --cyan:    #22d3ee;
    --green:   #34d399;
    --orange:  #f97316;
    --amber:   #fbbf24;
    --pink:    #ec4899;
    --red:     #ef4444;
    --text:    #e2e8f0;
    --muted:   #64748b;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#09090f 0%,#0c0e1a 100%) !important;
    border-right: 1px solid var(--border2) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
#MainMenu, footer { visibility: hidden; }

/* Grid bg */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(79,142,247,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(79,142,247,0.025) 1px, transparent 1px);
    background-size: 56px 56px;
    pointer-events: none; z-index: 0;
}

/* ── Animations ── */
@keyframes gradientMove {
    0%,100% { background-position: 0% 50%; }
    50%      { background-position: 100% 50%; }
}
@keyframes float {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-10px); }
}
@keyframes glow-pulse {
    0%,100% { box-shadow: 0 0 20px rgba(79,142,247,0.15), 0 0 60px rgba(124,92,252,0.08); }
    50%      { box-shadow: 0 0 50px rgba(79,142,247,0.35), 0 0 120px rgba(124,92,252,0.18); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes pop-in {
    0%   { transform: scale(0.8); opacity: 0; }
    70%  { transform: scale(1.05); }
    100% { transform: scale(1);   opacity: 1; }
}
@keyframes slide-up {
    from { transform: translateY(12px); opacity: 0; }
    to   { transform: translateY(0);    opacity: 1; }
}
@keyframes typing {
    0%,100% { opacity: 0.3; }
    50%      { opacity: 1; }
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, rgba(12,14,26,0.8) 0%, rgba(16,20,34,0.85) 45%, rgba(12,14,26,0.8) 100%);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(124,92,252,0.3);
    border-radius: 28px;
    padding: 3rem 2.8rem 2.5rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
    animation: glow-pulse 4s ease-in-out infinite;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
}
.hero::before {
    content:""; position:absolute; top:-90px; right:-90px;
    width:320px; height:320px; border-radius:50%;
    background:radial-gradient(circle, rgba(124,92,252,0.20) 0%, transparent 65%);
    animation: float 7s ease-in-out infinite;
}
.hero::after {
    content:""; position:absolute; bottom:-80px; left:-60px;
    width:260px; height:260px; border-radius:50%;
    background:radial-gradient(circle, rgba(79,142,247,0.16) 0%, transparent 65%);
    animation: float 9s ease-in-out infinite reverse;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.2rem; font-weight: 900;
    background: linear-gradient(135deg,#fff 0%,#c7d2fe 35%,#818cf8 65%,#7c5cfc 100%);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
    margin: 0 0 0.7rem; line-height: 1.1;
    position: relative; z-index: 1;
}
.hero-sub {
    font-size: 1.05rem; color: var(--muted);
    max-width: 580px; line-height: 1.65;
    position: relative; z-index: 1; margin: 0;
}
.hero-tags {
    margin-top: 1.3rem;
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    position: relative; z-index: 1;
}
.hero-tag {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 0.28rem 0.85rem;
    font-size: 0.74rem; color: var(--muted);
    transition: border-color 0.2s, color 0.2s;
}
.hero-tag:hover { border-color: rgba(79,142,247,0.4); color: var(--text); }

/* ── Stats Grid ── */
@keyframes float-stat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
}
.stats-grid {
    display: grid;
    grid-template-columns: repeat(5,1fr);
    gap: 1rem; margin-bottom: 2rem;
}
.stat-card {
    background: linear-gradient(145deg, rgba(20,24,40,0.6), rgba(16,20,34,0.8));
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(99,120,255,0.18);
    border-radius: 20px;
    padding: 1.5rem 1rem; text-align: center;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    animation: slide-up 0.5s ease both, float-stat 6s ease-in-out infinite;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
}
.stat-card:nth-child(2) { animation-delay: 0.1s, 1s; }
.stat-card:nth-child(3) { animation-delay: 0.2s, 2s; }
.stat-card:nth-child(4) { animation-delay: 0.3s, 3s; }
.stat-card:nth-child(5) { animation-delay: 0.4s, 4s; }

.stat-card:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: rgba(124,92,252,0.5);
    box-shadow: 0 15px 45px rgba(124,92,252,0.2), inset 0 1px 0 rgba(255,255,255,0.1);
}
.stat-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.1rem; font-weight: 900; line-height: 1; margin-bottom: 0.3rem;
}
.stat-lbl {
    font-size: 0.7rem; color: var(--muted);
    font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255,255,255,0.025) !important;
    border-radius: 18px !important;
    padding: 0.45rem 0.55rem !important;
    border: 1px solid var(--border2) !important;
    gap: 0.35rem !important;
    display: flex !important; flex-wrap: wrap !important;
    box-shadow: 0 6px 30px rgba(0,0,0,0.4) !important;
}
[data-testid="stTabs"] button[role="tab"] {
    border-radius: 12px !important;
    color: var(--muted) !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.83rem !important;
    padding: 0.52rem 1.05rem !important;
    transition: all 0.22s ease !important;
    border: 1px solid transparent !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stTabs"] button[role="tab"]:hover {
    background: rgba(79,142,247,0.09) !important;
    color: var(--text) !important;
    border-color: rgba(79,142,247,0.22) !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg,#4f8ef7,#7c5cfc) !important;
    color: #fff !important;
    box-shadow: 0 4px 20px rgba(79,142,247,0.4), 0 0 0 1px rgba(124,92,252,0.25) !important;
    border-color: transparent !important;
}

/* ── Inputs ── */
[data-testid="stTextInput"] > div > input,
[data-testid="stTextArea"] > div > textarea,
[data-testid="stSidebar"] [data-testid="stTextInput"] > div > input,
input[type="text"], textarea {
    background: #ffffff !important;
    border: 1.5px solid rgba(99,120,255,0.25) !important;
    border-radius: 11px !important;
    color: #111111 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    caret-color: #111111 !important;
}
[data-testid="stTextInput"] > div > input:focus,
[data-testid="stTextArea"] > div > textarea:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.18) !important;
    background: #ffffff !important; color: #111111 !important;
}
input::placeholder, textarea::placeholder { color: #9ca3af !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg,#4f8ef7,#7c5cfc) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important;
    padding: 0.68rem 1.8rem !important;
    font-size: 0.93rem !important; font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 20px rgba(79,142,247,0.28) !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(79,142,247,0.50) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Response Box ── */
.rbox {
    background: linear-gradient(135deg,var(--card) 0%,#0c0e1a 100%);
    border: 1px solid var(--border2);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    margin-top: 1.1rem;
    font-size: 0.96rem; line-height: 1.82;
    position: relative; overflow: hidden;
    animation: slide-up 0.35s ease;
}
.rbox::before {
    content:""; position:absolute; top:0; left:0; right:0;
    height:3px;
    background:linear-gradient(90deg,var(--blue),var(--violet),var(--cyan));
    border-radius: 20px 20px 0 0;
}
.rbox h1,.rbox h2,.rbox h3 { color:var(--cyan) !important; font-family:'Space Grotesk',sans-serif !important; }
.rbox strong { color: var(--amber) !important; }
.rbox code {
    font-family:'Fira Code',monospace;
    background:rgba(79,142,247,0.12); border:1px solid rgba(79,142,247,0.28);
    border-radius:6px; padding:2px 7px; color:var(--cyan); font-size:0.88em;
}
.rbox pre {
    background:rgba(0,0,0,0.55); border:1px solid var(--border);
    border-radius:14px; padding:1.3rem; overflow-x:auto;
}
.rbox ul,.rbox ol { padding-left:1.6rem; }
.rbox li { margin-bottom:0.38rem; }
.rbox a { color:var(--blue); }

/* ── XP Toast ── */
.xp-toast {
    display:inline-flex; align-items:center; gap:0.4rem;
    background:linear-gradient(90deg,rgba(251,191,36,0.18),rgba(251,191,36,0.06));
    border:1px solid rgba(251,191,36,0.32); border-radius:100px;
    padding:0.4rem 1.1rem; font-size:0.82rem; font-weight:700;
    color:var(--amber); margin-top:0.8rem;
    animation: pop-in 0.4s cubic-bezier(.22,.61,.36,1);
}

/* ── XP bar ── */
.xp-wrap {
    background:var(--card); border:1px solid var(--border);
    border-radius:14px; padding:1rem; margin-bottom:0.9rem;
}
.xp-track {
    background:rgba(255,255,255,0.07); border-radius:100px;
    height:10px; overflow:hidden; margin:0.5rem 0 0.3rem;
}
.xp-fill {
    height:100%; border-radius:100px;
    transition:width 0.9s ease;
}

/* ── Badge ── */
.badge {
    display:inline-flex; align-items:center; gap:0.35rem;
    background:rgba(255,255,255,0.04); border:1px solid var(--border);
    border-radius:100px; padding:0.3rem 0.75rem;
    font-size:0.72rem; color:var(--muted); cursor:help;
    transition:all 0.2s; animation: pop-in 0.4s ease;
}
.badge:hover { border-color:rgba(124,92,252,0.4); color:var(--text); }
.badge-on { color:var(--amber); border-color:rgba(251,191,36,0.35);
    background:rgba(251,191,36,0.07); }

/* ── Note card ── */
.note-card {
    background:var(--card); border:1px solid var(--border);
    border-left:3px solid var(--blue); border-radius:14px;
    padding:1.2rem; margin-bottom:0.8rem;
    transition:border-left-color 0.2s;
}
.note-card:hover { border-left-color:var(--violet); }

/* ── Concept map ── */
.cmap {
    background:rgba(0,0,0,0.55); border:1px solid var(--border2);
    border-radius:18px; padding:1.6rem;
    font-family:'Fira Code',monospace; font-size:0.87rem;
    line-height:1.95; color:var(--cyan);
    white-space:pre-wrap; overflow-x:auto;
}

/* ── Flashcard ── */
.flashcard {
    background:linear-gradient(135deg,var(--card),var(--card2));
    border:1px solid var(--border2); border-radius:18px;
    padding:1.5rem 1.8rem; margin-bottom:1rem;
    border-left:4px solid var(--violet);
    animation: slide-up 0.3s ease;
    transition: transform 0.2s, box-shadow 0.2s;
}
.flashcard:hover {
    transform:translateY(-3px);
    box-shadow:0 10px 30px rgba(124,92,252,0.15);
}
.fc-q { font-weight:700; color:var(--text); font-size:0.96rem; margin-bottom:0.6rem; }
.fc-a { color:var(--green); font-size:0.92rem; line-height:1.6; }
.fc-tip { font-size:0.8rem; color:var(--amber); margin-top:0.5rem; }
.fc-num {
    font-size:0.7rem; font-weight:700; color:var(--violet);
    text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.4rem;
}

/* ── Score card ── */
.score-card {
    background:linear-gradient(135deg,var(--card),var(--card2));
    border:2px solid; border-radius:22px;
    padding:2.2rem; text-align:center; margin-top:1.5rem;
    animation: pop-in 0.5s ease;
}
.score-big {
    font-family:'Space Grotesk',sans-serif;
    font-size:4.5rem; font-weight:900; line-height:1;
}

/* ── Chat bubbles ── */
.chat-wrap { max-height:480px; overflow-y:auto; padding:0.5rem 0; }
.msg-user {
    display:flex; justify-content:flex-end; margin:0.6rem 0;
    animation: slide-up 0.25s ease;
}
.msg-ai {
    display:flex; justify-content:flex-start; margin:0.6rem 0;
    gap:0.6rem; align-items:flex-start;
    animation: slide-up 0.25s ease;
}
.bubble-user {
    background:linear-gradient(135deg,#4f8ef7,#7c5cfc);
    color:#fff; border-radius:20px 20px 4px 20px;
    padding:0.85rem 1.3rem; max-width:72%;
    font-size:0.94rem; line-height:1.65;
    box-shadow:0 4px 18px rgba(79,142,247,0.3);
}
.bubble-ai {
    background:var(--card2); border:1px solid var(--border2);
    color:var(--text); border-radius:20px 20px 20px 4px;
    padding:0.9rem 1.35rem; max-width:76%;
    font-size:0.94rem; line-height:1.7;
    box-shadow:0 4px 18px rgba(0,0,0,0.25);
}
.ai-avatar {
    width:34px; height:34px; border-radius:50%;
    background:linear-gradient(135deg,#4f8ef7,#7c5cfc);
    display:flex; align-items:center; justify-content:center;
    font-size:1.1rem; flex-shrink:0; margin-top:4px;
    box-shadow:0 3px 12px rgba(79,142,247,0.35);
}
.typing-dot {
    display:inline-block; width:7px; height:7px;
    border-radius:50%; background:var(--muted); margin:0 2px;
}
.typing-dot:nth-child(1){animation:typing 1.2s 0s infinite;}
.typing-dot:nth-child(2){animation:typing 1.2s 0.2s infinite;}
.typing-dot:nth-child(3){animation:typing 1.2s 0.4s infinite;}
.chip-row { display:flex; flex-wrap:wrap; gap:0.45rem; margin:0.8rem 0; }
.chip {
    background:rgba(79,142,247,0.1); border:1px solid rgba(79,142,247,0.28);
    border-radius:100px; padding:0.3rem 0.85rem;
    font-size:0.76rem; color:var(--blue); cursor:pointer;
    transition:all 0.18s;
}
.chip:hover { background:rgba(79,142,247,0.2); border-color:rgba(79,142,247,0.5); }

/* ── Industry card ── */
.ind-card {
    background:var(--card); border:1px solid var(--border);
    border-radius:16px; padding:1.3rem 1.5rem; margin-bottom:1rem;
    border-top:3px solid;
    transition:transform 0.2s, box-shadow 0.2s;
}
.ind-card:hover {
    transform:translateY(-4px);
    box-shadow:0 12px 35px rgba(0,0,0,0.3);
}

/* ── Interview Q ── */
.iq-card {
    background:var(--card); border:1px solid var(--border);
    border-radius:16px; padding:1.4rem; margin-bottom:1rem;
    border-left:4px solid;
    animation: slide-up 0.3s ease;
}

/* ── Study week ── */
.week-card {
    background:var(--card); border:1px solid var(--border);
    border-radius:16px; padding:1.3rem 1.5rem; margin-bottom:1rem;
    position:relative; overflow:hidden;
}
.week-num {
    position:absolute; top:1rem; right:1.2rem;
    font-size:3rem; font-weight:900;
    font-family:'Space Grotesk',sans-serif;
    opacity:0.06; color:var(--text);
    line-height:1;
}

/* ── Section ── */
.s-head { font-family:'Space Grotesk',sans-serif; font-size:1.3rem; font-weight:700; color:var(--text); margin-bottom:0.3rem; }
.s-sub  { font-size:0.86rem; color:var(--muted); margin-bottom:1.3rem; }

/* ── Topic tag ── */
.ttag {
    display:inline-block; background:rgba(79,142,247,0.1);
    border:1px solid rgba(79,142,247,0.25); border-radius:100px;
    padding:0.2rem 0.72rem; font-size:0.74rem; color:var(--blue);
    margin:0.2rem; font-weight:500;
}

/* ── Fancy HR ── */
.fhr { border:none; height:1px; background:linear-gradient(90deg,transparent,var(--border2),transparent); margin:1.5rem 0; }

/* ── Level badge ── */
.lb { display:inline-flex; align-items:center; gap:0.4rem;
    border-radius:100px; padding:0.32rem 0.85rem;
    font-size:0.75rem; font-weight:700; border:1px solid; }
.lb-b { color:#34d399; background:rgba(52,211,153,0.1); border-color:rgba(52,211,153,0.3); }
.lb-i { color:#fbbf24; background:rgba(251,191,36,0.1); border-color:rgba(251,191,36,0.3); }
.lb-e { color:#ef4444; background:rgba(239,68,68,0.1); border-color:rgba(239,68,68,0.3); }

[data-testid="stProgress"] > div > div {
    background:linear-gradient(90deg,var(--blue),var(--violet)) !important;
    border-radius:100px !important;
}
[data-testid="stAlert"] { border-radius:12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ────────────────────────────────────────────────────────────────
LEVELS = [
    (0,   "🌱 Seedling",  "#34d399"),
    (80,  "📚 Scholar",   "#4f8ef7"),
    (200, "🔥 Achiever",  "#f97316"),
    (400, "⚡ Expert",    "#a855f7"),
    (700, "🏆 Master",    "#fbbf24"),
]
ALL_ACH = {
    "first_explain":  {"icon":"🎯","name":"First Steps",    "desc":"Generated first explanation"},
    "first_example":  {"icon":"🌍","name":"World Explorer", "desc":"First real-life example"},
    "quiz_taker":     {"icon":"📝","name":"Quiz Taker",     "desc":"Completed first quiz"},
    "perfect_quiz":   {"icon":"⭐","name":"Perfect Score",  "desc":"Scored 5/5 on quiz"},
    "note_taker":     {"icon":"📒","name":"Note Taker",     "desc":"Saved 3+ notes"},
    "polymath":       {"icon":"🌟","name":"Polymath",       "desc":"Studied 3+ topics"},
    "xp_200":         {"icon":"💎","name":"XP Climber",     "desc":"Earned 200+ XP"},
    "full_session":   {"icon":"🚀","name":"Full Session",   "desc":"Completed full session"},
    "concept_mapper": {"icon":"🗺️","name":"Mapper",        "desc":"Generated concept map"},
    "chatbot_user":   {"icon":"🤖","name":"AI Conversationalist","desc":"Sent 5+ chatbot messages"},
    "industry_pro":   {"icon":"🏭","name":"Industry Pro",  "desc":"Explored real-world apps"},
    "career_ready":   {"icon":"💼","name":"Career Ready",  "desc":"Used Interview Prep"},
    "planner":        {"icon":"📅","name":"Planner",       "desc":"Generated study plan"},
    "flashcard_fan":  {"icon":"🃏","name":"Flashcard Fan", "desc":"Generated flashcards"},
    "coder":          {"icon":"💻","name":"Code Explorer", "desc":"Viewed code example"},
}
DAILY_TIPS = [
    "💡 Binary Search works ONLY on sorted arrays!",
    "💡 O(log n) — doubling data adds just 1 extra step.",
    "💡 Always test edge cases: empty array, single element, duplicates.",
    "💡 The best way to learn: teach it to someone else.",
    "💡 Spaced repetition beats cramming — 1 day, 3 days, 1 week review.",
    "💡 Understanding WHY beats memorising HOW every time.",
    "💡 Code it, break it, fix it — that's how real learning happens.",
]
LEVEL_CTX = {
    "🟢 Beginner":     "Use simple language, no jargon, everyday analogies. Assume zero prior knowledge.",
    "🟡 Intermediate": "Use technical terms (explain them). Include code and complexity notes.",
    "🔴 Expert":       "Be precise and technical. Include complexity analysis, edge cases, advanced nuances.",
}
CHAT_SUGGESTIONS = [
    "💡 Explain it with an analogy",
    "🔍 How does it actually work?",
    "🌍 Give me a real-world example",
    "⏱️ What's the time complexity?",
    "❓ What are common mistakes?",
    "💼 Where is this used in industry?",
    "🧩 How is it different from linear search?",
    "📝 Give me a quick quiz question",
]
INDUSTRY_COLORS = ["#4f8ef7","#34d399","#f97316","#ec4899","#fbbf24","#a855f7"]

# ── Helpers ──────────────────────────────────────────────────────────────────
def get_lv(xp):
    info = LEVELS[0]
    for t,n,c in LEVELS:
        if xp>=t: info=(t,n,c)
    return info

def get_xp_pct(xp):
    ts=[t for t,_,_ in LEVELS]
    for i,t in enumerate(ts):
        if i+1<len(ts) and xp<ts[i+1]:
            return (xp-t)/(ts[i+1]-t)*100, ts[i+1]
    return 100.0, ts[-1]

def add_xp(n,reason=""):
    st.session_state.xp+=n
    st.session_state.xp_log.append(f"+{n} XP — {reason}")
    if st.session_state.xp>=200: award("xp_200")

def award(k):
    if k in ALL_ACH and k not in st.session_state.ach:
        st.session_state.ach.add(k)

# ── Prompt Library ───────────────────────────────────────────────────────────
def p_explain(topic,level):
    ctx=LEVEL_CTX[level]
    return f"""You are BinaryBot, a world-class AI tutor. {ctx}
Explain **{topic}** for a {level.split()[1]} learner. Structure:
1. **What is it?** — One punchy definition sentence.
2. **The Big Idea** — Core concept with a vivid analogy (2-3 sentences).
3. **How it Works** — Numbered step-by-step breakdown.
4. **Key Insight** — The one most important thing (bold it).
5. **Common Mistake** — One mistake beginners often make.
Be engaging and memorable. No dry textbook tone."""

def p_example(topic,level):
    ctx=LEVEL_CTX[level]
    return f"""You are BinaryBot. {ctx}
Give ONE unforgettable real-world example of **{topic}** for a {level.split()[1]} learner.
Format:
🎬 **The Scene:** [1 vivid sentence]
🔍 **How {topic} Applies:** [2-3 clear sentences]
💡 **The Aha Moment:** [One sentence that makes it click]
🔑 **Remember This:** [One-liner takeaway]"""

def p_quiz(topic,level):
    ctx=LEVEL_CTX[level]
    return f"""You are BinaryBot. {ctx}
Create EXACTLY 5 MCQs on **{topic}** for a {level.split()[1]} learner.
Format for EVERY question:
**Q1: [Question]**
A) ...  B) ...  C) ...  D) ...
✅ **Correct:** [Letter] — [1-sentence explanation]
---
(Q2 through Q5 same format)
Cover: definition · mechanism · complexity · use case · edge case."""

def p_grade(topic,quiz_text,answers):
    ab="\n".join([f"Q{i+1}: '{a}'" for i,a in enumerate(answers)])
    return f"""Grade this quiz on {topic}.
Quiz:
{quiz_text}
Student answers:
{ab}
Grade each:
**Q1:** ✅/❌ — [brief reason]
**Q2:** ✅/❌ — ...
**Q3:** ✅/❌ — ...
**Q4:** ✅/❌ — ...
**Q5:** ✅/❌ — ...
---
**🏆 Score: X / 5 (XX%)**
**Grade: [A/B/C/D/F]**
[One warm, specific encouragement line]"""

def p_realworld(topic,level):
    return f"""You are BinaryBot. Provide a detailed real-world applications analysis for **{topic}**.

For EACH of these 5 industries, give a dedicated section:
1. 🖥️ **Tech & Software** (e.g. Google, Microsoft, Meta)
2. 🏥 **Healthcare & Biotech** (e.g. hospitals, genomics)
3. 💰 **Finance & Banking** (e.g. trading, fraud detection)
4. 🛒 **E-commerce & Retail** (e.g. Amazon, Flipkart)
5. 🚗 **Transportation & Logistics** (e.g. Uber, FedEx)

For each industry section use:
**🏢 Companies:** [Specific real company names]
**🔧 How they use {topic}:** [2-3 sentences, very specific]
**💡 Impact:** [Business result or scale]

After all 5, add:
🚀 **Why {topic} is Industry-Critical:** [2-3 sentences]
📊 **Scale of Use:** [Any stats or numbers you know]"""

def p_interview(topic,level):
    ctx=LEVEL_CTX[level]
    return f"""You are BinaryBot, an expert interview coach. {ctx}
Generate 8 interview questions on **{topic}** for a {level.split()[1]} candidate.
For EACH question:
**Q[n]: [Question]** *(Type: Conceptual / Coding / Scenario)*
💬 **Model Answer:** [Clear, complete answer — 3-4 sentences]
⭐ **Pro Tip:** [One tip to stand out]
---
At the end:
🎯 **3 Common Follow-ups:** [bullet points]
📚 **Key Topics to Revise:** [3 topics]
🏢 **Companies that Ask This:** [2-3 real company names]"""

def p_study_plan(topic,level):
    ctx=LEVEL_CTX[level]
    return f"""You are BinaryBot, an expert academic advisor. {ctx}
Create a detailed 4-week study plan to master **{topic}** at {level.split()[1]} level.

📅 **Week 1: Foundation**
- Day 1–2: [Topics + what to read/watch]
- Day 3–4: [Topics + practice]
- Day 5–7: [Mini-project or exercises]
✅ **Milestone:** [What you can do after week 1]

📅 **Week 2: Core Concepts**
(same format)

📅 **Week 3: Advanced Topics**
(same format)

📅 **Week 4: Mastery & Application**
(same format)

After the weeks:
📚 **Resources:** [3-5 specific books, courses, or websites]
🎯 **Capstone Project:** [One project idea to demonstrate mastery]
⏱️ **Daily Commitment:** [Recommended hours/day]"""

def p_flashcards(topic,level):
    ctx=LEVEL_CTX[level]
    return f"""You are BinaryBot. {ctx}
Create 8 flashcards for **{topic}** at {level.split()[1]} level.

For EACH card:
🃏 **Card [n]:**
**Q:** [Clear, specific question]
**A:** [Concise answer — 1-2 sentences max]
💡 **Memory Tip:** [Mnemonic or vivid trick to remember]
---
(All 8 cards, same format)
After all cards:
🎯 **Recommended Review Order:** [Order to study for best retention]"""

def p_code(topic,level):
    ctx=LEVEL_CTX[level]
    return f"""You are BinaryBot. {ctx}
Provide a clean, working code example for **{topic}** in Python.

📝 **Python Implementation:**
```python
# Well-commented, production-quality code
```

🔍 **Line-by-Line Explanation:**
[Key lines explained simply]

⚡ **Time Complexity:** O(?) — [Why]
💾 **Space Complexity:** O(?) — [Why]

🔧 **Real Production Use:**
[How this exact code pattern appears in real software — 2-3 sentences]

🏢 **Used By:** [2-3 real companies/systems that use this]

🚀 **Challenge:** [One modification task for the student]"""

def p_concept_map(topic):
    return f"""Create a detailed concept map for **{topic}** using ASCII art tree structure.

🎯 {topic.upper()}
├── 📌 [Main Branch 1: Definition & Core]
│   ├── [Sub-concept 1a]
│   ├── [Sub-concept 1b]
│   └── [Sub-concept 1c]
├── 📌 [Main Branch 2: How It Works]
│   ├── ...
│   └── ...
├── 📌 [Main Branch 3: Variants/Types]
│   └── ...
├── 📌 [Main Branch 4: Applications]
│   └── ...
└── 📌 [Main Branch 5: Complexity & Trade-offs]
    └── ...

🔗 **Key Connections:** [How branches relate]
💡 **Learning Path:** [Suggested study order]
🎯 **Core Principle:** [One sentence that ties it all together]"""

def p_full_session(topic,level):
    ctx=LEVEL_CTX[level]
    return f"""You are BinaryBot, the world's most engaging AI tutor. {ctx}
Run a COMPLETE, EXCITING learning session on **{topic}** (Level: {level.split()[1]}).

👋 **Welcome** — Enthusiastic, personalised greeting
📖 **Core Concept** — Crystal-clear explanation with analogy
🌍 **Real-World Example** — One vivid, memorable example
🏭 **Industry Spotlight** — One industry that heavily uses this
🤔 **Think About It** — One challenging discussion question
📝 **Mini-Quiz** — 3 quick questions with answers
🎯 **Key Takeaways** — 3 bullet points to remember forever
🚀 **What's Next?** — 2-3 related topics to explore
💪 **Closing** — Warm, motivating farewell

Make it feel like an exciting live masterclass. Use emojis, be dynamic!"""

def p_chatbot(topic, level, history_text, user_msg):
    return f"""You are BinaryBot, a brilliant and conversational AI tutor specializing in {topic}.

Context: You are having a friendly, engaging chat with a student learning {topic} at {level.split()[1]} level.

Your personality in this chat:
- Warm, encouraging mentor (not a lecturer)
- Use emojis naturally (1-2 per message max)
- Keep responses concise (3-5 sentences) — expand only if asked
- Always connect to real-world applications
- Ask one follow-up question to keep the conversation going
- Celebrate correct understanding enthusiastically

Recent conversation:
{history_text}

Student says: {user_msg}

Respond as BinaryBot:"""

# ── Session State ────────────────────────────────────────────────────────────
_def = {
    "xp":0, "xp_log":[], "ach":set(), "topics":set(),
    "notes":[], "chat_msgs":[], "quiz_text":"", "quiz_answers":["","","","",""],
    "quiz_graded":"", "quiz_score":-1, "interactions":0, "q_count":0,
    "session_start":datetime.now(), "level":"🟢 Beginner",
    "last_explain":"", "last_explain_topic":"",
    "last_example":"", "concept_map_text":"",
    "realworld_text":"", "interview_text":"",
    "study_plan_text":"", "flashcards_text":"",
    "code_text":"", "full_session_text":"",
    "chat_input_val":"",
}
for k,v in _def.items():
    if k not in st.session_state:
        st.session_state[k] = v if not isinstance(v,set) else set()

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.3rem 0 0.8rem;'>
        <div style='font-size:3.2rem;line-height:1;margin-bottom:0.5rem;'>🎓</div>
        <div style='font-family:"Space Grotesk",sans-serif;font-size:1.28rem;font-weight:800;
            background:linear-gradient(135deg,#4f8ef7,#7c5cfc,#22d3ee);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>
            AI Learning Buddy
        </div>
        <div style='font-size:0.68rem;color:#64748b;margin-top:0.25rem;
            letter-spacing:0.1em;text-transform:uppercase;font-weight:600;'>
            Real-World EdTech Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(100,120,255,0.14);margin:0.5rem 0 1rem;'>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.78rem;font-weight:700;color:#64748b;letter-spacing:0.07em;text-transform:uppercase;margin-bottom:0.4rem;'>🎯 Topic</div>", unsafe_allow_html=True)
    topic = st.text_input("t", value="Binary Search", placeholder="Any topic…", key="topic_in", label_visibility="collapsed")

    st.markdown("<div style='font-size:0.78rem;font-weight:700;color:#64748b;letter-spacing:0.07em;text-transform:uppercase;margin-bottom:0.4rem;margin-top:0.85rem;'>📊 Level</div>", unsafe_allow_html=True)
    level = st.radio("l", ["🟢 Beginner","🟡 Intermediate","🔴 Expert"], key="level_r", label_visibility="collapsed")
    st.session_state.level = level

    st.markdown("<hr style='border:none;border-top:1px solid rgba(100,120,255,0.14);margin:0.85rem 0;'>", unsafe_allow_html=True)

    xp = st.session_state.xp
    _,lv_n,lv_c = get_lv(xp)
    xp_p,nxt = get_xp_pct(xp)
    st.markdown(f"""
    <div class="xp-wrap">
        <div style='display:flex;justify-content:space-between;align-items:center;'>
            <div style='font-size:0.9rem;font-weight:700;color:#e2e8f0;font-family:"Space Grotesk",sans-serif;'>{lv_n}</div>
            <div style='font-size:0.9rem;font-weight:800;color:{lv_c};font-family:"Space Grotesk",sans-serif;'>{xp} XP</div>
        </div>
        <div class="xp-track">
            <div class="xp-fill" style='width:{min(xp_p,100):.1f}%;background:linear-gradient(90deg,{lv_c},{lv_c}88);'></div>
        </div>
        <div style='font-size:0.68rem;color:#64748b;text-align:right;'>Next: {nxt} XP</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.ach:
        st.markdown("<div style='font-size:0.78rem;font-weight:700;color:#64748b;letter-spacing:0.07em;text-transform:uppercase;margin-bottom:0.5rem;'>🏅 Badges</div>", unsafe_allow_html=True)
        bh='<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">'
        for k in st.session_state.ach:
            if k in ALL_ACH:
                a=ALL_ACH[k]
                aname=a["name"]; adesc=a["desc"]; aicon=a["icon"]
                bh+=f'<div class="badge badge-on" title="{aname}: {adesc}">{aicon} {aname}</div>'
        bh+='</div>'
        st.markdown(bh, unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:0.78rem;color:#64748b;font-style:italic;'>Complete actions to earn badges! 🏅</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(100,120,255,0.14);margin:0.85rem 0;'>", unsafe_allow_html=True)

    session_mins = max(1, int((datetime.now()-st.session_state.session_start).total_seconds()/60))
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.02);border-radius:11px;padding:0.75rem;font-size:0.78rem;color:#64748b;'>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:0.45rem;'>
            <div>⏱️ <b style='color:#e2e8f0'>{session_mins}m</b></div>
            <div>⚡ <b style='color:#e2e8f0'>{st.session_state.interactions}</b> actions</div>
            <div>📚 <b style='color:#e2e8f0'>{len(st.session_state.topics)}</b> topics</div>
            <div>💬 <b style='color:#e2e8f0'>{st.session_state.q_count}</b> chats</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.topics:
        tags="".join([f'<span class="ttag">{t}</span>' for t in st.session_state.topics])
        st.markdown(f"<div style='margin-top:0.6rem;'>{tags}</div>", unsafe_allow_html=True)

    tip=random.choice(DAILY_TIPS)
    st.markdown(f"""
    <div style='background:rgba(79,142,247,0.06);border-left:3px solid #4f8ef7;border-radius:0 10px 10px 0;
        padding:0.85rem;margin-top:0.9rem;font-size:0.78rem;color:#94a3b8;line-height:1.6;'>{tip}</div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(100,120,255,0.14);margin:0.85rem 0;'>", unsafe_allow_html=True)
    if st.button("🔄 Reset Session", key="reset_btn"):
        for k,v in _def.items():
            st.session_state[k]=v if not isinstance(v,set) else set()
        st.rerun()

# ── HERO ─────────────────────────────────────────────────────────────────────
ld=level.split()[1] if level else "Beginner"
lbc={"Beginner":"lb-b","Intermediate":"lb-i","Expert":"lb-e"}.get(ld,"lb-b")

st.markdown(f"""
<div class="hero">
    <div style='display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:1rem;'>
        <div>
            <h1 class="hero-title">AI Learning Buddy</h1>
            <p class="hero-sub">A real-world adaptive EdTech platform — powered by Google Gemini AI. Learn any topic through intelligent tutoring, industry insights, interview prep, and conversational AI.</p>
            <div class="hero-tags">
                <div class="hero-tag">🤖 Multi-turn AI Chatbot</div>
                <div class="hero-tag">🏭 Industry Applications</div>
                <div class="hero-tag">💼 Interview Prep</div>
                <div class="hero-tag">📅 Study Plan</div>
                <div class="hero-tag">🃏 Flashcards</div>
                <div class="hero-tag">💻 Code Examples</div>
                <div class="hero-tag">🎮 XP Gamification</div>
                <div class="hero-tag">🏅 Achievements</div>
            </div>
        </div>
        <div style='text-align:right;flex-shrink:0;'>
            <div style='font-size:4.2rem;line-height:1;'>🎓</div>
            <div class="lb {lbc}" style='margin-top:0.6rem;'>{level}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── STATS ────────────────────────────────────────────────────────────────────
xp=st.session_state.xp
_,lv_n,lv_c=get_lv(xp)
st.markdown(f"""
<div class="stats-grid">
    <div class="stat-card"><div class="stat-num" style="color:{lv_c};">{xp}</div><div class="stat-lbl">XP Earned</div></div>
    <div class="stat-card"><div class="stat-num" style="color:#22d3ee;">{len(st.session_state.topics)}</div><div class="stat-lbl">Topics</div></div>
    <div class="stat-card"><div class="stat-num" style="color:#34d399;">{st.session_state.interactions}</div><div class="stat-lbl">Actions</div></div>
    <div class="stat-card"><div class="stat-num" style="color:#f97316;">{len(st.session_state.notes)}</div><div class="stat-lbl">Notes</div></div>
    <div class="stat-card"><div class="stat-num" style="color:#fbbf24;">{len(st.session_state.ach)}</div><div class="stat-lbl">Badges</div></div>
</div>
""", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9 = st.tabs([
    "📖 Learn","🃏 Flashcards","💻 Code","🌍 Real-World Apps",
    "🧠 Smart Quiz","💼 Interview & Plan","🗺️ Concept Map",
    "🤖 AI Chatbot","📝 Notes & Progress"
])

# ─────────── TAB 1: LEARN ───────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="s-head">📖 Explain a Concept</div>', unsafe_allow_html=True)
    st.markdown('<div class="s-sub">BinaryBot explains with analogies, step-by-step breakdown, and key insights — tailored to your level.</div>', unsafe_allow_html=True)

    c1,c2=st.columns([4,1])
    with c1: do_explain = st.button("✨ Explain Now  (+10 XP)", key="b_explain")
    with c2: do_save_e  = st.button("💾 Save", key="b_save_e")

    if do_explain:
        if not topic.strip(): st.warning("Enter a topic.")
        else:
            with st.spinner("BinaryBot is crafting your explanation…"):
                try:
                    r=model.generate_content(p_explain(topic.strip(),level)).text
                    st.session_state.last_explain=r
                    st.session_state.last_explain_topic=topic.strip()
                    st.session_state.topics.add(topic.strip())
                    st.session_state.interactions+=1
                    add_xp(10,f"Explained '{topic}'")
                    award("first_explain")
                    if len(st.session_state.topics)>=3: award("polymath")
                except Exception as e: st.error(f"Error: {e}")

    if do_save_e and st.session_state.last_explain:
        st.session_state.notes.append({"topic":st.session_state.last_explain_topic,"type":"Explanation","content":st.session_state.last_explain,"time":datetime.now().strftime("%H:%M")})
        add_xp(5,"Saved note")
        if len(st.session_state.notes)>=3: award("note_taker")
        st.success("✅ Saved to notes!")

    if st.session_state.last_explain:
        st.markdown(f'<div class="rbox">{st.session_state.last_explain}</div>',unsafe_allow_html=True)
        st.markdown('<div class="xp-toast">⚡ +10 XP earned!</div>',unsafe_allow_html=True)

    if do_save_e and not st.session_state.last_explain:
        st.info("Generate an explanation first.")

    # Full Session shortcut
    st.markdown('<div class="fhr"></div>', unsafe_allow_html=True)
    st.markdown('<div class="s-head">🚀 Full Learning Session</div>', unsafe_allow_html=True)
    st.markdown('<div class="s-sub">One click → complete masterclass: concept · example · industry · quiz · takeaways · next steps.</div>', unsafe_allow_html=True)

    c3,c4=st.columns([4,1])
    with c3: do_full=st.button("▶️ Start Full Session  (+30 XP)",key="b_full")
    with c4: do_save_f=st.button("💾 Save",key="b_save_f")

    if do_full:
        if not topic.strip(): st.warning("Enter a topic.")
        else:
            with st.spinner("BinaryBot is preparing your masterclass…"):
                try:
                    r=model.generate_content(p_full_session(topic.strip(),level)).text
                    st.session_state.full_session_text=r
                    st.session_state.topics.add(topic.strip())
                    st.session_state.interactions+=1
                    add_xp(30,"Full Session")
                    award("full_session")
                    if len(st.session_state.topics)>=3: award("polymath")
                except Exception as e: st.error(f"Error: {e}")

    if do_save_f and st.session_state.full_session_text:
        st.session_state.notes.append({"topic":topic.strip(),"type":"Full Session","content":st.session_state.full_session_text,"time":datetime.now().strftime("%H:%M")})
        if len(st.session_state.notes)>=3: award("note_taker")
        st.success("✅ Session saved!")

    if st.session_state.full_session_text:
        st.markdown(f'<div class="rbox">{st.session_state.full_session_text}</div>',unsafe_allow_html=True)
        st.markdown('<div class="xp-toast">🚀 +30 XP earned!</div>',unsafe_allow_html=True)

# ─────────── TAB 2: FLASHCARDS ──────────────────────────────────────────────
with tab2:
    st.markdown('<div class="s-head">🃏 AI Flashcard Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="s-sub">8 AI-generated Q&A flashcards with memory tricks — perfect for spaced repetition review.</div>', unsafe_allow_html=True)

    c5,c6=st.columns([4,1])
    with c5: do_fc=st.button("🃏 Generate Flashcards  (+15 XP)",key="b_fc")
    with c6: do_fc_save=st.button("💾 Save",key="b_fc_save")

    if do_fc:
        if not topic.strip(): st.warning("Enter a topic.")
        else:
            with st.spinner("Creating your flashcard deck…"):
                try:
                    r=model.generate_content(p_flashcards(topic.strip(),level)).text
                    st.session_state.flashcards_text=r
                    st.session_state.topics.add(topic.strip())
                    st.session_state.interactions+=1
                    add_xp(15,"Generated flashcards")
                    award("flashcard_fan")
                except Exception as e: st.error(f"Error: {e}")

    if do_fc_save and st.session_state.flashcards_text:
        st.session_state.notes.append({"topic":topic.strip(),"type":"Flashcards","content":st.session_state.flashcards_text,"time":datetime.now().strftime("%H:%M")})
        if len(st.session_state.notes)>=3: award("note_taker")
        st.success("✅ Flashcards saved!")

    if st.session_state.flashcards_text:
        st.markdown(f'<div class="rbox">{st.session_state.flashcards_text}</div>',unsafe_allow_html=True)
        st.markdown('<div class="xp-toast">🃏 +15 XP earned!</div>',unsafe_allow_html=True)

# ─────────── TAB 3: CODE ────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="s-head">💻 Code Example Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="s-sub">Working Python implementation with line-by-line explanation, complexity analysis, and real production context.</div>', unsafe_allow_html=True)

    c7,c8=st.columns([4,1])
    with c7: do_code=st.button("💻 Generate Code Example  (+15 XP)",key="b_code")
    with c8: do_code_save=st.button("💾 Save",key="b_code_save")

    if do_code:
        if not topic.strip(): st.warning("Enter a topic.")
        else:
            with st.spinner("BinaryBot is writing clean code…"):
                try:
                    r=model.generate_content(p_code(topic.strip(),level)).text
                    st.session_state.code_text=r
                    st.session_state.topics.add(topic.strip())
                    st.session_state.interactions+=1
                    add_xp(15,"Generated code example")
                    award("coder")
                except Exception as e: st.error(f"Error: {e}")

    if do_code_save and st.session_state.code_text:
        st.session_state.notes.append({"topic":topic.strip(),"type":"Code Example","content":st.session_state.code_text,"time":datetime.now().strftime("%H:%M")})
        if len(st.session_state.notes)>=3: award("note_taker")
        st.success("✅ Code saved!")

    if st.session_state.code_text:
        st.markdown(f'<div class="rbox">{st.session_state.code_text}</div>',unsafe_allow_html=True)
        st.markdown('<div class="xp-toast">💻 +15 XP earned!</div>',unsafe_allow_html=True)

    # Real-Life Example (moved here as secondary)
    st.markdown('<div class="fhr"></div>', unsafe_allow_html=True)
    st.markdown('<div class="s-head">🌍 Real-Life Example</div>', unsafe_allow_html=True)
    st.markdown('<div class="s-sub">One unforgettable real-world scenario that makes the concept click instantly.</div>', unsafe_allow_html=True)
    if st.button("🌍 Get Example  (+10 XP)",key="b_ex"):
        if not topic.strip(): st.warning("Enter a topic.")
        else:
            with st.spinner("Finding the perfect example…"):
                try:
                    r=model.generate_content(p_example(topic.strip(),level)).text
                    st.session_state.last_example=r
                    st.session_state.topics.add(topic.strip())
                    st.session_state.interactions+=1
                    add_xp(10,f"Example for '{topic}'")
                    award("first_example")
                except Exception as e: st.error(f"Error: {e}")
    if st.session_state.last_example:
        st.markdown(f'<div class="rbox">{st.session_state.last_example}</div>',unsafe_allow_html=True)
        st.markdown('<div class="xp-toast">🌍 +10 XP earned!</div>',unsafe_allow_html=True)

# ─────────── TAB 4: REAL-WORLD APPS ─────────────────────────────────────────
with tab4:
    st.markdown('<div class="s-head">🌍 Real-World Industry Applications</div>', unsafe_allow_html=True)
    st.markdown('<div class="s-sub">See exactly how real companies — Google, Amazon, Netflix, Uber — use this topic in production systems.</div>', unsafe_allow_html=True)

    c9,c10=st.columns([4,1])
    with c9: do_rw=st.button("🏭 Explore Industry Applications  (+20 XP)",key="b_rw")
    with c10: do_rw_save=st.button("💾 Save",key="b_rw_save")

    if do_rw:
        if not topic.strip(): st.warning("Enter a topic.")
        else:
            with st.spinner("Researching industry applications…"):
                try:
                    r=model.generate_content(p_realworld(topic.strip(),level)).text
                    st.session_state.realworld_text=r
                    st.session_state.topics.add(topic.strip())
                    st.session_state.interactions+=1
                    add_xp(20,"Real-world apps explored")
                    award("industry_pro")
                except Exception as e: st.error(f"Error: {e}")

    if do_rw_save and st.session_state.realworld_text:
        st.session_state.notes.append({"topic":topic.strip(),"type":"Industry Apps","content":st.session_state.realworld_text,"time":datetime.now().strftime("%H:%M")})
        if len(st.session_state.notes)>=3: award("note_taker")
        st.success("✅ Saved!")

    if st.session_state.realworld_text:
        st.markdown(f'<div class="rbox">{st.session_state.realworld_text}</div>',unsafe_allow_html=True)
        st.markdown('<div class="xp-toast">🏭 +20 XP earned!</div>',unsafe_allow_html=True)

# ─────────── TAB 5: SMART QUIZ ──────────────────────────────────────────────
with tab5:
    st.markdown('<div class="s-head">🧠 Smart Graded Quiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="s-sub">Generate a 5-question quiz → type all answers → AI grades every answer and gives a full score card.</div>', unsafe_allow_html=True)

    cq1,cq2=st.columns([3,1])
    with cq1: do_gen_quiz=st.button("🎲 Generate Quiz  (+5 XP)",key="b_gq")
    with cq2:
        if st.button("🔄 Reset",key="b_rq"):
            st.session_state.quiz_text=""
            st.session_state.quiz_answers=["","","","",""]
            st.session_state.quiz_graded=""
            st.rerun()

    if do_gen_quiz:
        if not topic.strip(): st.warning("Enter a topic.")
        else:
            with st.spinner("Generating your quiz…"):
                try:
                    r=model.generate_content(p_quiz(topic.strip(),level)).text
                    st.session_state.quiz_text=r
                    st.session_state.quiz_answers=["","","","",""]
                    st.session_state.quiz_graded=""
                    st.session_state.topics.add(topic.strip())
                    st.session_state.interactions+=1
                    add_xp(5,"Generated quiz")
                    award("quiz_taker")
                except Exception as e: st.error(f"Error: {e}")

    if st.session_state.quiz_text:
        st.markdown(f'<div class="rbox">{st.session_state.quiz_text}</div>',unsafe_allow_html=True)
        st.markdown('<div class="fhr"></div>',unsafe_allow_html=True)
        st.markdown("**✍️ Your Answers** *(type A, B, C, or D for each)*")
        cols=st.columns(5)
        for i,col in enumerate(cols):
            with col:
                st.session_state.quiz_answers[i]=st.text_input(
                    f"Q{i+1}",value=st.session_state.quiz_answers[i],
                    placeholder="A-D",key=f"qa_{i}",max_chars=50)

        if st.button("🎯 Submit & Grade All  (+20 XP)",key="b_grade"):
            filled=[a.strip() for a in st.session_state.quiz_answers if a.strip()]
            if len(filled)<3: st.warning("Answer at least 3 questions.")
            else:
                with st.spinner("BinaryBot is grading…"):
                    try:
                        fb=model.generate_content(p_grade(topic.strip(),st.session_state.quiz_text,st.session_state.quiz_answers)).text
                        st.session_state.quiz_graded=fb
                        st.session_state.interactions+=1
                        add_xp(20,"Completed graded quiz")
                        if "5 / 5" in fb or "5/5" in fb:
                            add_xp(10,"Perfect score bonus!")
                            award("perfect_quiz")
                    except Exception as e: st.error(f"Error: {e}")

    if st.session_state.quiz_graded:
        fb=st.session_state.quiz_graded
        if "5/5" in fb or "5 / 5" in fb:   sc,sc_c="5/5","#34d399"
        elif "4/5" in fb or "4 / 5" in fb: sc,sc_c="4/5","#4f8ef7"
        elif "3/5" in fb or "3 / 5" in fb: sc,sc_c="3/5","#fbbf24"
        else:                               sc,sc_c="?/5","#f97316"
        st.markdown(f"""
        <div class="score-card" style="border-color:{sc_c}44;">
            <div class="score-big" style="color:{sc_c};">{sc}</div>
            <div style='font-size:1.1rem;font-weight:600;color:{sc_c};margin-top:0.4rem;'>Quiz Score</div>
        </div>""",unsafe_allow_html=True)
        st.markdown(f'<div class="rbox">{fb}</div>',unsafe_allow_html=True)
        st.markdown('<div class="xp-toast">🎯 +20 XP for completing the quiz!</div>',unsafe_allow_html=True)

# ─────────── TAB 6: INTERVIEW & PLAN ────────────────────────────────────────
with tab6:
    ci1,ci2=st.columns(2)

    with ci1:
        st.markdown('<div class="s-head">💼 Interview Prep</div>', unsafe_allow_html=True)
        st.markdown('<div class="s-sub">8 real interview questions with model answers, pro tips, and company insights.</div>', unsafe_allow_html=True)

        cib1,cib2=st.columns([3,1])
        with cib1: do_iv=st.button("💼 Generate Interview Q&A  (+20 XP)",key="b_iv")
        with cib2: do_iv_save=st.button("💾",key="b_iv_s")

        if do_iv:
            if not topic.strip(): st.warning("Enter a topic.")
            else:
                with st.spinner("Preparing your interview pack…"):
                    try:
                        r=model.generate_content(p_interview(topic.strip(),level)).text
                        st.session_state.interview_text=r
                        st.session_state.topics.add(topic.strip())
                        st.session_state.interactions+=1
                        add_xp(20,"Interview prep")
                        award("career_ready")
                    except Exception as e: st.error(f"Error: {e}")

        if do_iv_save and st.session_state.interview_text:
            st.session_state.notes.append({"topic":topic.strip(),"type":"Interview Prep","content":st.session_state.interview_text,"time":datetime.now().strftime("%H:%M")})
            if len(st.session_state.notes)>=3: award("note_taker")
            st.success("✅ Saved!")

        if st.session_state.interview_text:
            st.markdown(f'<div class="rbox" style="max-height:520px;overflow-y:auto;">{st.session_state.interview_text}</div>',unsafe_allow_html=True)
            st.markdown('<div class="xp-toast">💼 +20 XP earned!</div>',unsafe_allow_html=True)

    with ci2:
        st.markdown('<div class="s-head">📅 Personalized Study Plan</div>', unsafe_allow_html=True)
        st.markdown('<div class="s-sub">AI-generated 4-week learning roadmap with daily tasks, milestones, and resources.</div>', unsafe_allow_html=True)

        csb1,csb2=st.columns([3,1])
        with csb1: do_sp=st.button("📅 Generate Study Plan  (+20 XP)",key="b_sp")
        with csb2: do_sp_save=st.button("💾",key="b_sp_s")

        if do_sp:
            if not topic.strip(): st.warning("Enter a topic.")
            else:
                with st.spinner("Building your personalized roadmap…"):
                    try:
                        r=model.generate_content(p_study_plan(topic.strip(),level)).text
                        st.session_state.study_plan_text=r
                        st.session_state.topics.add(topic.strip())
                        st.session_state.interactions+=1
                        add_xp(20,"Generated study plan")
                        award("planner")
                    except Exception as e: st.error(f"Error: {e}")

        if do_sp_save and st.session_state.study_plan_text:
            st.session_state.notes.append({"topic":topic.strip(),"type":"Study Plan","content":st.session_state.study_plan_text,"time":datetime.now().strftime("%H:%M")})
            if len(st.session_state.notes)>=3: award("note_taker")
            st.success("✅ Saved!")

        if st.session_state.study_plan_text:
            st.markdown(f'<div class="rbox" style="max-height:520px;overflow-y:auto;">{st.session_state.study_plan_text}</div>',unsafe_allow_html=True)
            st.markdown('<div class="xp-toast">📅 +20 XP earned!</div>',unsafe_allow_html=True)

# ─────────── TAB 7: CONCEPT MAP ─────────────────────────────────────────────
with tab7:
    st.markdown('<div class="s-head">🗺️ Concept Map Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="s-sub">Visual ASCII concept map showing all sub-topics, relationships, learning path, and core principle.</div>', unsafe_allow_html=True)

    cm1,cm2=st.columns([4,1])
    with cm1: do_cm=st.button("🗺️ Generate Concept Map  (+15 XP)",key="b_cm")
    with cm2: do_cm_save=st.button("💾 Save",key="b_cm_s")

    if do_cm:
        if not topic.strip(): st.warning("Enter a topic.")
        else:
            with st.spinner("Mapping your concept…"):
                try:
                    r=model.generate_content(p_concept_map(topic.strip())).text
                    st.session_state.concept_map_text=r
                    st.session_state.topics.add(topic.strip())
                    st.session_state.interactions+=1
                    add_xp(15,"Concept map generated")
                    award("concept_mapper")
                except Exception as e: st.error(f"Error: {e}")

    if do_cm_save and st.session_state.concept_map_text:
        st.session_state.notes.append({"topic":topic.strip(),"type":"Concept Map","content":st.session_state.concept_map_text,"time":datetime.now().strftime("%H:%M")})
        if len(st.session_state.notes)>=3: award("note_taker")
        st.success("✅ Saved!")

    if st.session_state.concept_map_text:
        st.markdown(f'<div class="cmap">{st.session_state.concept_map_text}</div>',unsafe_allow_html=True)
        st.markdown('<div class="xp-toast">🗺️ +15 XP earned!</div>',unsafe_allow_html=True)

# ─────────── TAB 8: AI CHATBOT ───────────────────────────────────────────────
with tab8:
    st.markdown("""
    <div style='display:flex;align-items:center;gap:1rem;margin-bottom:0.4rem;'>
        <div style='background:linear-gradient(135deg,#4f8ef7,#7c5cfc);width:48px;height:48px;border-radius:50%;
            display:flex;align-items:center;justify-content:center;font-size:1.5rem;
            box-shadow:0 4px 20px rgba(79,142,247,0.4);flex-shrink:0;'>🤖</div>
        <div>
            <div class="s-head" style="margin-bottom:0;">BinaryBot — AI Chatbot</div>
            <div class="s-sub" style="margin-bottom:0;">Multi-turn conversational AI. Ask anything about the topic — BinaryBot remembers your conversation.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Welcome if fresh
    if not st.session_state.chat_msgs:
        st.markdown(f"""
        <div class="msg-ai">
            <div class="ai-avatar">🤖</div>
            <div class="bubble-ai">
                👋 Hey there! I'm <b>BinaryBot</b>, your personal AI tutor on <b>{topic}</b>.<br><br>
                I'm here to chat, explain, answer your questions, and help you truly understand the concept — not just memorise it. What would you like to explore? 🚀
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Suggestion chips
    st.markdown('<div class="chip-row">', unsafe_allow_html=True)
    chip_cols = st.columns(4)
    selected_chip = ""
    for i, (col, chip) in enumerate(zip(chip_cols, CHAT_SUGGESTIONS[:4])):
        with col:
            if st.button(chip, key=f"chip_{i}"):
                selected_chip = chip.split(" ",1)[1] if " " in chip else chip

    chip_cols2 = st.columns(4)
    for i, (col, chip) in enumerate(zip(chip_cols2, CHAT_SUGGESTIONS[4:])):
        with col:
            if st.button(chip, key=f"chip2_{i}"):
                selected_chip = chip.split(" ",1)[1] if " " in chip else chip
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat history display
    if st.session_state.chat_msgs:
        chat_html = ""
        for msg in st.session_state.chat_msgs[-20:]:
            if msg["role"]=="user":
                chat_html += f'<div class="msg-user"><div class="bubble-user">{msg["content"]}</div></div>'
            else:
                chat_html += f'<div class="msg-ai"><div class="ai-avatar">🤖</div><div class="bubble-ai">{msg["content"]}</div></div>'
        st.markdown(f'<div class="chat-wrap">{chat_html}</div>', unsafe_allow_html=True)

    # Input area
    st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
    user_input_val = selected_chip if selected_chip else ""

    user_msg = st.text_area(
        "Message BinaryBot",
        value=user_input_val,
        placeholder=f"Ask BinaryBot anything about {topic}…",
        height=80, key="chat_inp", label_visibility="collapsed"
    )

    cb1,cb2,cb3=st.columns([3,1,1])
    with cb1:
        do_send=st.button("🚀 Send Message  (+5 XP)",key="b_send_chat")
    with cb2:
        do_clear_chat=st.button("🗑️ Clear Chat",key="b_clear_chat")
    with cb3:
        do_save_chat=st.button("💾 Save Chat",key="b_save_chat")

    if do_clear_chat:
        st.session_state.chat_msgs=[]
        st.rerun()

    if do_save_chat and st.session_state.chat_msgs:
        chat_export="\n\n".join([f"{'You' if m['role']=='user' else 'BinaryBot'}: {m['content']}" for m in st.session_state.chat_msgs])
        st.session_state.notes.append({"topic":topic.strip(),"type":"Chatbot Conversation","content":chat_export,"time":datetime.now().strftime("%H:%M")})
        if len(st.session_state.notes)>=3: award("note_taker")
        st.success("✅ Chat saved to notes!")

    if do_send and (user_msg.strip() or selected_chip):
        msg_to_send = user_msg.strip() or selected_chip
        if not msg_to_send: st.warning("Type a message.")
        elif not topic.strip(): st.warning("Enter a topic in the sidebar.")
        else:
            # Build history context (last 8 messages)
            hist=""
            for m in st.session_state.chat_msgs[-8:]:
                role="Student" if m["role"]=="user" else "BinaryBot"
                hist+=f"{role}: {m['content']}\n\n"

            with st.spinner("BinaryBot is typing…"):
                try:
                    reply=model.generate_content(p_chatbot(topic.strip(),level,hist,msg_to_send)).text
                    st.session_state.chat_msgs.append({"role":"user","content":msg_to_send})
                    st.session_state.chat_msgs.append({"role":"ai","content":reply})
                    st.session_state.interactions+=1
                    st.session_state.q_count+=1
                    add_xp(5,"Chatbot message")
                    if st.session_state.q_count>=5: award("chatbot_user")
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

# ─────────── TAB 9: NOTES & PROGRESS ────────────────────────────────────────
with tab9:
    cn1,cn2=st.columns([3,2])

    with cn1:
        st.markdown('<div class="s-head">📝 Study Notes Library</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="s-sub">{len(st.session_state.notes)} notes saved this session.</div>', unsafe_allow_html=True)

        if not st.session_state.notes:
            st.markdown("""
            <div style='background:rgba(255,255,255,0.02);border:1px dashed rgba(100,120,255,0.2);
                border-radius:16px;padding:2.5rem;text-align:center;color:#64748b;'>
                <div style='font-size:2.5rem;margin-bottom:0.6rem;'>📭</div>
                <div>No notes yet. Use 💾 buttons on other tabs to save content here.</div>
            </div>""", unsafe_allow_html=True)
        else:
            TC={"Explanation":"#4f8ef7","Concept Map":"#22d3ee","Full Session":"#7c5cfc",
                "Industry Apps":"#34d399","Interview Prep":"#f97316","Study Plan":"#fbbf24",
                "Flashcards":"#ec4899","Code Example":"#a855f7","Chatbot Conversation":"#64748b"}
            for note in reversed(st.session_state.notes):
                tc=TC.get(note["type"],"#4f8ef7")
                preview=note["content"][:320]+"…" if len(note["content"])>320 else note["content"]
                st.markdown(f"""
                <div class="note-card" style="border-left-color:{tc};">
                    <div style='font-size:0.7rem;font-weight:700;color:{tc};text-transform:uppercase;
                        letter-spacing:0.08em;margin-bottom:0.4rem;'>
                        📌 {note["topic"]} — {note["type"]}
                    </div>
                    <div style='font-size:0.87rem;color:#94a3b8;line-height:1.65;'>{preview}</div>
                    <div style='font-size:0.69rem;color:#64748b;margin-top:0.5rem;'>⏱️ {note["time"]}</div>
                </div>""", unsafe_allow_html=True)
            if st.button("🗑️ Clear All Notes",key="b_cn"):
                st.session_state.notes=[]
                st.rerun()

    with cn2:
        st.markdown('<div class="s-head">📈 Progress & Achievements</div>', unsafe_allow_html=True)

        xp=st.session_state.xp
        _,lv_n,lv_c=get_lv(xp)
        xp_p,nxt=get_xp_pct(xp)

        st.markdown(f"""
        <div style='background:var(--card);border:1px solid var(--border2);border-radius:18px;padding:1.6rem;margin-bottom:1rem;'>
            <div style='font-family:"Space Grotesk",sans-serif;font-size:1.1rem;font-weight:700;color:#e2e8f0;margin-bottom:0.3rem;'>{lv_n}</div>
            <div style='font-size:3rem;font-weight:900;color:{lv_c};font-family:"Space Grotesk",sans-serif;line-height:1;margin-bottom:0.8rem;'>
                {xp} <span style='font-size:1rem;font-weight:600;color:#64748b;'>XP</span>
            </div>
            <div style='background:rgba(255,255,255,0.07);border-radius:100px;height:12px;overflow:hidden;'>
                <div style='width:{min(xp_p,100):.1f}%;height:100%;background:linear-gradient(90deg,{lv_c},{lv_c}88);border-radius:100px;'></div>
            </div>
            <div style='font-size:0.7rem;color:#64748b;margin-top:0.4rem;text-align:right;'>{nxt-xp} XP to next level</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**🏅 All Achievements**")
        for k,a in ALL_ACH.items():
            un=k in st.session_state.ach
            bg="rgba(251,191,36,0.08)" if un else "rgba(255,255,255,0.02)"
            bd="rgba(251,191,36,0.3)" if un else "rgba(100,120,255,0.1)"
            nc="#fbbf24" if un else "#64748b"
            op="1" if un else "0.4"
            st.markdown(f"""
            <div style='background:{bg};border:1px solid {bd};border-radius:11px;padding:0.6rem 0.85rem;
                margin-bottom:0.4rem;display:flex;align-items:center;gap:0.6rem;opacity:{op};'>
                <span style='font-size:1.15rem;'>{a["icon"]}</span>
                <div>
                    <div style='font-size:0.81rem;font-weight:700;color:{nc};'>{a["name"]}</div>
                    <div style='font-size:0.7rem;color:#64748b;'>{a["desc"]}</div>
                </div>
                {'<div style="margin-left:auto;font-size:0.68rem;color:#fbbf24;font-weight:700;">✓ UNLOCKED</div>' if un else ''}
            </div>""", unsafe_allow_html=True)

        if st.session_state.xp_log:
            st.markdown("**⚡ Recent XP**")
            for e in reversed(st.session_state.xp_log[-6:]):
                st.markdown(f'<div style="font-size:0.76rem;color:#64748b;padding:0.18rem 0;">✦ {e}</div>', unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;margin-top:3rem;padding:2rem;border-top:1px solid rgba(100,120,255,0.1);'>
    <div style='font-family:"Space Grotesk",sans-serif;font-size:1.05rem;font-weight:800;
        background:linear-gradient(90deg,#4f8ef7,#7c5cfc,#22d3ee);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
        margin-bottom:0.5rem;'>AI Learning Buddy — Real-World EdTech Platform</div>
    <div style='font-size:0.77rem;color:#64748b;line-height:1.8;'>
        Powered by <b style='color:#4f8ef7;'>Google Gemini 2.5 Flash</b> &nbsp;·&nbsp;
        Multi-turn AI Chatbot &nbsp;·&nbsp; Industry Applications &nbsp;·&nbsp;
        Interview Prep &nbsp;·&nbsp; Gamified Learning &nbsp;·&nbsp;
        Built with Streamlit
    </div>
</div>
""", unsafe_allow_html=True)