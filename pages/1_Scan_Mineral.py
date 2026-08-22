
import streamlit as st
from PIL import Image
import numpy as np
import hashlib
import random
from utils.model_loader import load_mineral_model, predict_mineral
from utils.deepseek import get_market_insight
from utils.supabase_client import deduct_scan

st.set_page_config(page_title="Scan Mineral", page_icon="🔍", layout="wide")

st.title("🔍 Scan Mineral")
st.markdown("Upload a photo of your rock/ore sample.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Your sample", width=300)

    if st.button("Identify Mineral", type="primary"):
        # Check if user is logged in
        user = st.session_state.get("user", None)
        if user is None:
            st.warning("Please log in to scan. Your first scan is free, but you need an account.")
            # Still allow demo scan but don't deduct
            with st.spinner("Analyzing (demo mode)..."):
                model = load_mineral_model()
                mineral, confidence, grade = predict_mineral(model, image)
                value_ngn = random.uniform(50000, 500000)
                value_usd = value_ngn / 1500
            st.success(f"**{mineral}** identified with {confidence*100:.1f}% confidence")
            st.metric("Estimated Grade", f"{grade*100:.0f}%")
            col1, col2 = st.columns(2)
            col1.metric("Market Value (₦)", f"₦{value_ngn:,.0f}")
            col2.metric("Market Value (USD)", f"${value_usd:,.2f}")
            st.info("Create an account to save scans and get full features.")
        else:
            # Deduct scan before running inference
            new_total = deduct_scan(user.id)
            if new_total < 0:
                st.error("Not enough scans. Please buy more.")
                st.stop()
            with st.spinner("Analyzing..."):
                model = load_mineral_model()
                mineral, confidence, grade = predict_mineral(model, image)
                value_ngn = random.uniform(50000, 500000)
                value_usd = value_ngn / 1500
            st.success(f"**{mineral}** identified with {confidence*100:.1f}% confidence")
            st.metric("Estimated Grade", f"{grade*100:.0f}%")
            col1, col2 = st.columns(2)
            col1.metric("Market Value (₦)", f"₦{value_ngn:,.0f}")
            col2.metric("Market Value (USD)", f"${value_usd:,.2f}")
            st.markdown("---")
            st.subheader("💡 Market Insight")
            insight = get_market_insight(mineral, grade, value_ngn)
            st.write(insight)
            st.caption(f"Scan deducted. Remaining scans: {new_total}")
