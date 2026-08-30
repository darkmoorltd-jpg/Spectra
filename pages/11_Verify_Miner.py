
import streamlit as st
from supabase import create_client, Client
import uuid
import requests as req
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
SERVICE_KEY = st.secrets["supabase"]["service_key"]
PAYSTACK_PUBLIC = "pk_live_3af5d245e74f86f0517d214b6872f4ac8236e057"
PAYSTACK_SECRET = st.secrets["paystack"]["secret_key"]


def normalize_phone(phone):
    """Convert Nigerian phone to international format."""
    if not phone:
        return "08000000000"
    phone = phone.strip().replace(" ", "").replace("-", "").replace("+", "")
    if phone.startswith("0"):
        return "234" + phone[1:]
    elif phone.startswith("234"):
        return phone
    else:
        return "234" + phone


@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


@st.cache_resource
def init_service():
    return create_client(SUPABASE_URL, SERVICE_KEY)


st.set_page_config(page_title="SPECTRA – Miner Verification", page_icon="⛏️", layout="wide")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in first.")
    st.stop()

user = st.session_state.user
supabase = init_supabase()
service = init_service()

# Fetch user phone
user_phone = ""
try:
    profile_res = service.table("user_profiles").select("phone").eq("user_id", user.id).execute()
    if profile_res.data and len(profile_res.data) > 0:
        user_phone = profile_res.data[0].get("phone", "") or ""
except:
    pass

phone_for_sms = normalize_phone(user_phone)

# Custom dark theme
st.markdown("""
<style>
    .stApp { background: radial-gradient(ellipse at 20% 50%, #0d1b2a 0%, #0a0e17 70%); color: #e0e0e0; }
    header, footer { visibility: hidden; }
    .title { font-size: 2.5rem; font-weight: 800; text-align: center; color: #ffd700; }
    .subtitle { text-align: center; color: #8892b0; margin-bottom: 2rem; }
    .card { background: #111827; border: 1px solid #1f2a44; border-radius: 16px; padding: 1.5rem; margin: 1rem 0; }
    .stButton > button { background: #ffd700; color: #0a0e17; font-weight: bold; border: none; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">⛏️ Miner Verification</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Verify your identity to unlock buyer matching, wallet, and official reports</div>', unsafe_allow_html=True)

# Check existing verification
try:
    existing = service.table("miner_verifications").select("*").eq("user_id", user.id).execute()
    if existing.data and len(existing.data) > 0:
        status = existing.data[0].get("status", "pending")
        if status == "approved":
            st.success("✅ You are already verified! All features are unlocked.")
            st.stop()
        elif status == "pending":
            st.info("⏳ Your verification is pending review. Please wait for admin approval.")
            st.stop()
except:
    pass

with st.form("miner_verification_form"):
    st.markdown("### 📋 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name *", placeholder="e.g., Ibrahim Musa")
        phone = st.text_input("Phone Number *", value=user_phone, placeholder="e.g., 08031234567")
        state = st.text_input("State *", placeholder="e.g., Nasarawa")
    with col2:
        lga = st.text_input("LGA", placeholder="e.g., Akwanga")
        mining_site = st.text_input("Mining Site/Location *", placeholder="e.g., Keffi mining area")
        minerals = st.text_input("Minerals of Interest", placeholder="e.g., Lithium, Coltan, Tin")

    st.markdown("---")
    st.markdown("### 🪪 ID Upload")
    col1, col2 = st.columns(2)
    with col1:
        id_type = st.selectbox("ID Type *", ["National ID Card", "Driver's License", "International Passport", "Voter's Card (PVC)", "NIN Slip"])
        id_number = st.text_input("ID Number *", placeholder="e.g., 12345678901")
    with col2:
        id_upload = st.file_uploader("Upload ID *", type=["jpg","jpeg","png","pdf"])
        selfie_upload = st.file_uploader("Upload Selfie with ID *", type=["jpg","jpeg","png"])

    st.markdown("---")
    st.markdown("### 💳 Verification Fee: ₦2,000")
    submit = st.form_submit_button("✅ Submit for Verification", type="primary", use_container_width=True)

if submit:
    if not full_name or not phone or not state or not mining_site or not id_upload or not selfie_upload:
        st.error("❌ Please fill all required fields and upload ID + selfie.")
    else:
        # Create verification record
        verification_ref = f"SPECTRA_VERIFY_{user.id[:8]}_{uuid.uuid4().hex[:8]}"
        service.table("miner_verifications").insert({
            "user_id": user.id,
            "full_name": full_name,
            "phone": phone,
            "state": state,
            "lga": lga,
            "mining_site": mining_site,
            "minerals": minerals,
            "payment_reference": verification_ref,
            "payment_status": "pending",
            "status": "pending",
        }).execute()

        # Paystack payment
        components_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://js.paystack.co/v1/inline.js"></script>
        </head>
        <body>
            <button onclick="payForVerification()" style="background:#ffd700;color:#0a0e17;border:none;padding:15px 40px;border-radius:10px;font-weight:700;cursor:pointer;">Pay ₦2,000 to Verify</button>
            <script>
                function payForVerification() {{
                    PaystackPop.setup({{
                        key: '{PAYSTACK_PUBLIC}',
                        email: '{user.email}',
                        phone: '{phone_for_sms}',
                        amount: 200000,
                        currency: 'NGN',
                        ref: '{verification_ref}',
                        label: 'SPECTRA Miner Verification',
                        onClose: function() {{ window.location.reload(); }},
                        callback: function(response) {{
                            window.location.href = '/~/callback?reference=' + response.reference + '&plan=verification';
                        }}
                    }}).openIframe();
                }}
            </script>
        </body>
        </html>
        """
        st.components.v1.html(components_html, height=120)
        st.info("👆 Click the gold button above to pay the verification fee.")
