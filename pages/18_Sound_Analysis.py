
import streamlit as st
from utils.style import apply_global_style
from utils.sidebar import render_sidebar
from utils.extra_features import record_scratch_sound, analyze_sound

st.set_page_config(page_title="Sound Analysis", page_icon="🔊", layout="wide")
apply_global_style()
render_sidebar()

st.markdown('<h2 style="text-align:center;">🔊 Sound Scratch Test</h2>', unsafe_allow_html=True)

if st.button("Record Scratch (3 seconds)"):
    with st.spinner("Recording..."):
        recording, fs = record_scratch_sound()
    if recording is None:
        st.warning("⚠️ Microphone access is not available in this environment (PortAudio missing). Please use the photo-based identification instead.")
    else:
        st.success("Recording complete!")
        centroid, std = analyze_sound(recording, fs)
        if centroid is not None:
            st.write(f"Spectral Centroid: {centroid:.2f} Hz")
            st.write(f"Standard Deviation: {std:.2f}")
            st.info("This feature is experimental. Combine with image for better accuracy.")
        else:
            st.warning("Sound analysis failed. Try again or use photo identification.")
