
import streamlit as st
import pandas as pd
from utils.style import apply_global_style
from utils.sidebar import render_sidebar
from utils.auth import get_current_user
from supabase import create_client

st.set_page_config(page_title="My Vault", page_icon="📊", layout="wide")
apply_global_style()
render_sidebar()

st.markdown('<h2 style="text-align:center;">💎 My Vault</h2>', unsafe_allow_html=True)

user = get_current_user()
if user is None:
    st.warning("Please log in to view your history.")
else:
    # Use service role to query scan_history
    url = st.secrets["supabase"]["url"]
    service_key = st.secrets["supabase"]["service_key"]
    service = create_client(url, service_key)

    try:
        res = service.table("scan_history") \
            .select("id, mineral, confidence, grade, value_ngn, created_at") \
            .eq("user_id", user.id) \
            .order("created_at", desc=True) \
            .limit(100) \
            .execute()
        if res.data:
            df = pd.DataFrame(res.data)
            # Format columns
            df["confidence"] = df["confidence"].apply(lambda x: f"{x*100:.1f}%")
            df["grade"] = df["grade"].apply(lambda x: f"{x*100:.0f}%" if x is not None else "N/A")
            df["value_ngn"] = df["value_ngn"].apply(lambda x: f"₦{x:,.0f}" if x is not None else "N/A")
            df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
            df = df[["created_at", "mineral", "confidence", "grade", "value_ngn"]]
            df.columns = ["Date", "Mineral", "Confidence", "Grade", "Value"]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No scans yet. Go to Scan Mineral to start your collection.")
    except Exception as e:
        st.error(f"Failed to load history: {e}")
