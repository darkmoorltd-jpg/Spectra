
import streamlit as st
from utils.style import apply_global_style

st.set_page_config(page_title="Mining License Guide", page_icon="📜", layout="wide")
apply_global_style()

st.markdown('<h2 style="text-align:center;">📜 Mining License & Permit Guide</h2>', unsafe_allow_html=True)

state = st.selectbox("Select State", ["Kaduna", "Kano", "Jos", "Nasarawa", "Zamfara", "Others"])
mineral = st.selectbox("Mineral", ["Gold", "Cassiterite", "Coltan", "Lithium", "Copper", "Quartz", "Others"])

st.markdown("### Steps to Get License")
steps = [
    "1. Register your mining cooperative or company with CAC.",
    "2. Obtain a Certificate of Occupancy for the land (if applicable).",
    "3. Apply for a Small Scale Mining Lease (SSML) from the Mining Cadastre Office (MCO).",
    "4. Submit environmental impact assessment (EIA) or environmental management plan (EMP).",
    "5. Pay the prescribed fees and wait for approval.",
]
for step in steps:
    st.write(step)

st.info("Always consult the Ministry of Mines and Steel Development for exact requirements.")
