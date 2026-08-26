
import streamlit as st
from utils.auth import sign_up, sign_in, sign_out, get_current_user

def render_sidebar():
    with st.sidebar:
        st.markdown("## 🔐 Account")
        user = get_current_user()
        if user is None:
            auth_choice = st.radio("Login / Signup", ["Login", "Signup"], key="sidebar_auth_choice")
            email = st.text_input("Email", key="sidebar_email")
            password = st.text_input("Password", type="password", key="sidebar_password")
            if auth_choice == "Signup":
                first_name = st.text_input("First Name (optional)", key="sidebar_first")
                last_name = st.text_input("Last Name (optional)", key="sidebar_last")
                if st.button("Create Account", key="sidebar_signup_btn"):
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
                if st.button("Login", key="sidebar_login_btn"):
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
            if st.button("Logout", key="sidebar_logout_btn"):
                sign_out()
                st.rerun()

        st.markdown("---")
        st.markdown("### 🚀 Quick Navigation")
        # Use markdown links instead of st.page_link for better compatibility
        pages = [
            ("🏠 Home", "/"),
            ("🔍 Scan Mineral", "/Scan_Mineral"),
            ("📊 My Vault", "/My_History"),
            ("💹 Market Prices", "/Market"),
            ("💳 Buy Scans", "/Buy_Scans"),
            ("👤 Profile", "/Profile"),
            ("📚 Mineralpedia", "/Mineralpedia"),
            ("🏆 Leaderboard", "/Leaderboard"),
            ("🔗 Referral", "/Referral"),
            ("💰 Profit Simulator", "/Profit_Simulator"),
            ("🤝 Find Buyers", "/Buyer_Matching"),
            ("🔔 Price Alerts", "/Price_Alerts"),
            ("📈 Compare Scans", "/Multi_Scan_Compare"),
            ("🗺️ Exploration Map", "/Exploration_Map"),
            ("⭐ Find of the Day", "/Find_of_the_Day"),
            ("📜 License Guide", "/Mining_License"),
            ("🎥 Real‑Time Video", "/Real_Time_Video"),
            ("🔊 Sound Analysis", "/Sound_Analysis"),
        ]
        for label, path in pages:
            st.markdown(f"[{label}]({path})")
