
import streamlit as st
from utils.auth import sign_up, sign_in, sign_out, get_current_user

st.set_page_config(page_title="SPECTRA", page_icon="⛏️", layout="wide")

# Initialize user in session state if not present
if "user" not in st.session_state:
    st.session_state.user = None

# Sidebar authentication
with st.sidebar:
    st.title("🔐 Account")
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
                    with st.spinner("Creating account..."):
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

# Main content
st.title("⛏️ SPECTRA – Mineral Identification AI")
st.markdown("#### Know what you've found. Get its grade. Get fair market value.")

st.info("""
**How it works:**
1. Take a clear photo of your mineral / ore sample.
2. SPECTRA identifies the mineral and estimates grade.
3. Get current market value in Naira and USD.
4. Find the best place to sell.

👉 Use the **Scan Mineral** page to start.
""")

# Quick stats
col1, col2, col3 = st.columns(3)
col1.metric("Minerals Recognized", "10+")
col2.metric("Scan Cost", "₦300")
col3.metric("Countries Served", "Nigeria (beta)")

st.markdown("---")
st.caption("Powered by Darkmoor Ltd")
