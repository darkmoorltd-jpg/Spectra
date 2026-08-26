from utils.sidebar import render_sidebar

import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.style import apply_global_style

st.set_page_config(page_title="Exploration Map", page_icon="🗺️", layout="wide")
render_sidebar()
apply_global_style()

st.markdown('<h2 style="text-align:center;">🗺️ Mineral Exploration Map</h2>', unsafe_allow_html=True)

# Default center: Nigeria
m = folium.Map(location=[9.0765, 7.3986], zoom_start=6)
# Add some marker for known mineral areas (demo)
folium.Marker([9.5, 7.5], popup="Gold potential", icon=folium.Icon(color="gold")).add_to(m)
folium.Marker([10.0, 8.0], popup="Cassiterite area", icon=folium.Icon(color="red")).add_to(m)
folium.Marker([8.5, 8.0], popup="Copper belt", icon=folium.Icon(color="blue")).add_to(m)

st_folium(m, width=800, height=500)
st.info("Full exploration recommendations based on your GPS and scan history coming soon.")