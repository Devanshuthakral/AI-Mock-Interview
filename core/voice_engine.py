import speech_recognition as sr
from gtts import gTTS
import base64
import io

def generate_audio_base64(text):
    """Generates a clean base64 string from gTTS text for direct native player rendering."""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        b64 = base64.b64encode(mp3_fp.read()).decode()
        return b64
    except Exception as e:
        return None

def listen_to_user():
    """Captures speech with wide limits to prevent truncating long structural definitions."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Increase duration to accurately parse and suppress deep room echo/background noise
        recognizer.adjust_for_ambient_noise(source, duration=1.2)
        try:
            # timeout=12 (waits for speaker to start), phrase_time_limit=45 (allows long answers)
            audio = recognizer.listen(source, timeout=12, phrase_time_limit=45)
            return recognizer.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            return "ERROR: Audio clarity was too low. Please speak closer to the microphone."
        except sr.WaitTimeoutError:
            return "ERROR: Silence detected. Please check your mic connection and try again."