
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.style import apply_global_style
from utils.constants import MINERALS, MINERAL_PRICES

st.set_page_config(page_title="Market Prices", page_icon="💹", layout="wide")
apply_global_style()

st.markdown('<h2 style="text-align:center;">💹 Mineral Market</h2>', unsafe_allow_html=True)

# Price ticker
st.markdown("### Live Prices (USD/kg)")
price_df = pd.DataFrame(list(MINERAL_PRICES.items()), columns=["Mineral", "Price"])
st.dataframe(price_df, use_container_width=True)

# Price chart
fig = px.bar(price_df, x="Mineral", y="Price", color="Mineral",
             title="Current Market Prices",
             template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Miner's Calculator
st.markdown("---")
st.subheader("🧮 Miner's Calculator")
col1, col2 = st.columns(2)
with col1:
    mineral = st.selectbox("Mineral", MINERALS)
    weight_kg = st.number_input("Weight (kg)", min_value=0.1, value=1.0)
with col2:
    grade = st.slider("Estimated Grade (%)", 0, 100, 50) / 100
    price = MINERAL_PRICES.get(mineral, 1.0)
    total_usd = price * grade * weight_kg
    st.metric("Total Value (USD)", f"${total_usd:,.2f}")
    st.metric("Total Value (₦)", f"₦{total_usd*1500:,.0f}")
