
import streamlit as st
import pandas as pd

st.set_page_config(page_title="My History", page_icon="📊", layout="wide")

st.title("📊 My Scan History")
st.markdown("Your recent mineral identifications will appear here.")

# Demo history (replace with actual database queries)
if "user" in st.session_state and st.session_state.user is not None:
    user_id = st.session_state.user.id
else:
    user_id = None

if user_id is None:
    st.warning("Please log in to view your history.")
else:
    # Placeholder data
    data = {
        "Date": ["2025-01-15", "2025-01-14", "2025-01-13"],
        "Mineral": ["Gold", "Cassiterite", "Coltan"],
        "Confidence": [94.2, 88.7, 91.5],
        "Grade": ["72%", "55%", "63%"],
        "Value (₦)": ["₦450,000", "₦220,000", "₦380,000"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    st.info("Full scan history will be stored in Supabase.")
