
import streamlit as st
import requests
import os
import tempfile

def transcribe_audio(audio_bytes):
    """Transcribe audio using Groq Whisper API."""
    try:
        api_key = st.secrets["groq"]["api_key"]
    except:
        api_key = ""
    if not api_key:
        return None, "Groq API key missing"
    # Save audio to temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.write(audio_bytes)
    tmp.close()
    headers = {"Authorization": f"Bearer {api_key}"}
    with open(tmp.name, "rb") as f:
        files = {"file": ("audio.wav", f, "audio/wav")}
        data = {"model": "whisper-large-v3", "language": "en"}
        resp = requests.post("https://api.groq.com/openai/v1/audio/transcriptions",
                             headers=headers, files=files, data=data)
    os.unlink(tmp.name)
    if resp.status_code == 200:
        return resp.json().get("text", "").strip(), None
    else:
        return None, f"Transcription error {resp.status_code}"
