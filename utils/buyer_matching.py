
import streamlit as st
from supabase import create_client

def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def get_buyers_for_mineral(mineral, location=None, limit=3):
    """Fetch top matching buyers from Supabase 'mineral_buyers' table."""
    client = get_supabase()
    try:
        query = client.table("mineral_buyers").select("*").eq("mineral", mineral)
        if location:
            query = query.eq("state", location)
        res = query.limit(limit).execute()
        if res.data:
            return res.data
        # fallback to dummy if table missing
        return [
            {"name": "Local Trader A", "phone": "+2348012345678", "price_offer": "₦450,000/ton", "rating": 4.5},
            {"name": "Jos Minerals Ltd", "phone": "+2348055555555", "price_offer": "₦480,000/ton", "rating": 4.8},
            {"name": "Kano Export Co.", "phone": "+2348099999999", "price_offer": "₦420,000/ton", "rating": 4.2}
        ]
    except:
        return []
