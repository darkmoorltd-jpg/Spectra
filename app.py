
import streamlit as st
from utils.style import apply_global_style, metric_box
from utils.sidebar import render_sidebar
from utils.constants import MINERALS
from utils.gamification import update_streak, get_leaderboard
from utils.session import init_session

init_session()
st.set_page_config(page_title="SPECTRA", page_icon="⛏️", layout="wide")
render_sidebar()  # This shows the full login/signup in sidebar

# Custom skin selection (persist in session)
if "skin" not in st.session_state:
    st.session_state.skin = "Obsidian"   # default

# Apply selected skin colors via CSS
skin_colors = {
    "Obsidian": {"bg": "#0a0e17", "accent": "#ffd700"},
    "Gold Rush": {"bg": "#1a0f00", "accent": "#ffaa00"},
    "Copper Vein": {"bg": "#1a0a00", "accent": "#b87333"},
    "Neon Prospector": {"bg": "#000000", "accent": "#00ffcc"}
}
c = skin_colors[st.session_state.skin]
st.markdown(f"""
<style>
:root {{
    --bg: {c['bg']};
    --gold: {c['accent']};
    --cyan: #00e5ff;
}}
.stApp {{
    background: radial-gradient(ellipse at 20% 50%, {c['bg']}, #000000);
}}
.hero-title {{
    background: linear-gradient(135deg, {c['accent']}, #ffffff, {c['accent']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 12px {c['accent']};
}}
</style>
""", unsafe_allow_html=True)

apply_global_style()

# Initialize user
if "user" not in st.session_state:
    st.session_state.user = None

# Hero Section
st.markdown('<div class="hero-title">SPECTRA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">GEOLOGIST IN YOUR POCKET</div>', unsafe_allow_html=True)

# Live Price Ticker
st.markdown("""
<div class="ticker-wrap" style="background:#111827; border:1px solid #1f2a44; border-radius:8px; padding:10px 0; margin:10px 0; overflow:hidden;">
    <div class="ticker" style="display:flex; animation: scroll 15s linear infinite; white-space:nowrap;">
        <span style="padding:0 20px; color:#ffd700;">Gold: $65,000/kg</span>
        <span style="padding:0 20px; color:#b87333;">Copper: $8,500/ton</span>
        <span style="padding:0 20px; color:#00e5ff;">Quartz: $500/ton</span>
        <span style="padding:0 20px; color:#00c853;">Malachite: $20,000/ton</span>
        <span style="padding:0 20px; color:#ffd700;">Bornite: $15,000/ton</span>
    </div>
</div>
<style>
@keyframes scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
</style>
""", unsafe_allow_html=True)

# Quick Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_box(f"{len(MINERALS)}+", "Minerals Recognized")
with col2:
    metric_box("₦300", "Per Scan")
with col3:
    metric_box("24/7", "Offline Ready")
with col4:
    metric_box("NGN/USD", "Live Prices")

# Show streak if logged in
if user:
    streak = update_streak(user.id)
    st.markdown(f"🔥 Streak: **{streak} days**")

st.markdown("---")
st.subheader("🚀 Quick Access")
# Grid of buttons
pages = [
    ("1_Scan_Mineral", "🔍 Scan Mineral"),
    ("2_My_History", "📊 My Vault"),
    ("6_Market", "💹 Market Prices"),
    ("3_Buy_Scans", "💳 Buy Scans"),
    ("4_Profile", "👤 Profile"),
    ("7_Mineralpedia", "📚 Mineralpedia"),
    ("8_Leaderboard", "🏆 Leaderboard"),
    ("9_Referral", "🔗 Referral"),
    ("10_Profit_Simulator", "💰 Profit Simulator"),
    ("11_Buyer_Matching", "🤝 Find Buyers"),
    ("12_Price_Alerts", "🔔 Price Alerts"),
    ("13_Multi_Scan_Compare", "📈 Compare Scans"),
    ("14_Exploration_Map", "🗺️ Exploration Map"),
    ("15_Find_of_the_Day", "⭐ Find of the Day"),
    ("16_Mining_License", "📜 Mining License Guide"),
    ("17_Real_Time_Video", "🎥 Real-Time Video"),
    ("18_Sound_Analysis", "🔊 Sound Scratch Test")
]
cols = st.columns(3)
for i, (page, label) in enumerate(pages):
    with cols[i % 3]:
        st.page_link(f"pages/{page}.py", label=label, use_container_width=True)

# Gamification Preview
st.markdown("---")
st.subheader("🏆 Your Achievements")
if user:
    st.markdown('<span class="badge">🔬 First Scan</span>', unsafe_allow_html=True)
    st.markdown('<span class="badge">🥇 Gold Hunter</span>', unsafe_allow_html=True)
else:
    st.info("Login to start earning badges.")

st.markdown("---")
st.caption("Powered by Darkmoor Ltd")