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

def get_next_question(role, history):
    if not client:
        return "⚠️ GROQ_API_KEY Missing: Check your .env file setup."

    context = f"""
You are an elite technical interviewer conducting a live interview for the '{role}' position.
Review previous conversation and ask ONLY ONE progressive technical interview question.
Do not explain. Do not give feedback. Do not ask multiple questions.
Return only the interview question.
"""

    # History format set karo
    messages = [{"role": "system", "content": context}]
    for m in history:
        # Groq standard roles use karta hai: 'user' ya 'assistant'
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