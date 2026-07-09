# 🎓 AI Learning Buddy — Real-World EdTech Platform 🏆

![AI Learning Buddy](https://img.shields.io/badge/Status-Hackathon%20Ready-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B?style=for-the-badge&logo=streamlit)
![Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini%202.5%20Flash-8E75B2?style=for-the-badge)

Welcome to the **AI Learning Buddy**, a gamified, adaptive, and highly interactive EdTech platform built for modern learners. This project was developed as a hackathon submission to demonstrate the power of Generative AI in education.

---

## ✨ Features (Grand Prize Edition)

The platform goes far beyond a simple chatbot. It provides a complete, 9-tab interactive learning environment:

1. **📖 Learn Concepts:** Adaptive explanations with real-world analogies tailored to your level (Beginner, Intermediate, Expert).
2. **🤖 Multi-turn AI Chatbot:** Have a full conversation with BinaryBot! Features memory, quick-reply suggestion chips, and beautiful chat bubbles.
3. **🎮 Gamification (XP & Badges):** Earn XP for every action, level up from *Seedling* 🌱 to *Master* 🏆, and unlock 15 unique achievement badges.
4. **🧠 Smart Graded Quiz:** Generate a 5-question multiple-choice quiz, type your answers, and let the AI grade it instantly with a final score (X/5) and feedback.
5. **🌍 Industry Applications:** See exactly how top companies (Google, Amazon, Uber, etc.) use your topic in production across 5 different industries.
6. **💼 Career & Interview Prep:** Instantly generate 8 real-world interview questions, model answers, and pro-tips for job seekers.
7. **📅 Study Plan Generator:** Get a 4-week personalized roadmap to master any topic.
8. **🗺️ Concept Maps:** Generates a visual ASCII tree diagram mapping out sub-topics and relationships.
9. **📝 Study Notes Library:** Save your favorite explanations, quizzes, and code snippets into a personal, session-based study library.
10. **💻 Code Examples & 🃏 Flashcards:** Generate production-quality Python code or spaced-repetition flashcards with memory tricks.

---

## 🚀 How to Run Locally

### 1. Prerequisites
Make sure you have Python installed (Python 3.10+ recommended).

### 2. Install Dependencies
Open your terminal and install the required packages:
```bash
pip install -r requirements.txt
```
*(Dependencies include `streamlit` and `google-generativeai`)*

### 3. API Key Setup
The application requires a **Google Gemini API Key**.
By default, the key is hardcoded in `app.py` for immediate hackathon testing. If you need to change it, replace the `GEMINI_API_KEY` variable at the top of `app.py` with your own key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```
The application will open automatically in your browser at `http://localhost:8501`.

---

## 🛠️ Technology Stack

* **Frontend/UI:** [Streamlit](https://streamlit.io/) with heavy custom CSS for animations, glassmorphism, gradients, and custom layouts.
* **LLM Backend:** Google's `google-generativeai` SDK.
* **Model:** `gemini-2.5-flash` for high-speed, cost-effective, and intelligent responses.
* **Prompt Engineering:** Extensive role-prompting, few-shot prompting, and strict output formatting instructions.

---

## 🎯 The "Why" behind the project
Traditional tutorials are static. Learners often struggle with concepts because they don't see the *real-world application* or they aren't engaged. 

**AI Learning Buddy** solves this by:
1. Adapting the language complexity to the user's level.
2. Gamifying the experience to encourage continuous exploration.
3. Bridging the gap between academic theory and industry reality (via the Real-World Apps & Interview Prep tabs).

---
