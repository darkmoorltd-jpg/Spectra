
import streamlit as st
from supabase import create_client, Client

def get_supabase() -> Client:
    """Return Supabase client using anon key."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def get_service_client() -> Client:
    """Return service role client for admin/write operations."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["service_key"]
    return create_client(url, key)

def get_user_scans(user_id: str) -> int:
    """Fetch scans remaining for user."""
    try:
        client = get_service_client()
        res = client.table("user_scans").select("scans_remaining").eq("user_id", user_id).execute()
        if res.data and len(res.data) > 0:
            return res.data[0]["scans_remaining"]
        else:
            # Create default row if missing
            client.table("user_scans").insert({"user_id": user_id, "scans_remaining": 30, "plan": "free"}).execute()
            return 30
    except Exception as e:
        print(f"Error fetching scans: {e}")
        return 30

def deduct_scan(user_id: str, amount: int = 1) -> int:
    """Deduct scans and return new total."""
    client = get_service_client()
    try:
        current = get_user_scans(user_id)
        new_total = max(0, current - amount)
        client.table("user_scans").update({"scans_remaining": new_total}).eq("user_id", user_id).execute()
        return new_total
    except Exception as e:
        print(f"Error deducting scan: {e}")
        return 0

def add_scans_to_user(user_id: str, amount: int) -> int:
    """Add scans to user account and return new total."""
    client = get_service_client()
    try:
        current = get_user_scans(user_id)
        new_total = current + amount
        client.table("user_scans").update({"scans_remaining": new_total}).eq("user_id", user_id).execute()
        return new_total
    except Exception as e:
        print(f"Error adding scans: {e}")
        return 0

def save_scan_history(user_id: str, mineral: str, confidence: float, grade: float, value_ngn: float):
    """Insert a new scan record into scan_history."""
    client = get_service_client()
    try:
        client.table("scan_history").insert({
            "user_id": user_id,
            "mineral": mineral,
            "confidence": confidence,
            "grade": grade,
            "value_ngn": value_ngn,
            "created_at": "now()"
        }).execute()
        return True
    except Exception as e:
        print(f"Failed to save scan history: {e}")
        return False

def save_payment_record(user_id: str, amount: float, scans_added: int, plan: str, reference: str):
    """Insert payment history row."""
    client = get_service_client()
    try:
        client.table("payment_history").insert({
            "user_id": user_id,
            "amount": amount,
            "scans_added": scans_added,
            "plan": plan,
            "reference": reference,
            "paid_at": "now()"
        }).execute()
        return True
    except Exception as e:
        print(f"Failed to save payment: {e}")
        return False
