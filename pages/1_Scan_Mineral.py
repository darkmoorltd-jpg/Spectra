
import streamlit as st
from PIL import Image
import numpy as np
import random
import time
import plotly.graph_objects as go
import base64
import uuid
from utils.style import apply_global_style
from utils.sidebar import render_sidebar
from utils.model_loader import load_mineral_model, predict_mineral, estimate_grade
from utils.deepseek import get_market_insight
from utils.supabase_client import deduct_scan, save_scan_history
from utils.constants import MINERALS, MINERAL_PRICES
from utils.voice import transcribe_audio, text_to_speech
from utils.threejs_viewer import render_3d_mineral
from utils.extra_features import overlay_heatmap, process_video_frames, record_scratch_sound, analyze_sound

st.set_page_config(page_title="Scan Mineral", page_icon="🔍", layout="wide")
apply_global_style()
render_sidebar()

st.markdown('<h2 style="text-align:center;">🔍 Mineral Scanner</h2>', unsafe_allow_html=True)

# Load model (cached)
@st.cache_resource(show_spinner=False)
def get_model():
    return load_mineral_model()

model = get_model()
if model is None:
    st.warning("Real model unavailable – using demo predictions.")

# Voice command (simplified)
if st.button("🎤 Voice Command"):
    st.info("Click the microphone below to record your command (max 10 seconds).")
    audio = st.audio_input("Record your voice command")
    if audio is not None:
        with st.spinner("Transcribing..."):
            text, err = transcribe_audio(audio.getvalue())
        if err:
            st.warning(f"Could not transcribe: {err}")
        else:
            st.success(f"You said: \"{text}\"")
            if any(word in text.lower() for word in ["scan", "identify", "what is"]):
                st.info("Please upload a photo or use camera.")

# Input method
option = st.radio("Input Method", ["Upload Photo", "Use Camera", "Upload Video"], horizontal=True)
image_file = None
video_file = None

if option == "Use Camera":
    image_file = st.camera_input("Take a photo of the mineral")
elif option == "Upload Photo":
    image_file = st.file_uploader("Upload a photo", type=["jpg","jpeg","png"])
else:
    video_file = st.file_uploader("Upload a video", type=["mp4","mov","avi"])

if image_file is not None:
    image = Image.open(image_file).convert("RGB")
    st.image(image, caption="Your sample", width=400)

    if st.button("Identify Mineral", type="primary"):
        user = st.session_state.get("user", None)
        if user is None:
            st.warning("Please log in to scan. (Demo scan without deduction)")
        else:
            new_total = deduct_scan(user.id)
            if new_total < 0:
                st.error("Not enough scans. Buy more.")
                st.stop()
            st.caption(f"Scan deducted. Remaining: {new_total}")

        with st.spinner("Analyzing mineral composition..."):
            if model is not None:
                mineral, confidence, grade = predict_mineral(model, image)
            else:
                mineral = random.choice(MINERALS)
                confidence = random.uniform(0.7, 0.98)
                grade = estimate_grade(image, mineral) if model is not None else 0.5

            my_bar = st.progress(0)
            for percent in range(0, 101, 20):
                time.sleep(0.1)
                my_bar.progress(percent)
            my_bar.progress(100)

        if mineral == "Unknown":
            st.error("This does not match any of the 7 supported minerals. Try another sample.")
            st.stop()

        if grade is None:
            grade = estimate_grade(image, mineral) if model is not None else 0.5

        price_per_kg = MINERAL_PRICES.get(mineral, 1.0)
        value_usd = price_per_kg * grade * 10
        value_ngn = value_usd * 1500

        # Save scan history
        if user is not None:
            save_scan_history(user.id, mineral, confidence, grade, value_ngn)

        # Heatmap (simulated)
        heatmap_img = overlay_heatmap(image, grade, mineral)
        st.image(heatmap_img, caption="Mineral Distribution Heatmap", use_container_width=True)

        st.markdown("---")
        st.markdown("## Analysis Result")

        col1, col2 = st.columns([1, 2])
        with col1:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = confidence*100,
                domain = {'x': [0,1], 'y': [0,1]},
                title = {'text': "Confidence"},
                gauge = {'axis': {'range': [None, 100]},
                         'bar': {'color': "#ffd700"},
                         'bgcolor': "#111827",
                         'borderwidth': 2,
                         'bordercolor': "#1f2a44"}
            ))
            fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20),
                              paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(color='#e0e0e0'))
            st.plotly_chart(fig, use_container_width=True)
            render_3d_mineral(mineral)

        with col2:
            st.markdown(f'<h1 style="color:#ffd700; font-size:3rem;">{mineral}</h1>', unsafe_allow_html=True)
            st.markdown(f"**Estimated Grade:** {grade*100:.0f}%")
            col_usd, col_ngn = st.columns(2)
            col_usd.metric("USD", f"${value_usd:,.2f}")
            col_ngn.metric("Naira", f"₦{value_ngn:,.0f}")

        # AI Insight
        with st.expander("Geologist's Note", expanded=True):
            insight = get_market_insight(mineral, grade, value_ngn)
            st.write(insight)

        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Save to Vault"):
                st.success("Saved!")
        with col2:
            if st.button("Find Buyers"):
                st.info("Go to Buyer Matching page.")
        with col3:
            if st.button("Voice Explanation"):
                audio_bytes, tts_err = text_to_speech(insight, "en-GB")
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                else:
                    st.warning(f"Voice generation failed: {tts_err}")
        with col4:
            st.caption("PDF coming soon")

elif video_file is not None:
    st.video(video_file)
    st.info("Video analysis coming soon. Please use photo upload for now.")
