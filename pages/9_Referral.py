
import streamlit as st
from utils.style import apply_global_style
from utils.auth import get_current_user

st.set_page_config(page_title="Referral", page_icon="🔗", layout="wide")
apply_global_style()

st.markdown('<h2 style="text-align:center;">🔗 Referral Program</h2>', unsafe_allow_html=True)

user = get_current_user()
if user is None:
    st.warning("Please login to get your referral link.")
else:
    ref_code = user.id[:8].upper()  # simple code from user ID
    ref_link = f"https://spectragpt.streamlit.app/?ref={ref_code}"
    st.success(f"Your referral link: {ref_link}")
    st.markdown("Share this link with friends. When they sign up and scan, you both get 5 free scans!")
    st.markdown(f'<a href="https://wa.me/?text=Join%20SPECTRA%20and%20get%20free%20mineral%20scans!%20Use%20my%20link:%20{ref_link}" target="_blank"><button>Share on WhatsApp</button></a>', unsafe_allow_html=True)
