from utils.sidebar import render_sidebar

import streamlit as st
from utils.style import apply_global_style

st.set_page_config(page_title="Find of the Day", page_icon="⭐", layout="wide")
render_sidebar()
apply_global_style()

st.markdown('<h2 style="text-align:center;">⭐ Community Find of the Day</h2>', unsafe_allow_html=True)

# Demo submissions
submissions = [
    {"mineral": "Malachite", "user": "Aisha B.", "votes": 120, "image": "https://via.placeholder.com/150"},
    {"mineral": "Gold", "user": "Ibrahim M.", "votes": 98, "image": "https://via.placeholder.com/150"},
    {"mineral": "Cassiterite", "user": "David O.", "votes": 75, "image": "https://via.placeholder.com/150"}
]
for s in submissions:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(s["image"], width=100)
    with col2:
        st.markdown(f"**{s['mineral']}** by {s['user']}")
        st.markdown(f"👍 {s['votes']} votes")
        st.button(f"Vote for {s['mineral']}", key=s['mineral'])