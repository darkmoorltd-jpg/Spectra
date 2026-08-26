from utils.sidebar import render_sidebar

import streamlit as st
from utils.style import apply_global_style
from utils.constants import MINERALS, MINERAL_PRICES

st.set_page_config(page_title="Profit Simulator", page_icon="💰", layout="wide")
render_sidebar()
apply_global_style()

st.markdown('<h2 style="text-align:center;">💰 Mining Profit Simulator</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    mineral = st.selectbox("Mineral", MINERALS)
    weight_kg = st.number_input("Ore weight (kg)", min_value=1.0, value=100.0)
    grade = st.slider("Estimated grade (%)", 0, 100, 50) / 100
    price = MINERAL_PRICES.get(mineral, 1.0)
    gross_revenue = price * grade * weight_kg
    st.metric("Gross Revenue (USD)", f"${gross_revenue:,.2f}")
with col2:
    mining_cost = st.number_input("Mining cost (USD)", min_value=0.0, value=10.0)
    transport_cost = st.number_input("Transport cost (USD)", min_value=0.0, value=5.0)
    license_cost = st.number_input("License/other (USD)", min_value=0.0, value=2.0)
    total_cost = mining_cost + transport_cost + license_cost
    net_profit = gross_revenue - total_cost
    st.metric("Net Profit (USD)", f"${net_profit:,.2f}")
    st.metric("Break-even Grade", f"{total_cost / (price * weight_kg) * 100:.1f}%")

if net_profit > 0:
    st.success("This operation is profitable.")
else:
    st.error("Loss detected. Adjust grade or reduce costs.")