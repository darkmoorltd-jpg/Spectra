
import streamlit as st
from utils.style import apply_global_style

st.set_page_config(page_title="Admin", page_icon="🔐", layout="wide")
apply_global_style()

st.title("🔐 Admin Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Users", "0")
col2.metric("Total Scans", "0")
col3.metric("Revenue", "₦0")
st.info("Admin features will be fully implemented with Supabase.")
