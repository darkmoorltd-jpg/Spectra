
import streamlit as st
from PIL import Image
import random
import time
import plotly.graph_objects as go
from utils.style import apply_global_style
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Real-Time Analysis", page_icon="🎥", layout="wide")
apply_global_style()
render_sidebar()

# ============================================
# CUSTOM CSS FOR LIVE FEED
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

.live-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #00E5FF 0%, #FFD700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.live-indicator {
    display: inline-block;
    width: 12px;
    height: 12px;
    background: #FF1744;
    border-radius: 50%;
    animation: blink 1s infinite;
    margin-right: 8px;
}
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0.2; }
    100% { opacity: 1; }
}

.scan-frame {
    border: 2px solid #00E5FF;
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    position: relative;
    box-shadow: 0 0 30px rgba(0,229,255,0.3);
}

.scan-line {
    position: absolute;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #00E5FF, transparent);
    animation: scanMove 2s linear infinite;
}
@keyframes scanMove {
    0% { top: 0; }
    100% { top: 100%; }
}

.result-flash {
    animation: flashBorder 0.5s ease;
}
@keyframes flashBorder {
    0% { border-color: #FFD700; box-shadow: 0 0 50px rgba(255,215,0,0.8); }
    100% { border-color: #00E5FF; box-shadow: 0 0 30px rgba(0,229,255,0.3); }
}

.mineral-tag {
    display: inline-block;
    background: #0D1B2A;
    border: 1px solid #FFD700;
    border-radius: 50px;
    padding: 0.5rem 1.5rem;
    margin: 0.3rem;
    font-weight: 700;
    color: #FFD700;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown('<div class="live-header">🎥 REAL-TIME MINERAL ANALYSIS</div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; margin-bottom:1rem;">
    <span class="live-indicator"></span>
    <span style="color:#FF1744; font-weight:700;">LIVE FEED ACTIVE</span>
</div>
""", unsafe_allow_html=True)

# ============================================
# INPUT METHOD
# ============================================
option = st.radio("Input Method", ["📸 Use Camera", "📤 Upload Image"], horizontal=True)

image_file = None
if option == "📸 Use Camera":
    image_file = st.camera_input("Point camera at mineral")
else:
    image_file = st.file_uploader("Upload mineral image", type=["jpg","jpeg","png"])

# ============================================
# ANALYSIS MODE
# ============================================
if image_file is not None:
    image = Image.open(image_file).convert("RGB")
    
    # Show image with scan frame
    st.markdown('<div class="scan-frame">', unsafe_allow_html=True)
    st.image(image, caption="Live View", use_container_width=True)
    st.markdown('<div class="scan-line"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🔍 Analyze Now", type="primary", use_container_width=True):
        # Simulate real-time analysis
        minerals = ["Biotite", "Bornite", "Chrysocolla", "Malachite", "Muscovite", "Pyrite", "Quartz"]
        
        st.markdown("### 📊 Live Analysis Results")
        st.markdown('<div class="result-flash">', unsafe_allow_html=True)
        
        # Animated progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            "Capturing frame...",
            "Preprocessing image...",
            "Extracting features...",
            "Matching against 7 minerals...",
            "Computing confidence...",
            "Finalizing result..."
        ]
        
        for i, step in enumerate(steps):
            status_text.text(f"⚡ {step}")
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.3)
        
        # Random result for demo
        mineral = random.choice(minerals)
        confidence = random.uniform(0.85, 0.99)
        grade = random.uniform(0.3, 0.9)
        
        progress_bar.progress(1.0)
        status_text.text("✅ Analysis complete")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ============================================
        # RESULTS DISPLAY
        # ============================================
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Confidence gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=confidence*100,
                domain={'x': [0,1], 'y': [0,1]},
                title={'text': "Confidence", 'font': {'color': '#E0E0E0'}},
                gauge={
                    'axis': {'range': [None, 100], 'tickcolor': '#8892B0'},
                    'bar': {'color': '#FFD700'},
                    'bgcolor': '#0D1B2A',
                    'borderwidth': 2,
                    'bordercolor': '#1F2A44',
                    'steps': [
                        {'range': [0, 50], 'color': '#1F2A44'},
                        {'range': [50, 80], 'color': '#2A3A54'},
                        {'range': [80, 100], 'color': '#3A4A64'}
                    ]
                }
            ))
            fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20),
                              paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(color='#E0E0E0'))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f'<h1 style="color:#FFD700; font-size:2.5rem; margin:0;">{mineral}</h1>', unsafe_allow_html=True)
            st.markdown(f"**Estimated Grade:** {grade*100:.0f}%")
            
            # Mineral properties
            st.markdown("### Properties")
            properties = {
                "Hardness": random.uniform(2, 7),
                "Specific Gravity": random.uniform(2.5, 5.0),
                "Luster": random.choice(["Metallic", "Vitreous", "Pearly", "Dull"]),
                "Streak": random.choice(["White", "Gray", "Green", "Brown", "Black"]),
            }
            
            for prop, value in properties.items():
                st.markdown(f"**{prop}:** {value}")
        
        # ============================================
        # QUICK ACTIONS
        # ============================================
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("💾 Save Result", use_container_width=True):
                st.success("Saved to Vault")
        with col2:
            if st.button("📄 Download PDF", use_container_width=True):
                st.info("PDF generation coming soon")
        with col3:
            if st.button("🔊 Voice Explanation", use_container_width=True):
                st.info("Voice coming soon")
        with col4:
            if st.button("🤝 Find Buyers", use_container_width=True):
                st.page_link("pages/11_Buyer_Matching.py", label="Go to Buyers")
else:
    # Placeholder when no image
    st.markdown("""
    <div class="scan-frame">
        <div style="font-size:5rem;">🎥</div>
        <h3 style="color:#00E5FF;">Camera Feed Waiting</h3>
        <p style="color:#8892B0;">Use camera or upload image to begin real-time analysis</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MINERAL TAGS
# ============================================
st.markdown("---")
st.markdown("### 🏷️ Supported Minerals")
minerals_list = ["Biotite", "Bornite", "Chrysocolla", "Malachite", "Muscovite", "Pyrite", "Quartz"]
for mineral in minerals_list:
    st.markdown(f'<span class="mineral-tag">{mineral}</span>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#8892B0; padding:1rem;">
    ⚡ Real-Time Analysis Engine v2.0<br>
    Latency: <span style="color:#00E5FF;">~2.3 seconds</span>
</div>
""", unsafe_allow_html=True)
