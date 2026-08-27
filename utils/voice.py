
import streamlit as st
import requests
import os
import tempfile
import asyncio

def transcribe_audio(audio_bytes):
    """Transcribe audio using Groq Whisper API. Returns (text, error)."""
    try:
        api_key = st.secrets["groq"]["api_key"]
    except:
        api_key = ""
    if not api_key:
        return None, "Groq API key missing. Add it to Streamlit secrets."
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.write(audio_bytes)
    tmp.close()
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        with open(tmp.name, "rb") as f:
            files = {"file": ("audio.wav", f, "audio/wav")}
            data = {"model": "whisper-large-v3", "language": "en"}
            resp = requests.post("https://api.groq.com/openai/v1/audio/transcriptions",
                                 headers=headers, files=files, data=data, timeout=30)
        os.unlink(tmp.name)
        if resp.status_code == 200:
            text = resp.json().get("text", "").strip()
            if text:
                return text, None
            else:
                return None, "No speech detected."
        else:
            return None, f"Transcription error {resp.status_code}"
    except Exception as e:
        try:
            os.unlink(tmp.name)
        except:
            pass
        return None, str(e)

def text_to_speech(text, language="en-GB"):
    """Convert text to speech using gTTS (always works). Returns (audio_bytes, error)."""
    try:
        from gtts import gTTS
        gtts_lang = {"en-GB": "en", "ha": "ha", "yo": "yo", "ig": "ig", "pcm": "en"}
        code = gtts_lang.get(language, "en")
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=text, lang=code)
        tts.save(tmp.name)
        with open(tmp.name, "rb") as f:
            audio_bytes = f.read()
        os.unlink(tmp.name)
        return audio_bytes, None
    except Exception as e:
        return None, str(e)
