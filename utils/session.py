
import streamlit as st
from supabase import create_client

def init_session():
    """Initialise user session from Supabase if not already in st.session_state."""
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        try:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
            client = create_client(url, key)
            session = client.auth.get_session()
            if session and session.user:
                st.session_state.user = session.user
        except Exception:
            pass
