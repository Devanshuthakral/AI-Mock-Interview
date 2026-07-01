# 🤖 Enterprise AI Technical Interviewer

An advanced, production-grade GenAI Mock Interview platform built using **Streamlit**, **Groq Cloud API (Llama 3.3 70B)**, and **WebRTC/STT Engines**. The application simulates real-world corporate technical rounds with continuous context-aware dynamic questioning, instant speech-to-text processing, automatic voice feedback, and a complete metric analytics dashboard.

---

## 🚀 Key Features

* **Dynamic Context-Aware Questioning:** Uses state-of-the-art LLMs via Groq to generate progressive, non-scripted follow-up questions based on previous candidate answers.
* **Audio Orchestration Engine:** Incorporates native browser TTS (Google Text-to-Speech) loops that read questions automatically, complete with a **Repeat Question** manual override function.
* **Anti-Bypass Camera Validation:** Security logic monitors WebRTC video tracks; voice recording and audio pipelines are strictly locked/disabled until the camera feed is live.
* **Interactive Analytics Dashboard:** Parses evaluation metrics dynamically to render real-time comparative charts scoring Technical Depth, Communication, and Confidence.
* **Production Architecture:** Fully modular code separation dividing concerns into AI Logic, Voice Processing, and UI Components layers.

---

## 📸 Application Walkthrough & Screenshots

### 1. Initial Profile Setup Screen
*Before the session begins, the candidate inputs the target job profile and sets up the workspace parameters.*

![Initial Profile Setup Screen](screenshots/setup_screen.png)

---

### 2. Live Interview Interface
*Once active, the system injects automatic question audio, locks verification metrics, monitors the real-time camera track, and waits for voice capture pipelines to initiate.*

![Live Interview Evaluation Screen](screenshots/live_question_1.png)

---

### 3. Post-Interview Performance Analytics
*After completing the set number of questions, the system aggregates session logs, parses the text stream, and displays a dynamic performance chart along with granular strengths and weaknesses analysis.*

![Interview Performance Analytics](screenshots/analytics_dashboard.png)
![AI Interviewer Detailed Feedback](screenshots/detailed_feedback.png)

---

## 📂 Project Structure

```text
ai-pro-interviewer/
│
├── core/
│   ├── __init__.py
│   ├── ai_engine.py      # Groq LLM Integration & Error-Proof Prompts
│   └── voice_engine.py   # Base64 Audio TTS & Speech-to-Text pipelines
│
├── ui/
│   ├── __init__.py
│   ├── components.py     # Camera, WebRTC and layout components
│   └── dashboard.py      # Scorecard Analytics Charts & Feedback UI
│
├── app.py                # Main Router / Controller Node
├── requirements.txt      # Python Dependencies
├── .env                  # Environment API Keys (Private)
└── README.md             # Project Documentation