from utils.sidebar import render_sidebar

import streamlit as st
from utils.style import apply_global_style
from utils.buyer_matching import get_buyers_for_mineral
from utils.constants import MINERALS

st.set_page_config(page_title="Find Buyers", page_icon="🤝", layout="wide")
render_sidebar()
apply_global_style()

st.markdown('<h2 style="text-align:center;">🤝 Smart Buyer Matching</h2>', unsafe_allow_html=True)

mineral = st.selectbox("Mineral", MINERALS)
location = st.text_input("State (optional)", "")

if st.button("Find Buyers"):
    buyers = get_buyers_for_mineral(mineral, location if location else None)
    if buyers:
        st.markdown("### Top Buyers")
        for buyer in buyers:
            st.markdown(f"""
            <div class="scan-card">
                <h3>{buyer.get('name','Unknown')}</h3>
                <p>Phone: {buyer.get('phone','N/A')}</p>
                <p>Offer: {buyer.get('price_offer','N/A')}</p>
                <p>Rating: {buyer.get('rating','N/A')} ⭐</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No buyers found for this mineral yet. Try another mineral.")