
import streamlit as st
import pandas as pd
from utils.style import apply_global_style

st.set_page_config(page_title="Leaderboard", page_icon="🏆", layout="wide")
apply_global_style()

st.markdown('<h2 style="text-align:center;">🏆 Top Miners This Week</h2>', unsafe_allow_html=True)

# Dummy data (replace with real query)
data = {
    "Rank": [1,2,3,4,5],
    "Miner": ["Ibrahim M.", "Aisha B.", "David O.", "Fatima Y.", "John T."],
    "Scans": [250, 210, 180, 150, 120],
    "Value Found": ["₦5M", "₦4M", "₦3.5M", "₦2M", "₦1.8M"]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

st.info("Leaderboard updates every hour. Scan more to climb the ranks!")
