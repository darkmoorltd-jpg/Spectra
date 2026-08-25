
import streamlit as st
from supabase import create_client

def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def add_price_alert(user_id, mineral, target_price):
    client = get_supabase()
    try:
        client.table("price_alerts").insert({
            "user_id": user_id,
            "mineral": mineral,
            "target_price": target_price,
            "active": True
        }).execute()
        return True, None
    except Exception as e:
        return False, str(e)

def get_user_alerts(user_id):
    client = get_supabase()
    try:
        res = client.table("price_alerts").select("*").eq("user_id", user_id).eq("active", True).execute()
        return res.data if res.data else []
    except:
        return []
