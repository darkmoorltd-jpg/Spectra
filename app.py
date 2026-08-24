
import streamlit as st
from utils.style import apply_global_style, metric_box
from utils.auth import sign_up, sign_in, sign_out, get_current_user
from utils.constants import MINERALS

st.set_page_config(page_title="SPECTRA", page_icon="⛏️", layout="wide")
apply_global_style()

# Initialize user
if "user" not in st.session_state:
    st.session_state.user = None

# Sidebar Auth
with st.sidebar:
    st.markdown("## 🔐 Account")
    user = get_current_user()
    if user is None:
        auth_choice = st.radio("Login / Signup", ["Login", "Signup"])
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if auth_choice == "Signup":
            first_name = st.text_input("First Name (optional)")
            last_name = st.text_input("Last Name (optional)")
            if st.button("Create Account"):
                if email and password:
                    with st.spinner("Creating..."):
                        user, err = sign_up(email, password, first_name, last_name)
                    if user:
                        st.session_state.user = user
                        st.success("Account created! 30 free scans added.")
                        st.rerun()
                    else:
                        st.error(err)
                else:
                    st.warning("Email and password required.")
        else:
            if st.button("Login"):
                if email and password:
                    with st.spinner("Logging in..."):
                        user, err = sign_in(email, password)
                    if user:
                        st.session_state.user = user
                        st.success("Logged in!")
                        st.rerun()
                    else:
                        st.error(err)
                else:
                    st.warning("Email and password required.")
    else:
        st.write(f"Logged in as: **{user.email}**")
        if st.button("Logout"):
            sign_out()
            st.rerun()

# Hero Section
st.markdown('<div class="hero-title">SPECTRA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">GEOLOGIST IN YOUR POCKET</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin: 2rem 0;">
    <span style="font-size:1.2rem; color:#8892b0;">Know what you've found. Get its grade. Get fair market value.</span>
</div>
""", unsafe_allow_html=True)

# Quick Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_box(f"{len(MINERALS)}+", "Minerals Recognized")
with col2:
    metric_box("₦300", "Per Scan")
with col3:
    metric_box("24/7", "Offline Ready")
with col4:
    metric_box("NGN/USD", "Live Prices")

st.markdown("---")

# Navigation cards
st.subheader("🚀 Quick Access")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/1_Scan_Mineral.py", label="🔍 Scan Mineral", use_container_width=True)
with col2:
    st.page_link("pages/2_My_History.py", label="📊 My Vault", use_container_width=True)
with col3:
    st.page_link("pages/6_Market.py", label="💹 Market Prices", use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/3_Buy_Scans.py", label="💳 Buy Scans", use_container_width=True)
with col2:
    st.page_link("pages/4_Profile.py", label="👤 Profile", use_container_width=True)

# Gamification Preview
st.markdown("---")
st.subheader("🏆 Your Achievements")
if user:
    # Placeholder for badges from Supabase
    st.markdown('<span class="badge">🔬 First Scan</span>', unsafe_allow_html=True)
    st.markdown('<span class="badge">🥇 Gold Hunter</span>', unsafe_allow_html=True)
else:
    st.info("Login to start earning badges.")

st.markdown("---")
st.caption("Powered by Darkmoor Ltd")
