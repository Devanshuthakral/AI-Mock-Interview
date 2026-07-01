import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Env variables load karo
load_dotenv(override=True)
api_key = os.getenv("GROQ_API_KEY")

# Groq Client initialize karo
if api_key:
    client = Groq(api_key=api_key)
else:
    client = None

# Sabse tez aur best free model technical interview ke liye
MODEL_NAME = "llama-3.3-70b-versatile"


def check_ats_score(resume_text, job_description):
    """
    Compares the uploaded resume with the Job Description using Groq.
    Returns scores, missing keywords, and screening verdict.
    """
    if not client:
        return "⚠️ GROQ_API_KEY Missing: Cannot parse ATS score."

    prompt = f"""
You are an advanced ATS (Applicant Tracking System) algorithm and an expert HR data scientist.
Analyze the provided Resume Text against the Job Description (JD).

Return the evaluation strictly in this markdown format:

### 📊 ATS Match Score: xx%
---
**Verdict:** [Proceed to Interview] OR [Resume Needs Improvement - Missing Core Skills]
---
### 🔍 Detailed Breakdown:
* **Missing Key Skills/Keywords:** - ...
* **Profile Optimization Feedback:** - ...
* **Why this verdict?** - ...

Job Description (JD):
{job_description}

Resume Text:
{resume_text}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ATS Screening Error: {str(e)}"


def get_next_question(role, history, job_desc=""):
    """
    Generates the next interview question based on the role, previous history,
    and optionally tailors it to the provided Job Description (JD).
    """
    if not client:
        return "⚠️ GROQ_API_KEY Missing: Check your .env file setup."

    # Baseline context
    context = f"You are an elite technical interviewer conducting a live interview for the '{role}' position."
    
    # Agar Job Description available hai, toh context ko customize karo
    if job_desc:
        context += f"\nHere is the target Job Description for this role:\n{job_desc}\nTailor your questions to map these exact requirements."

    context += """
Review the previous conversation history and ask ONLY ONE progressive technical interview question.
CRITICAL LAWS:
1. Return ONLY the plain text of the question.
2. Do NOT use markdown formatting, do NOT use bold marks (**), and do NOT use bullet points.
3. Do NOT explain or give feedback during the conversation.
4. Keep the question crisp and straightforward.
"""

    # History format set karo
    messages = [{"role": "system", "content": context}]
    for m in history:
        role_type = "assistant" if m['role'] == "interviewer" else "user"
        messages.append({"role": role_type, "content": m['content']})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Groq AI Error: {str(e)}"


def get_final_analytics(role, history):
    if not client:
        return "Technical Score: 0/100\nVerdict:\nNo Hire\nFeedback:\nGroq API Key Missing"

    context = f"You are a senior hiring manager. Analyze this interview for the role: {role}. Return exactly in the requested format."
    
    messages = [{"role": "system", "content": context}]
    
    formatted_transcript = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in history])
    
    prompt = f"""
Analyze this interview transcript and score it.
Return exactly in this format.

Technical Score: xx/100
Communication Score: xx/100
Confidence Score: xx/100
---
Verdict:
Strong Hire / Hire / No Hire

Feedback:
Strengths:
- ...
Weaknesses:
- ...
Suggestions:
- ...

Interview Transcript:
{formatted_transcript}
"""
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Technical Score: 0/100\n---\nVerdict:\nError\n\nFeedback:\nAI Error: {str(e)}"