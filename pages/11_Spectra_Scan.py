
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import time
import uuid
from utils.spectra_model_loader import load_model, predict, DISPLAY_NAMES, CLASS_NAMES
from utils.georoc_validator import GeoROCValidator

st.set_page_config(page_title="Spectra Scan", page_icon="⛏️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    .stApp { background: radial-gradient(ellipse at 50% 50%, #0d1b2a 0%, #050810 100%); color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    header, footer { visibility: hidden; }
    .title { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .subtitle { text-align: center; color: #8892b0; margin-bottom: 2rem; letter-spacing: 2px; }
    .result-card { background: #0d1117; border: 2px solid #1f2a44; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; }
    .result-known { border-left: 5px solid #00e5ff; }
    .result-unknown { border-left: 5px solid #ff1744; }
    .result-name { font-family: 'Orbitron', sans-serif; font-size: 2rem; font-weight: 700; color: #ffd700; }
    .result-confidence { font-size: 1.2rem; color: #8892b0; }
    .geo-match { background: #0a2a0a; border: 1px solid #00c853; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; }
    .geo-nomatch { background: #2a0a0a; border: 1px solid #ff1744; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">⛏️ SPECTRA SCAN</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Mineral Identification with Regional Validation</div>', unsafe_allow_html=True)

# ============================================
# LOAD MODEL (cached)
# ============================================
@st.cache_resource(show_spinner="🧠 Loading Spectra AI model...")
def get_model():
    return load_model()

@st.cache_resource(show_spinner="🌍 Connecting to GEOROC...")
def get_validator():
    return GeoROCValidator()

model, class_names, img_size = get_model()
validator = get_validator()

if model is None:
    st.error("❌ Could not load the Spectra AI model. Please try again later.")
    st.stop()

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("## ⛏️ Spectra")
    st.markdown("---")
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/1_Scan_Mineral.py", label="⛏️ Classic Scan")
    st.page_link("pages/11_Spectra_Scan.py", label="🔬 AI Scan (New)")
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    threshold = st.slider(
        "Confidence threshold",
        min_value=0.30, max_value=0.95, value=0.60, step=0.05,
        help="Below this → mineral is rejected as 'Unknown'"
    )
    use_georoc = st.checkbox("🌍 Use GEOROC regional validation", value=True)

# ============================================
# INPUT
# ============================================
st.markdown("### 📸 Upload a mineral photo")
tab1, tab2 = st.tabs(["Upload Photo", "Use Camera"])

image = None
with tab1:
    uploaded = st.file_uploader("Upload a clear photo", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded:
        image = Image.open(uploaded).convert("RGB")

with tab2:
    camera = st.camera_input("Take a photo", label_visibility="collapsed")
    if camera:
        image = Image.open(camera).convert("RGB")

# Location input
st.markdown("### 📍 Mining Location (optional)")
col1, col2 = st.columns(2)
with col1:
    lat = st.number_input("Latitude", value=9.0765, format="%.4f", step=0.001, help="GPS latitude")
with col2:
    lon = st.number_input("Longitude", value=7.3986, format="%.4f", step=0.001, help="GPS longitude")

# ============================================
# PREDICT
# ============================================
if image is not None:
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(image, caption="Your sample", use_container_width=True)

    with col2:
        if st.button("🔍 Identify Mineral", type="primary", use_container_width=True):
            with st.spinner("🧠 Analyzing..."):
                time.sleep(1)  # brief scan animation
                result = predict(model, class_names, img_size, image, confidence_threshold=threshold)

            # ---------- RESULT CARD ----------
            if result["is_unknown"]:
                st.markdown(f"""
                <div class="result-card result-unknown">
                    <div class="result-name" style="color:#ff1744;">❓ {result['display_name']}</div>
                    <div class="result-confidence">
                        Top guess: <strong>{result['top_3'][0][0].title()}</strong> 
                        (confidence: {result['top_3'][0][1]*100:.1f}% — below threshold {threshold*100:.0f}%)
                    </div>
                    <p style="color:#ff5252;margin-top:1rem;">
                        ⚠️ This mineral is not confidently recognized. It may be:
                    </p>
                    <ul style="color:#8892b0;">
                        <li>A mineral outside our 7 supported classes</li>
                        <li>Poorly lit or blurry photo</li>
                        <li>A mix of multiple minerals</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                # Save unknown scan info
                scan_id = str(uuid.uuid4())[:8]
                st.info(f"💡 Tip: Try a clearer photo with better lighting. Scan ID: `{scan_id}`")
            else:
                st.markdown(f"""
                <div class="result-card result-known">
                    <div class="result-name">💎 {result['display_name']}</div>
                    <div class="result-confidence">
                        Confidence: <strong>{result['confidence']*100:.1f}%</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Confidence gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result["confidence"] * 100,
                    domain={"x": [0, 1], "y": [0, 1]},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#8892b0"},
                        "bar": {"color": "#ffd700"},
                        "bgcolor": "#111827",
                        "borderwidth": 2,
                        "bordercolor": "#1f2a44",
                        "steps": [
                            {"range": [0, threshold*100], "color": "#2a0a0a"},
                            {"range": [threshold*100, 100], "color": "#0a2a0a"},
                        ],
                        "threshold": {
                            "line": {"color": "#ff1744", "width": 4},
                            "thickness": 0.75,
                            "value": threshold * 100,
                        }
                    }
                ))
                fig.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", font_color="#e0e0e0")
                st.plotly_chart(fig, use_container_width=True)

                # ---------- TOP 3 PREDICTIONS ----------
                st.markdown("### 📊 Top 3 Predictions")
                for mineral, prob in result["top_3"]:
                    st.write(f"**{DISPLAY_NAMES.get(mineral, mineral)}**: {prob*100:.1f}%")
                    st.progress(float(prob))

                # ---------- GEOROC VALIDATION ----------
                if use_georoc:
                    st.markdown("---")
                    st.markdown("### 🌍 Regional Validation (GEOROC)")
                    with st.spinner("Checking African geochemistry database..."):
                        geo = validator.validate_prediction(result["mineral"], lat, lon, radius_km=150)

                    if geo["region_match"] is True:
                        st.markdown(f"""
                        <div class="geo-match">
                            <strong>✅ Region Match</strong><br>
                            {geo['message']}<br>
                            <small>Found {geo['found_samples']} nearby samples. Matching rock types: {', '.join(geo['matching_rocks'])}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    elif geo["region_match"] is False:
                        st.markdown(f"""
                        <div class="geo-nomatch">
                            <strong>⚠️ Unusual for this Region</strong><br>
                            {geo['message']}<br>
                            <small>Expected rocks: {', '.join(geo['expected_rocks'][:5])}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info(geo["message"])
                else:
                    st.caption("🌍 GEOROC validation disabled in sidebar")

                # ---------- NEXT STEPS ----------
                st.markdown("---")
                st.markdown("### 🚀 Next Steps")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button("📄 Save to Vault", use_container_width=True):
                        st.success("✅ Saved (demo)")
                with col_b:
                    if st.button("💰 Get Market Value", use_container_width=True):
                        st.info("Coming soon: Naira price per grade")
                with col_c:
                    if st.button("🔊 Voice Explanation", use_container_width=True):
                        st.info("Coming soon: Spoken results in local languages")
else:
    st.info("👆 Upload a photo or use the camera to start scanning.")
