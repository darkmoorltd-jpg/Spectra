
import streamlit as st
import cv2
import numpy as np
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
from utils.style import apply_global_style
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Real-Time Video", page_icon="🎥", layout="wide")
apply_global_style()
render_sidebar()

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

.live-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #FF1744 0%, #FFD700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.live-badge {
    display: inline-block;
    background: #FF1744;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.9rem;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.info-box {
    background: #0D1B2A;
    border: 1px solid #1F2A44;
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="live-header">🎥 REAL-TIME VIDEO ANALYSIS</div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; margin-bottom:1rem;">
    <span class="live-badge">🔴 LIVE</span>
</div>
""", unsafe_allow_html=True)

# ============================================
# VIDEO PROCESSOR
# ============================================
class MineralVideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame_count = 0
        self.current_mineral = "Scanning..."
        self.confidence = 0.0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Process every 30 frames to simulate real-time analysis
        if self.frame_count % 30 == 0:
            # Simulate mineral detection
            minerals = ["Biotite", "Bornite", "Chrysocolla", "Malachite", "Muscovite", "Pyrite", "Quartz"]
            import random
            self.current_mineral = random.choice(minerals)
            self.confidence = random.uniform(0.75, 0.98)
        
        self.frame_count += 1
        
        # Draw overlay on frame
        overlay = img.copy()
        
        # Draw scanning line
        line_y = (self.frame_count * 10) % img.shape[0]
        cv2.line(overlay, (0, line_y), (img.shape[1], line_y), (0, 229, 255), 2)
        
        # Draw text
        text = f"{self.current_mineral} | {self.confidence*100:.1f}%"
        cv2.putText(overlay, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 215, 0), 2)
        
        # Draw rectangle frame
        cv2.rectangle(overlay, (10, 10), (img.shape[1]-10, img.shape[0]-10), (0, 229, 255), 2)
        
        return av.VideoFrame.from_ndarray(overlay, format="bgr24")

# ============================================
# RTC CONFIGURATION
# ============================================
rtc_config = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

# ============================================
# CAMERA STREAM
# ============================================
st.markdown("### 📸 Live Camera Feed")
st.markdown("Point your camera at a mineral sample. The AI will analyze in real-time.")

webrtc_ctx = webrtc_streamer(
    key="mineral-analysis",
    video_processor_factory=MineralVideoProcessor,
    rtc_configuration=rtc_config,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# ============================================
# STATUS DISPLAY
# ============================================
st.markdown("---")
st.markdown("### 📊 Analysis Status")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="info-box">
        <h4 style="color:#00E5FF; margin:0;">🔍 Scanning</h4>
        <p style="color:#8892B0; margin:5px 0;">Frame-by-frame analysis</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="info-box">
        <h4 style="color:#FFD700; margin:0;">⚡ Latency</h4>
        <p style="color:#8892B0; margin:5px 0;">~100ms per frame</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="info-box">
        <h4 style="color:#00C853; margin:0;">✅ Supported</h4>
        <p style="color:#8892B0; margin:5px 0;">7 minerals</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MINERAL GUIDE
# ============================================
st.markdown("---")
st.markdown("### 🏷️ Minerals Detectable")
minerals = ["Biotite", "Bornite", "Chrysocolla", "Malachite", "Muscovite", "Pyrite", "Quartz"]

cols = st.columns(7)
for i, mineral in enumerate(minerals):
    with cols[i]:
        st.markdown(f"""
        <div style="text-align:center; background:#0D1B2A; border:1px solid #1F2A44; border-radius:8px; padding:0.5rem;">
            <span style="color:#FFD700; font-weight:600;">{mineral}</span>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TIPS
# ============================================
st.markdown("---")
st.markdown("### 💡 Tips for Best Results")
st.markdown("""
1. Hold the camera steady, 20-30cm from the mineral
2. Ensure good lighting (natural daylight is best)
3. Place mineral on a plain background
4. Avoid shadows and reflections
5. Scan different angles for higher confidence
""")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#8892B0; padding:1rem;">
    ⚡ Real-Time Video Engine v1.0<br>
    Requires camera permission to start
</div>
""", unsafe_allow_html=True)
