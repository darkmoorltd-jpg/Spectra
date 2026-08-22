
import streamlit as st
from utils.auth import get_current_user

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")

st.title("👤 My Profile")
user = get_current_user()
if user is None:
    st.warning("Please log in first.")
else:
    st.write(f"**Email:** {user.email}")
    st.write(f"**User ID:** {user.id}")
    # Placeholder form (update later with Supabase)
    with st.form("profile_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        phone = st.text_input("Phone")
        state = st.text_input("State")
        submit = st.form_submit_button("Save Profile")
        if submit:
            st.success("Profile saved (demo only).")
