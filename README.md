# 🤖 Enterprise AI Technical Interviewer

An advanced, production-grade GenAI Mock Interview platform built using **Streamlit**, the official **Google Gen AI SDK (Gemini 2.5 Flash)**, and **WebRTC/STT Engines**. The application simulates real-world corporate technical rounds with continuous context-aware dynamic questioning, instant speech-to-text processing, automatic voice feedback, and a complete metric analytics dashboard.

---

## 🚀 Key Features

* **Dynamic Context-Aware Questioning:** Uses Gemini 2.5 to generate progressive, non-scripted follow-up questions based on previous candidate answers.
* **Audio Orchestration Engine:** Incorporates native browser TTS (Google Text-to-Speech) loops that read questions automatically, complete with a **Repeat Question** manual override function.
* **Anti-Bypass Camera Validation:** Security logic monitors WebRTC video tracks; voice recording is strictly locked/disabled until the camera feed is live.
* **Interactive Analytics Dashboard:** Parses evaluation metrics dynamically using `Plotly` radar graphs to score Technical Depth, Communication, and Confidence.
* **Production Architecture:** Fully modular code separation dividing concerns into AI Logic, Voice Processing, and UI Components layers.

---

## 📸 Application Walkthrough & Screenshots

### 1. Initial Profile Setup Screen
*Before the session begins, the candidate inputs the target job profile and sets up the workspace parameters.*

![Initial Profile Setup Screen](screenshots/setup_screen.png)

---

### 2. Live Interview Interface (Active 1st Question)
*Once active, the system injects automatic question audio, locks verification metrics, monitors the real-time camera track, and waits for voice capture pipelines to initiate.*

![Live Interview Evaluation Screen](screenshots/live_question_1.png)

---

## 📂 Project Structure

```text
ai-pro-interviewer/
│
├── core/
│   ├── __init__.py
│   ├── ai_engine.py      # Gemini LLM Integration & Error-Proof Prompts
│   └── voice_engine.py   # Base64 Audio TTS & Speech-to-Text pipelines
│
├── ui/
│   ├── __init__.py
│   ├── components.py     # Camera, WebRTC and layout components
│   └── dashboard.py      # Plotly Scorecard Analytics & Feedback UI
│
├── app.py                # Main Router / Controller Node
├── requirements.txt      # Python Dependencies
├── .gitignore            # Git exclusion mapping
└── .env                  # Environment API Keys (Private)