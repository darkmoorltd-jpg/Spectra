
import streamlit as st
from supabase import create_client, Client

def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def get_service_client():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["service_key"]
    return create_client(url, key)

def sign_up(email, password, first_name="", last_name=""):
    """Create a new user and initialize scans."""
    client = get_supabase()
    try:
        res = client.auth.sign_up({"email": email, "password": password})
        if res.user:
            service = get_service_client()
            service.table("user_scans").insert({
                "user_id": res.user.id,
                "scans_remaining": 30,
                "plan": "free"
            }).execute()
            service.table("user_profiles").insert({
                "user_id": res.user.id,
                "first_name": first_name,
                "last_name": last_name
            }).execute()
            return res.user, None
        else:
            return None, "Signup failed"
    except Exception as e:
        return None, str(e)

def sign_in(email, password):
    """Log in existing user."""
    client = get_supabase()
    try:
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            return res.user, None
        else:
            return None, "Login failed"
    except Exception as e:
        return None, str(e)

def sign_out():
    """Sign out current user."""
    client = get_supabase()
    try:
        client.auth.sign_out()
        st.session_state.user = None
    except:
        pass

def get_current_user():
    """Return user from session state, or try to recover from Supabase session."""
    if "user" in st.session_state and st.session_state.user is not None:
        return st.session_state.user

    # Try to get session from Supabase (persists across refresh)
    try:
        client = get_supabase()
        session = client.auth.get_session()
        if session and session.user:
            st.session_state.user = session.user
            return session.user
    except:
        pass
    return None
