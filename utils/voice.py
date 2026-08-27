
import streamlit as st
import requests
import os
import tempfile
import asyncio

def transcribe_audio(audio_bytes):
    """Transcribe audio using Groq Whisper API."""
    try:
        api_key = st.secrets["groq"]["api_key"]
    except:
        api_key = ""
    if not api_key:
        return None, "Groq API key missing"
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

def text_to_speech(text, language="en-GB"):
    """Convert text to speech using edge-tts (free) with fallback to gTTS.
    Returns (audio_bytes, error_msg). Imports are lazy to avoid errors."""
    voices = {
        "en-GB": "en-GB-SoniaNeural",
        "en-US": "en-US-JennyNeural",
        "pcm": "en-GB-RyanNeural",
        "ha": "ha-NG-MuhammedNeural",
        "yo": "yo-NG-AbimbolaNeural",
        "ig": "ig-NG-ChidinmaNeural",
    }
    gtts_lang = {
        "en-GB": "en",
        "en-US": "en",
        "pcm": "en",
        "ha": "ha",
        "yo": "yo",
        "ig": "ig",
    }
    voice = voices.get(language, "en-GB-SoniaNeural")
    gtts_code = gtts_lang.get(language, "en")

    # Try edge-tts (lazy import)
    try:
        import edge_tts
        async def gen():
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(tmp.name)
            return tmp.name
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_path = loop.run_until_complete(gen())
        loop.close()
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        os.unlink(audio_path)
        return audio_bytes, None
    except Exception as e:
        pass

    # Fallback to gTTS (lazy import)
    try:
        from gtts import gTTS
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=text, lang=gtts_code)
        tts.save(tmp.name)
        with open(tmp.name, "rb") as f:
            audio_bytes = f.read()
        os.unlink(tmp.name)
        return audio_bytes, None
    except Exception as e2:
        return None, str(e2)
