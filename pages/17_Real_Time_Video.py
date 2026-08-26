from utils.sidebar import render_sidebar

import streamlit as st
from utils.style import apply_global_style

st.set_page_config(page_title="Real-Time Video", page_icon="🎥", layout="wide")
render_sidebar()
apply_global_style()

st.markdown('<h2 style="text-align:center;">🎥 Real‑Time Mineral Analysis</h2>', unsafe_allow_html=True)
st.warning("Real‑time video processing is currently in beta. Requires streamlit-webrtc. Please use Upload Video for now.")