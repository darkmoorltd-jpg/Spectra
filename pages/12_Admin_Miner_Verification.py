
import streamlit as st
from supabase import create_client
import base64
import os
import tempfile

st.set_page_config(page_title="Admin – Miner Verification", page_icon="🔐", layout="wide")

# Styling
st.markdown("""
<style>
    .stApp { background: radial-gradient(ellipse at 20% 50%, #0d1b2a 0%, #0a0e17 70%); color: #e0e0e0; }
    header, footer { visibility: hidden; }
    .title { font-size: 2.5rem; font-weight: 800; text-align: center; color: #ffd700; }
    .subtitle { text-align: center; color: #8892b0; margin-bottom: 2rem; }
    .verified-card { background: #111827; border: 1px solid #1f2a44; border-radius: 16px; padding: 1.5rem; margin: 1rem 0; }
    .pending { color: #f57f17; font-weight: 600; }
    .approved { color: #2e7d32; font-weight: 600; }
    .rejected { color: #c62828; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🔐 Miner Verification Admin</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Review, verify, and manage miner identity documents</div>', unsafe_allow_html=True)

# Admin check
ADMIN_EMAIL = "darkmoorltd@gmail.com"
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in as admin first.")
    st.stop()

if st.session_state.user.email != ADMIN_EMAIL:
    st.error("Access denied. Admin only.")
    st.stop()

# Supabase clients
url = st.secrets["supabase"]["url"]
service_key = st.secrets["supabase"]["service_key"]
service = create_client(url, service_key)

# Fetch all miner verifications
try:
    res = service.table("miner_verifications").select("*").order("created_at", desc=True).execute()
    verifications = res.data if res.data else []
except Exception as e:
    st.error(f"Failed to load verifications: {e}")
    verifications = []

if not verifications:
    st.info("No miner verification applications yet.")
    st.stop()

# Tabs for status filtering
pending = [v for v in verifications if v.get("status") == "pending"]
approved = [v for v in verifications if v.get("status") == "approved"]
rejected = [v for v in verifications if v.get("status") == "rejected"]

tab1, tab2, tab3 = st.tabs(["⏳ Pending", "✅ Approved", "❌ Rejected"])

def display_verification(v):
    """Display a verification card with documents."""
    with st.container():
        st.markdown('<div class="verified-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2,2,1])
        with col1:
            st.markdown(f"### 👤 {v.get('full_name', 'N/A')}")
            st.markdown(f"**Phone:** {v.get('phone', 'N/A')}")
            st.markdown(f"**Email:** {v.get('email', 'N/A')}")
            st.markdown(f"**State:** {v.get('state', 'N/A')} – **LGA:** {v.get('lga', 'N/A')}")
        with col2:
            st.markdown(f"**Mining Site:** {v.get('mining_site', 'N/A')}")
            st.markdown(f"**Minerals:** {v.get('minerals', 'N/A')}")
            st.markdown(f"**ID Type:** {v.get('id_type', 'N/A')}")
            st.markdown(f"**ID Number:** {v.get('id_number', 'N/A')}")
        with col3:
            status = v.get("status", "pending")
            st.markdown(f"**Status:** <span class='{status}'>{status.upper()}</span>", unsafe_allow_html=True)
            st.markdown(f"**Payment:** {v.get('payment_status', 'pending')}")
        
        st.markdown("---")
        st.markdown("### 🪪 ID Documents")
        
        doc_col1, doc_col2 = st.columns(2)
        with doc_col1:
            st.markdown("**ID Upload:**")
            id_url = v.get("id_upload_url") or v.get("id_url")
            if id_url:
                st.image(id_url, width=300)
            else:
                st.caption("No ID image URL found")
        
        with doc_col2:
            st.markdown("**Selfie with ID:**")
            selfie_url = v.get("selfie_upload_url") or v.get("selfie_url")
            if selfie_url:
                st.image(selfie_url, width=300)
            else:
                st.caption("No selfie URL found")
        
        st.markdown("</div>", unsafe_allow_html=True)
        return v.get("user_id")

# ----- Pending Tab -----
with tab1:
    if not pending:
        st.info("No pending verifications.")
    else:
        for v in pending:
            user_id = display_verification(v)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", key=f"approve_{v['id']}", use_container_width=True):
                    service.table("miner_verifications").update({"status": "approved"}).eq("id", v["id"]).execute()
                    # Also update user_profiles
                    service.table("user_profiles").update({"verification_status": "approved"}).eq("user_id", v["user_id"]).execute()
                    st.success("Miner approved!")
                    st.rerun()
            with col2:
                if st.button("❌ Reject", key=f"reject_{v['id']}", use_container_width=True):
                    service.table("miner_verifications").update({"status": "rejected"}).eq("id", v["id"]).execute()
                    service.table("user_profiles").update({"verification_status": "rejected"}).eq("user_id", v["user_id"]).execute()
                    st.error("Miner rejected.")
                    st.rerun()

# ----- Approved Tab -----
with tab2:
    if not approved:
        st.info("No approved miners.")
    else:
        for v in approved:
            display_verification(v)

# ----- Rejected Tab -----
with tab3:
    if not rejected:
        st.info("No rejected miners.")
    else:
        for v in rejected:
            display_verification(v)
            if st.button("🔄 Reopen", key=f"reopen_{v['id']}"):
                service.table("miner_verifications").update({"status": "pending"}).eq("id", v["id"]).execute()
                st.rerun()
