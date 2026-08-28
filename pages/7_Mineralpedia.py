from utils.sidebar import render_sidebar

import streamlit as st
from utils.style import apply_global_style
from utils.constants import MINERALS
from utils.session import init_session

init_session()
st.set_page_config(page_title="Mineralpedia", page_icon="📚", layout="wide")
render_sidebar()
apply_global_style()

st.markdown('<h2 style="text-align:center;">📚 Mineralpedia</h2>', unsafe_allow_html=True)
st.markdown("Explore the minerals SPECTRA can identify.")

# Mineral data (simplified; can be expanded)
MINERAL_INFO = {
    "Biotite": {"hardness": "2.5-3", "streak": "White-gray", "color": "Dark brown/black", "use": "Industrial filler", "rarity": "Common"},
    "Bornite": {"hardness": "3-3.5", "streak": "Gray-black", "color": "Iridescent purple/blue", "use": "Copper ore", "rarity": "Uncommon"},
    "Chrysocolla": {"hardness": "2-4", "streak": "White-blue", "color": "Blue-green", "use": "Copper ore, gem", "rarity": "Uncommon"},
    "Malachite": {"hardness": "3.5-4", "streak": "Pale green", "color": "Bright green", "use": "Copper ore, gem", "rarity": "Uncommon"},
    "Muscovite": {"hardness": "2-2.5", "streak": "White", "color": "White/colorless", "use": "Insulator", "rarity": "Common"},
    "Pyrite": {"hardness": "6-6.5", "streak": "Green-black", "color": "Brassy yellow", "use": "Sulfur, gold path", "rarity": "Common"},
    "Quartz": {"hardness": "7", "streak": "White", "color": "Various", "use": "Glass, electronics", "rarity": "Very common"}
}

selected = st.selectbox("Choose a mineral", MINERALS)
if selected:
    info = MINERAL_INFO.get(selected, {})
    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown(f"### {selected}")
        st.markdown(f"**Hardness:** {info.get('hardness','N/A')}")
        st.markdown(f"**Streak:** {info.get('streak','N/A')}")
        st.markdown(f"**Color:** {info.get('color','N/A')}")
        st.markdown(f"**Rarity:** {info.get('rarity','N/A')}")
    with col2:
        st.markdown("### Use & Value")
        st.write(info.get("use","N/A"))
        # Dummy image
        st.image("https://via.placeholder.com/300x200.png?text="+selected, use_container_width=True)