import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

def get_next_question(role, history):
    if not client: return "API Key Missing"
    
    context = f"""
    You are an elite technical interviewer conducting a live video interview for the '{role}' position.
    Review the previous history and ask exactly ONE relevant, progressive technical question.
    Do not give feedback or multi-part questions. Keep it crisp.
    """
    formatted_history = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in history])
    prompt = f"{context}\n\nHistory:\n{formatted_history}\n\nInterviewer:"
    
    response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)
    return response.text

def get_final_analytics(role, history):
    if not client: return "API Key Missing"
    
    prompt = f"""
    You are a principal hiring panel. Analyze this interview transcript for the '{role}' role.
    Provide a final report strictly in the following format:
    Technical Score: [0-100]
    Communication Score: [0-100]
    Confidence Score: [0-100]
    ---
    Verdict: [Strong Hire / Hire / No Hire]
    Detailed Feedback: <Write core strengths and areas of improvement here>
    """
    formatted_history = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in history])
    
    response = client.models.generate_content(model='gemini-1.5-flash', contents=f"{prompt}\n\nTranscript:\n{formatted_history}")
    return response.text