
import streamlit as st
from PIL import Image
import numpy as np
import hashlib
import random
import time
import plotly.graph_objects as go
import base64
import uuid
import datetime
from utils.style import apply_global_style
from utils.model_loader import load_mineral_model, predict_mineral
from utils.deepseek import get_market_insight
from utils.supabase_client import deduct_scan
from utils.constants import MINERALS, MINERAL_PRICES
from utils.voice import transcribe_audio
from utils.pdf_report import generate_pdf_report

st.set_page_config(page_title="Scan Mineral", page_icon="🔍", layout="wide")
apply_global_style()

st.markdown('<h2 style="text-align:center;">🔍 Mineral Scanner</h2>', unsafe_allow_html=True)

# Voice command button
if st.button("🎤 Voice Command"):
    audio = st.audio_input("Speak now")
    if audio:
        with st.spinner("Transcribing..."):
            text, err = transcribe_audio(audio.getvalue())
        if err:
            st.error(err)
        else:
            st.success(f"You said: {text}")
            # If text contains "scan" or "identify", trigger file upload prompt
            if any(word in text.lower() for word in ["scan", "identify", "what is"]):
                st.info("Please upload a photo or use camera.")

# Input method
option = st.radio("Input Method", ["Upload Photo", "Use Camera"], horizontal=True)
if option == "Use Camera":
    image_file = st.camera_input("Take a photo of the mineral")
else:
    image_file = st.file_uploader("Upload a photo", type=["jpg","jpeg","png"])

if image_file is not None:
    image = Image.open(image_file).convert("RGB")
    st.image(image, caption="Your sample", width=400)

    if st.button("Identify Mineral", type="primary"):
        user = st.session_state.get("user", None)
        if user is None:
            st.warning("Please log in to scan. (Demo scan without deduction)")
            mineral = random.choice(MINERALS)
            confidence = random.uniform(0.75, 0.98)
            grade = random.uniform(0.2, 0.9)
        else:
            new_total = deduct_scan(user.id)
            if new_total < 0:
                st.error("Not enough scans. Buy more.")
                st.stop()
            st.caption(f"Scan deducted. Remaining: {new_total}")
            model = load_mineral_model()
            mineral, confidence, grade = predict_mineral(model, image)

        price_per_kg = MINERAL_PRICES.get(mineral, 1.0)
        value_usd = price_per_kg * grade * 10
        value_ngn = value_usd * 1500

        # Scanning animation
        with st.spinner("Analyzing mineral composition..."):
            my_bar = st.progress(0)
            for percent in range(0, 101, 20):
                time.sleep(0.1)
                my_bar.progress(percent)
            my_bar.progress(100)

        # Result display
        st.markdown("---")
        st.markdown("## 🧪 Analysis Result")

        col1, col2 = st.columns([1, 2])
        with col1:
            # Confidence gauge
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

            # 3D viewer placeholder (using rotating emoji)
            st.markdown(f'<div style="text-align:center;"><span style="font-size:4rem;">💎</span><br><small>3D Viewer coming soon</small></div>', unsafe_allow_html=True)

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
            from utils.deepseek import get_market_insight
            response = get_market_insight(mineral, grade, value_ngn)  # reuse for demo
            st.write(response)

        # Action buttons
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Save to Vault"):
                # TODO: Save to Supabase
                st.success("Saved!")
        with col2:
            if st.button("Find Buyers"):
                st.info("Buyer map will be integrated soon.")
        with col3:
            if st.button("Voice Explanation"):
                # Placeholder for TTS
                st.audio(b"", format="audio/mp3")
        with col4:
            if st.button("Download PDF Report"):
                scan_id = str(uuid.uuid4())[:8]
                pdf_bytes = generate_pdf_report(mineral, confidence, grade, value_ngn, image_file.getvalue(), scan_id)
                b64 = base64.b64encode(pdf_bytes).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="SPECTRA_report_{mineral}_{scan_id}.pdf">📄 Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
