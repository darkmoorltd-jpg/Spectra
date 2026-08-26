from utils.sidebar import render_sidebar

import streamlit as st
from utils.auth import get_current_user
from utils.paystack import verify_payment
from utils.supabase_client import add_scans_to_user, save_payment_record

st.set_page_config(page_title="Payment Verification", page_icon="⏳", layout="centered")
render_sidebar()

st.title("⏳ Processing your payment...")

# Get query params
query_params = st.query_params
reference = query_params.get("reference", [None])[0]
plan = query_params.get("plan", [None])[0]

user = get_current_user()
if user is None:
    st.error("Please log in to complete payment.")
    st.stop()

if not reference or not plan:
    st.error("Invalid payment link. Missing reference or plan.")
    st.stop()

PLAN_SCANS = {"10": 10, "25": 25, "60": 60, "unlimited": 9999}
if plan not in PLAN_SCANS:
    st.error("Unknown plan.")
    st.stop()

# Verify the transaction
with st.spinner("Verifying payment..."):
    success, amount_paid, err = verify_payment(reference)

if success:
    scans_to_add = PLAN_SCANS[plan]
    # Update user scans
    new_total = add_scans_to_user(user.id, scans_to_add)
    # Save payment history
    save_payment_record(user.id, amount_paid, scans_to_add, plan, reference)
    st.success(f"✅ Payment successful! {scans_to_add} scans added. Your new balance is {new_total} scans.")
    st.markdown("[Go to Scan Mineral](/Scan_Mineral)")
else:
    st.error(f"Payment verification failed: {err}")
    st.markdown("[Try again](/Buy_Scans)")