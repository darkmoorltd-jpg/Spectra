
import streamlit as st
import streamlit.components.v1 as components

def save_session_to_local_storage(user_email, access_token):
    js = f"""
    <script>
    localStorage.setItem('spectra_user_email', '{user_email}');
    localStorage.setItem('spectra_access_token', '{access_token}');
    </script>
    """
    components.html(js, height=0)

def load_session_from_local_storage():
    # Use a hidden iframe to read localStorage and pass back to Streamlit
    # For now, we just check st.session_state
    if "user" not in st.session_state:
        st.session_state.user = None
    return st.session_state.user
