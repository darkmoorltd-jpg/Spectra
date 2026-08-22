
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
        with st.spinner("Analyzing..."):
            model = load_mineral_model()  # placeholder, returns None
            mineral, confidence, grade = predict_mineral(model, image)
            value_ngn = random.uniform(50000, 500000)  # placeholder, replace with real valuation
            value_usd = value_ngn / 1500

        st.success(f"**{mineral}** identified with {confidence*100:.1f}% confidence")
        st.metric("Estimated Grade", f"{grade*100:.0f}%")
        col1, col2 = st.columns(2)
        col1.metric("Market Value (₦)", f"₦{value_ngn:,.0f}")
        col2.metric("Market Value (USD)", f"${value_usd:,.2f}")

        # Market insight
        st.markdown("---")
        st.subheader("💡 Market Insight")
        insight = get_market_insight(mineral, grade, value_ngn)
        st.write(insight)

        # Deduct scan (if user logged in)
        if "user" in st.session_state and st.session_state.user is not None:
            new_total = deduct_scan(st.session_state.user.id)
            st.caption(f"Scan deducted. Remaining scans: {new_total}")
        else:
            st.caption("Note: Login to save your scans and get full reports.")
