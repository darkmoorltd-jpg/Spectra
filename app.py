
import streamlit as st
from utils.style import apply_global_style, metric_box
from utils.sidebar import render_sidebar
from utils.constants import MINERALS
from utils.session import init_session

init_session()
st.set_page_config(page_title="SPECTRA", page_icon="⛏️", layout="wide")

# ============================================
# MINING COMMAND CENTER THEME
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #050B14;
    --surface: #0D1B2A;
    --border: #1F2A44;
    --gold: #FFD700;
    --cyan: #00E5FF;
    --green: #00C853;
    --red: #FF1744;
    --text: #E0E0E0;
    --dim: #8892B0;
}

.stApp {
    background: radial-gradient(ellipse at 20% 50%, #0D1B2A 0%, #050B14 70%);
    color: var(--text);
    font-family: 'Rajdhani', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}
footer {visibility: hidden;}

/* ============ HERO TITLE ============ */
.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #FFD700 0%, #FF8C00 50%, #FFD700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(255,215,0,0.5);
    margin-bottom: 0;
    letter-spacing: 3px;
}

.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: var(--cyan);
    letter-spacing: 5px;
    margin-top: -5px;
    font-weight: 600;
}

/* ============ STAT CARDS ============ */
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transition: all 0.3s;
}
.stat-card:hover {
    border-color: var(--cyan);
    box-shadow: 0 4px 30px rgba(0,229,255,0.2);
}
.stat-value {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--gold);
}
.stat-label {
    font-size: 0.8rem;
    color: var(--dim);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 4px;
}

/* ============ SCAN ZONE ============ */
.scan-zone {
    background: var(--surface);
    border: 2px dashed var(--border);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin: 1.5rem 0;
    position: relative;
    overflow: hidden;
}
.scan-zone:hover {
    border-color: var(--cyan);
    box-shadow: 0 0 40px rgba(0,229,255,0.3);
}
.scan-icon {
    font-size: 3rem;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

/* ============ TICKER ============ */
.ticker-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 0;
    margin: 10px 0;
    overflow: hidden;
}
.ticker {
    display: flex;
    animation: scroll 20s linear infinite;
    white-space: nowrap;
}
@keyframes scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.ticker-item {
    padding: 0 20px;
    font-weight: 600;
    letter-spacing: 1px;
}

/* ============ BUTTONS ============ */
.stButton > button {
    background: linear-gradient(135deg, #FFD700, #FF8C00);
    color: #050B14;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    letter-spacing: 1px;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 2rem;
    transition: all 0.3s;
}
.stButton > button:hover {
    box-shadow: 0 0 20px rgba(255,215,0,0.5);
    transform: translateY(-2px);
}

/* ============ SCAN ITEMS ============ */
.scan-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.scan-mineral {
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text);
}
.scan-value {
    color: var(--gold);
    font-weight: 700;
}
.scan-confidence {
    color: var(--green);
    font-size: 0.9rem;
}

/* ============ NAV LINKS ============ */
.nav-link {
    display: inline-block;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.8rem 1.5rem;
    margin: 0.3rem;
    text-align: center;
    color: var(--text);
    text-decoration: none;
    transition: all 0.3s;
    font-weight: 600;
    letter-spacing: 1px;
}
.nav-link:hover {
    border-color: var(--gold);
    color: var(--gold);
    box-shadow: 0 0 15px rgba(255,215,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# ============================================
# RENDER SIDEBAR
# ============================================
render_sidebar()

# ============================================
# HERO SECTION
# ============================================
st.markdown('<div class="hero-title">SPECTRA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">MINING COMMAND CENTER</div>', unsafe_allow_html=True)

# ============================================
# LIVE PRICE TICKER
# ============================================
st.markdown("""
<div class="ticker-wrap">
    <div class="ticker">
        <span class="ticker-item" style="color:#FFD700;">Gold: $65,000/kg</span>
        <span class="ticker-item" style="color:#B87333;">Copper: $8,500/ton</span>
        <span class="ticker-item" style="color:#00E5FF;">Quartz: $500/ton</span>
        <span class="ticker-item" style="color:#00C853;">Malachite: $20,000/ton</span>
        <span class="ticker-item" style="color:#FFD700;">Bornite: $15,000/ton</span>
        <span class="ticker-item" style="color:#FF1744;">Cassiterite: $18,000/ton</span>
        <span class="ticker-item" style="color:#FFD700;">Gold: $65,000/kg</span>
        <span class="ticker-item" style="color:#B87333;">Copper: $8,500/ton</span>
        <span class="ticker-item" style="color:#00E5FF;">Quartz: $500/ton</span>
        <span class="ticker-item" style="color:#00C853;">Malachite: $20,000/ton</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# STAT CARDS
# ============================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">30</div>
        <div class="stat-label">Scans Left</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">₦450k</div>
        <div class="stat-label">Value Found</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">97.2%</div>
        <div class="stat-label">Accuracy</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">7</div>
        <div class="stat-label">Minerals</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SCAN ZONE
# ============================================
st.markdown("""
<div class="scan-zone">
    <div class="scan-icon">🔍</div>
    <h3 style="color:#FFD700; margin:10px 0;">SCAN MINERAL</h3>
    <p style="color:#8892B0;">Upload a photo or use camera to identify your mineral</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("📤 Upload Photo", use_container_width=True):
        st.switch_page("pages/1_Scan_Mineral.py")
with col2:
    if st.button("📸 Use Camera", use_container_width=True):
        st.switch_page("pages/1_Scan_Mineral.py")

# ============================================
# RECENT SCANS
# ============================================
st.markdown("---")
st.markdown("### 📊 Recent Scans")

recent_scans = [
    {"mineral": "💎 Quartz", "confidence": "92%", "value": "₦12,500"},
    {"mineral": "🪙 Pyrite", "confidence": "88%", "value": "₦5,000"},
    {"mineral": "🟢 Malachite", "confidence": "85%", "value": "₦18,000"},
]

for scan in recent_scans:
    st.markdown(f"""
    <div class="scan-item">
        <span class="scan-mineral">{scan['mineral']}</span>
        <span class="scan-confidence">✓ {scan['confidence']}</span>
        <span class="scan-value">{scan['value']}</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# QUICK NAVIGATION
# ============================================
st.markdown("---")
st.markdown("### 🚀 Quick Access")

pages = [
    ("🔍 Scan Mineral", "pages/1_Scan_Mineral.py"),
    ("📊 My Vault", "pages/2_My_History.py"),
    ("💹 Market Prices", "pages/6_Market.py"),
    ("💳 Buy Scans", "pages/3_Buy_Scans.py"),
    ("👤 Profile", "pages/4_Profile.py"),
    ("📚 Mineralpedia", "pages/7_Mineralpedia.py"),
    ("🏆 Leaderboard", "pages/8_Leaderboard.py"),
    ("🔗 Referral", "pages/9_Referral.py"),
]

cols = st.columns(4)
for i, (label, page_path) in enumerate(pages):
    with cols[i % 4]:
        st.page_link(page_path, label=label, use_container_width=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#8892B0; padding:1rem;">
    ⛏️ SPECTRA v2.0 — Mining Command Center<br>
    Powered by Darkmoor Ltd
</div>
""", unsafe_allow_html=True)
