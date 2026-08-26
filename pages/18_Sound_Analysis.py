from utils.sidebar import render_sidebar

import streamlit as st
from utils.style import apply_global_style
from utils.extra_features import record_scratch_sound, analyze_sound

st.set_page_config(page_title="Sound Analysis", page_icon="🔊", layout="wide")
render_sidebar()
apply_global_style()

st.markdown('<h2 style="text-align:center;">🔊 Sound Scratch Test</h2>', unsafe_allow_html=True)

if st.button("Record Scratch (3 seconds)"):
    with st.spinner("Recording..."):
        recording, fs = record_scratch_sound()
    st.success("Recording complete!")
    centroid, std = analyze_sound(recording, fs)
    st.write(f"Spectral Centroid: {centroid:.2f} Hz")
    st.write(f"Standard Deviation: {std:.2f}")
    st.info("This feature is experimental. Combine with image for better accuracy.")