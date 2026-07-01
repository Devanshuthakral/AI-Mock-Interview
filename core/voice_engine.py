import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import io
import base64

def generate_audio_base64(text):
    """
    Convert AI response to Base64 MP3 for autoplay.
    """
    try:
        tts = gTTS(text=text, lang="en", slow=False)

        mp3_buffer = io.BytesIO()
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)

        audio_base64 = base64.b64encode(
            mp3_buffer.read()
        ).decode("utf-8")

        return audio_base64

    except Exception as e:
        print(f"Audio Generation Error: {e}")
        return None


def listen_to_user():
    """
    Streamlit audio_input se voice capture karke text me convert karega.
    """
    # UI pe record button dikhayega
    audio_file = st.audio_input("Record Your Answer", key="voice_input_widget")

    if audio_file is None:
        return None

    recognizer = sr.Recognizer()

    # Streamlit ke audio buffer data ko read karo
    audio_bytes = audio_file.read()

    # Temporary file me save karo taaki SpeechRecognition read kar sake
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio_bytes)
        temp_path = temp_file.name

    try:
        # File ko standard audio source ki tarah open karo
        with sr.AudioFile(temp_path) as source:
            # Noise kam karne ke liye ambient adjust lagaya
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)

        # Google Speech Recognition API se text nikalo
        text = recognizer.recognize_google(
            audio_data,
            language="en-US"
        )
        return text

    except sr.UnknownValueError:
        return "ERROR: Audio clear nahi tha, please dobara bolein."

    except sr.RequestError:
        return "ERROR: Speech Recognition service down hai ya internet nahi chal raha."

    except Exception as e:
        return f"ERROR: {str(e)}"

    finally:
        # Taaki local storage full na ho, temp file har baar delete hogi
        if os.path.exists(temp_path):
            os.remove(temp_path)