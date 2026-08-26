
import streamlit as st
from supabase import create_client, Client

def get_supabase() -> Client:
    """Return Supabase client using anon key (for read operations when RLS applies)."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def get_service_client() -> Client:
    """Return service role client for admin/write operations."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["service_key"]
    return create_client(url, key)

def get_user_scans(user_id: str) -> int:
    """Fetch scans remaining for user (read is safe with anon if RLS allows)."""
    try:
        client = get_supabase()
        res = client.table("user_scans").select("scans_remaining").eq("user_id", user_id).execute()
        return res.data[0]["scans_remaining"] if res.data else 30
    except Exception:
        return 30

def deduct_scan(user_id: str, amount: int = 1) -> int:
    """Deduct scans and return new total. Uses service role to bypass RLS."""
    client = get_service_client()   # <-- use service for writes
    # Ensure row exists
    try:
        client.table("user_scans").insert({"user_id": user_id, "scans_remaining": 30}).execute()
    except:
        pass
    current = get_user_scans(user_id)
    new_total = max(0, current - amount)
    client.table("user_scans").update({"scans_remaining": new_total}).eq("user_id", user_id).execute()
    return new_total

def add_scans_to_user(user_id: str, amount: int) -> int:
    """Add scans to user account and return new total."""
    client = get_service_client()
    current = get_user_scans(user_id)
    new_total = current + amount
    client.table("user_scans").update({"scans_remaining": new_total}).eq("user_id", user_id).execute()
    return new_total

def save_payment_record(user_id: str, amount: float, scans_added: int, plan: str, reference: str):
    """Insert payment history row."""
    client = get_service_client()
    client.table("payment_history").insert({
        "user_id": user_id,
        "amount": amount,
        "scans_added": scans_added,
        "plan": plan,
        "reference": reference,
        "paid_at": "now()"
    }).execute()
