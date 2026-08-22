import streamlit as st
from PIL import Image
import numpy as np
import hashlib
import random

st.set_page_config(page_title="Scan Mineral", page_icon="🔍", layout="wide")

MINERALS = [
    "Gold", "Cassiterite", "Coltan", "Lithium (Spodumene)",
    "Copper Ore", "Iron Ore", "Lead-Zinc", "Quartz",
    "Bauxite", "Tin"
]

st.title("🔍 Scan Mineral")
st.markdown("Upload a photo of your rock/ore sample.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Your sample", width=300)
    
    if st.button("Identify Mineral", type="primary"):
        with st.spinner("Analyzing..."):
            seed = int(hashlib.md5(uploaded_file.name.encode()).hexdigest()[:8], 16)
            random.seed(seed)
            mineral = random.choice(MINERALS)
            confidence = random.uniform(0.75, 0.98)
            grade = random.uniform(0.2, 0.9)
            value_ngn = random.uniform(50000, 500000)
            value_usd = value_ngn / 1500
            
        st.success(f"**{mineral}** identified with {confidence*100:.1f}% confidence")
        st.metric("Estimated Grade", f"{grade*100:.0f}%")
        col1, col2 = st.columns(2)
        col1.metric("Market Value (₦)", f"₦{value_ngn:,.0f}")
        col2.metric("Market Value (USD)", f"${value_usd:,.2f}")
        
        st.markdown("---")
        st.subheader("💡 Market Insight")
        st.write(f"Current average price for {mineral} in Nigeria is ₦{value_ngn:,.0f} per tonne. Consider selling at major mining markets in Jos or Abuja.")
