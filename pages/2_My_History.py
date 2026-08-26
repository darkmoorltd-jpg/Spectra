from utils.sidebar import render_sidebar

import streamlit as st
import pandas as pd
from utils.style import apply_global_style, badge
from utils.auth import get_current_user

st.set_page_config(page_title="My Vault", page_icon="📊", layout="wide")
render_sidebar()
apply_global_style()

st.markdown('<h2 style="text-align:center;">💎 My Vault</h2>', unsafe_allow_html=True)
user = get_current_user()
if user is None:
    st.warning("Please login to view your vault.")
else:
    # Placeholder data
    st.info("Full scan history will be stored in Supabase.")
    data = {
        "Date": ["2025-01-15", "2025-01-14", "2025-01-13"],
        "Mineral": ["Gold", "Cassiterite", "Coltan"],
        "Confidence": [94.2, 88.7, 91.5],
        "Grade": ["72%", "55%", "63%"],
        "Value": ["₦450,000", "₦220,000", "₦380,000"]
    }
    df = pd.DataFrame(data)
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        mineral_filter = st.selectbox("Filter by Mineral", ["All"] + list(df["Mineral"].unique()))
    with col2:
        date_filter = st.selectbox("Sort", ["Newest", "Oldest"])
    filtered = df if mineral_filter == "All" else df[df["Mineral"] == mineral_filter]
    st.dataframe(filtered, use_container_width=True)

    # Achievements
    st.markdown("---")
    st.subheader("🏆 Badges Earned")
    col1, col2, col3 = st.columns(3)
    with col1: badge("🔬 First Scan")
    with col2: badge("🥇 Gold Hunter")
    with col3: badge("⛏️ Pro Miner")