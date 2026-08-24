
import streamlit as st

def apply_global_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

    :root {
        --bg: #0a0e17;
        --surface: #111827;
        --border: #1f2a44;
        --gold: #ffd700;
        --copper: #b87333;
        --cyan: #00e5ff;
        --green: #00c853;
        --text: #e0e0e0;
        --dim: #8892b0;
        --glow-gold: 0 0 12px rgba(255,215,0,0.5);
        --glow-cyan: 0 0 12px rgba(0,229,255,0.5);
    }

    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
        background-color: var(--bg) !important;
        color: var(--text);
    }

    .stApp {
        background: radial-gradient(ellipse at 20% 50%, #0d1b2a 0%, #0a0e17 70%);
        background-size: cover;
        color: var(--text);
    }

    /* Hide Streamlit default header */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    footer {visibility: hidden;}

    /* ---- Typography ---- */
    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #ffd700 0%, #b8860b 40%, #ffd700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: var(--glow-gold);
        animation: pulse 2s infinite alternate;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        font-size: 1.4rem;
        color: var(--dim);
        letter-spacing: 2px;
        margin-top: -10px;
    }

    /* ---- Cards ---- */
    .scan-card {
        background: linear-gradient(145deg, #111827 0%, #0d1117 100%);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    .scan-card:hover {
        border-color: var(--cyan);
        box-shadow: 0 8px 32px rgba(0,229,255,0.2);
    }

    .metric-box {
        background: var(--surface);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        text-align: center;
        border: 1px solid var(--border);
    }
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--gold);
    }
    .metric-label {
        font-size: 0.85rem;
        color: var(--dim);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ---- Buttons ---- */
    .stButton > button {
        background: linear-gradient(135deg, #1f2a44, #111827);
        color: var(--gold);
        border: 1px solid var(--gold);
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: var(--gold);
        color: #0a0e17;
        box-shadow: 0 0 15px rgba(255,215,0,0.5);
        transform: translateY(-2px);
    }

    /* ---- Inputs ---- */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: #111827;
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 6px;
    }

    /* ---- File uploader ---- */
    .stFileUploader > div > div {
        background: #111827;
        border: 2px dashed var(--border);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s;
    }
    .stFileUploader > div > div:hover {
        border-color: var(--cyan);
        box-shadow: 0 0 20px rgba(0,229,255,0.3);
    }

    /* ---- Spinner ---- */
    .stSpinner > div {
        border-top-color: var(--gold) !important;
    }

    /* ---- Progress bar ---- */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ffd700, #ff8c00);
    }

    /* ---- Tabs ---- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--dim);
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #1f2a44;
        color: var(--gold) !important;
    }

    /* ---- Sidebar ---- */
    [data-testid="stSidebar"] {
        background: #0d1117;
        border-right: 1px solid var(--border);
    }

    /* ---- Animations ---- */
    @keyframes pulse {
        0% { text-shadow: 0 0 10px rgba(255,215,0,0.7); }
        100% { text-shadow: 0 0 25px rgba(255,215,0,1), 0 0 50px rgba(255,215,0,0.5); }
    }

    @keyframes scanline {
        0% { top: 0; }
        100% { top: 100%; }
    }

    .scan-line {
        position: absolute;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--cyan), transparent);
        animation: scanline 2s linear infinite;
    }

    .result-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }

    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #1f2a44, #111827);
        border: 1px solid var(--gold);
        border-radius: 50px;
        padding: 0.4rem 1rem;
        margin: 0.2rem;
        font-weight: 600;
        color: var(--gold);
    }

    /* Gauge (simple radial) */
    .gauge {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(var(--gold) 0deg, #1f2a44 0deg);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    .gauge-inner {
        width: 80px;
        height: 80px;
        background: #0d1117;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.5rem;
        color: var(--gold);
    }

    /* Count-up animation */
    .count-up {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--gold);
    }
    </style>
    """, unsafe_allow_html=True)

def metric_box(value, label):
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def badge(text):
    st.markdown(f'<span class="badge">{text}</span>', unsafe_allow_html=True)
