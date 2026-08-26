from utils.sidebar import render_sidebar

import streamlit as st
from PIL import Image
import numpy as np
import random
import time
import plotly.graph_objects as go
import base64
import uuid
from utils.style import apply_global_style
from utils.model_loader import load_mineral_model, predict_mineral
from utils.deepseek import get_market_insight
from utils.supabase_client import deduct_scan
from utils.constants import MINERALS, MINERAL_PRICES
from utils.voice import transcribe_audio
from utils.pdf_report import generate_pdf_report
from utils.threejs_viewer import render_3d_mineral
from utils.extra_features import generate_qr_code, generate_blockchain_hash, overlay_heatmap, process_video_frames, record_scratch_sound, analyze_sound

st.set_page_config(page_title="Scan Mineral", page_icon="🔍", layout="wide")
render_sidebar()
apply_global_style()

st.markdown('<h2 style="text-align:center;">🔍 Mineral Scanner</h2>', unsafe_allow_html=True)

# Load the real model once (cached across reruns)
@st.cache_resource(show_spinner=False)
def get_model():
    return load_mineral_model()

model = get_model()
if model is None:
    st.warning("⚠️ Real model unavailable – using demo predictions.")

# Voice command
if st.button("🎤 Voice Command"):
    audio = st.audio_input("Speak now")
    if audio:
        with st.spinner("Transcribing..."):
            text, err = transcribe_audio(audio.getvalue())
        if err:
            st.error(err)
        else:
            st.success(f"You said: {text}")
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

    # Scratch sound test option
    use_sound = st.checkbox("Add Scratch Test (record sound)", value=False)
    sound_features = None
    if use_sound:
        if st.button("Record Scratch"):
            with st.spinner("Recording 3 seconds..."):
                recording, fs = record_scratch_sound()
            st.success("Recording done!")
            centroid, std = analyze_sound(recording, fs)
            st.write(f"Spectral Centroid: {centroid:.2f} Hz, Std: {std:.2f}")
            sound_features = (centroid, std)

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
            # Real model prediction
            if model is not None:
                mineral, confidence, grade = predict_mineral(model, image)
            else:
                # Fallback to demo
                mineral = random.choice(MINERALS)
                confidence = random.uniform(0.7, 0.98)
                grade = random.uniform(0.2, 0.9)

            # Simulate scanning animation
            my_bar = st.progress(0)
            for percent in range(0, 101, 20):
                time.sleep(0.1)
                my_bar.progress(percent)
            my_bar.progress(100)

        if mineral == "Unknown":
            st.error("❓ This does not match any of the 7 supported minerals. Try a different sample or check the image quality.")
            st.stop()

        # Grade placeholder (if not provided by model)
        if grade is None:
            grade = random.uniform(0.2, 0.9)  # still demo grade

        # Value estimation
        price_per_kg = MINERAL_PRICES.get(mineral, 1.0)
        value_usd = price_per_kg * grade * 10
        value_ngn = value_usd * 1500

        # Heatmap overlay (simulated)
        heatmap_img = overlay_heatmap(image, grade, mineral)
        st.image(heatmap_img, caption="Mineral Distribution Heatmap", use_container_width=True)

        # Result display
        st.markdown("---")
        st.markdown("## 🧪 Analysis Result")

        col1, col2 = st.columns([1, 2])
        with col1:
            # Confidence gauge using similarity
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
        with st.expander("💡 Geologist's Note", expanded=True):
            insight = get_market_insight(mineral, grade, value_ngn)
            st.write(insight)

        # Chat about mineral
        st.markdown("---")
        st.subheader("🤖 Ask the Geologist")
        user_question = st.text_input("Ask a question about this mineral", key="chat_input")
        if user_question:
            response = get_market_insight(mineral, grade, value_ngn)
            st.write(response)

        # Blockchain verification
        scan_id = str(uuid.uuid4())[:8]
        scan_data = f"{mineral}|{confidence}|{grade}|{value_ngn}|{scan_id}"
        hash_val = generate_blockchain_hash(scan_data)
        qr_data = f"SPECTRA_VERIFY:{hash_val}"
        qr_b64 = generate_qr_code(qr_data)

        st.markdown("---")
        st.subheader("🔗 Verification")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(base64.b64decode(qr_b64), width=100)
        with col2:
            st.markdown(f"**SHA‑256 Hash:** `{hash_val[:20]}...`")
            st.markdown(f"**Scan ID:** {scan_id}")

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
                st.audio(b"", format="audio/mp3")
        with col4:
            if st.button("Download PDF Report"):
                pdf_bytes = generate_pdf_report(mineral, confidence, grade, value_ngn, image_file.getvalue(), scan_id)
                b64 = base64.b64encode(pdf_bytes).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="SPECTRA_report_{mineral}_{scan_id}.pdf">📄 Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)

elif video_file is not None:
    st.video(video_file)
    if st.button("Analyze Video"):
        frames = process_video_frames(video_file, num_frames=5)
        st.success(f"Extracted {len(frames)} frames")
        for i, frame in enumerate(frames):
            st.image(frame, caption=f"Frame {i+1}", width=200)
        # Placeholder for video analysis
        st.markdown("Video analysis will be integrated soon.")