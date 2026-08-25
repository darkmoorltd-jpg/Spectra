
import streamlit as st
import pandas as pd
from PIL import Image
import random
from utils.style import apply_global_style
from utils.constants import MINERALS

st.set_page_config(page_title="Compare Scans", page_icon="📈", layout="wide")
apply_global_style()

st.markdown('<h2 style="text-align:center;">📈 Multi‑Scan Comparison</h2>', unsafe_allow_html=True)

uploads = st.file_uploader("Upload up to 5 mineral photos", type=["jpg","jpeg","png"], accept_multiple_files=True)

if uploads:
    results = []
    for i, file in enumerate(uploads[:5]):
        mineral = random.choice(MINERALS)
        confidence = random.uniform(0.7, 0.98)
        grade = random.uniform(0.2, 0.9)
        value = random.uniform(1000, 10000)
        results.append({
            "Photo": file.name,
            "Mineral": mineral,
            "Confidence": f"{confidence*100:.1f}%",
            "Grade": f"{grade*100:.0f}%",
            "Value (₦)": f"₦{value:,.0f}"
        })
    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)
    # Rank by value (sort)
    df_sorted = df.sort_values("Value (₦)", ascending=False)
    st.markdown("### Ranked by Value")
    st.dataframe(df_sorted, use_container_width=True)
