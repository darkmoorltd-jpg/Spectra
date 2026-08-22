
import streamlit as st
from supabase import create_client, Client

def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def sign_up(email, password, first_name="", last_name=""):
    """Create a new user and initialize scans."""
    client = get_supabase()
    try:
        res = client.auth.sign_up({"email": email, "password": password})
        if res.user:
            # Insert default scan row and profile
            client.table("user_scans").insert({
                "user_id": res.user.id,
                "scans_remaining": 30,
                "plan": "free"
            }).execute()
            client.table("user_profiles").insert({
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
    """Return user from session state or None."""
    return st.session_state.get("user", None)
