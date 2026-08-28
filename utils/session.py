
import streamlit as st
from supabase import create_client

@st.cache_resource(show_spinner=False)
def get_supabase_client():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def init_session():
    """Initialise user session from Supabase, caching the client."""
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        try:
            client = get_supabase_client()
            session = client.auth.get_session()
            if session and session.user:
                st.session_state.user = session.user
                # Force a rerun to update UI with user
                st.rerun()
        except Exception:
            pass
