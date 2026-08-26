
import streamlit as st
from utils.auth import sign_up, sign_in, sign_out, get_current_user

def render_sidebar():
    """Render the common sidebar for all pages."""
    with st.sidebar:
        st.markdown("## 🔐 Account")
        user = get_current_user()
        if user is None:
            auth_choice = st.radio("Login / Signup", ["Login", "Signup"])
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
        # Use page_link for navigation
        pages = [
            ("app.py", "🏠 Home"),
            ("pages/1_Scan_Mineral.py", "🔍 Scan Mineral"),
            ("pages/2_My_History.py", "📊 My Vault"),
            ("pages/6_Market.py", "💹 Market Prices"),
            ("pages/3_Buy_Scans.py", "💳 Buy Scans"),
            ("pages/4_Profile.py", "👤 Profile"),
            ("pages/7_Mineralpedia.py", "📚 Mineralpedia"),
            ("pages/8_Leaderboard.py", "🏆 Leaderboard"),
            ("pages/9_Referral.py", "🔗 Referral"),
            ("pages/10_Profit_Simulator.py", "💰 Profit Simulator"),
            ("pages/11_Buyer_Matching.py", "🤝 Find Buyers"),
            ("pages/12_Price_Alerts.py", "🔔 Price Alerts"),
            ("pages/13_Multi_Scan_Compare.py", "📈 Compare Scans"),
            ("pages/14_Exploration_Map.py", "🗺️ Exploration Map"),
            ("pages/15_Find_of_the_Day.py", "⭐ Find of the Day"),
            ("pages/16_Mining_License.py", "📜 License Guide"),
            ("pages/17_Real_Time_Video.py", "🎥 Real‑Time Video"),
            ("pages/18_Sound_Analysis.py", "🔊 Sound Analysis"),
        ]
        for path, label in pages:
            # Convert path to Streamlit page link format
            if path == "app.py":
                st.page_link("app.py", label=label, use_container_width=True)
            else:
                st.page_link(path, label=label, use_container_width=True)
