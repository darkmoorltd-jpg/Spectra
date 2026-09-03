
import streamlit as st
import cv2
import tempfile
import os
import numpy as np
from PIL import Image
import random
import time
import plotly.graph_objects as go
from utils.style import apply_global_style
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Video Analysis", page_icon="🎥", layout="wide")
apply_global_style()
render_sidebar()

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

.video-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #00E5FF 0%, #FFD700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.frame-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
}

.frame-card {
    background: #0D1B2A;
    border: 1px solid #1F2A44;
    border-radius: 12px;
    padding: 10px;
    text-align: center;
    width: 200px;
}

.frame-label {
    color: #FFD700;
    font-weight: 700;
    font-size: 0.9rem;
    margin-top: 5px;
}

.result-banner {
    background: #0D1B2A;
    border: 2px solid #FFD700;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 0 30px rgba(255,215,0,0.3);
}

.result-mineral {
    font-family: 'Orbitron', sans-serif;
    font-size: 2rem;
    font-weight: 900;
    color: #FFD700;
}

.stat-box {
    background: #0D1B2A;
    border: 1px solid #1F2A44;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="video-header">🎥 VIDEO UPLOAD ANALYSIS</div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#8892B0; margin-bottom:1rem;">
    Upload a video of your mineral sample. We'll extract frames and analyze each one.
</div>
""", unsafe_allow_html=True)

# ============================================
# VIDEO UPLOAD
# ============================================
video_file = st.file_uploader("📤 Upload Video", type=["mp4", "mov", "avi", "webm"])

if video_file is not None:
    # Save video to temp file
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(video_file.read())
    tfile.close()
    
    # Show video
    st.video(video_file)
    
    # ============================================
    # ANALYSIS OPTIONS
    # ============================================
    st.markdown("---")
    st.markdown("### ⚙️ Analysis Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        num_frames = st.slider("Number of frames to extract", min_value=3, max_value=20, value=5)
    with col2:
        confidence_threshold = st.slider("Confidence threshold", min_value=0.5, max_value=0.95, value=0.7, step=0.05)
    
    if st.button("🔍 Analyze Video", type="primary", use_container_width=True):
        with st.spinner("📊 Processing video frames..."):
            # Extract frames
            cap = cv2.VideoCapture(tfile.name)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            step = max(1, total_frames // num_frames)
            
            frames = []
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_count % step == 0:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(Image.fromarray(frame_rgb))
                frame_count += 1
                if len(frames) >= num_frames:
                    break
            cap.release()
            
            # Progress bar
            progress_bar = st.progress(0)
            
            # Simulate analysis on each frame
            minerals = ["Biotite", "Bornite", "Chrysocolla", "Malachite", "Muscovite", "Pyrite", "Quartz"]
            results = []
            
            for i, frame in enumerate(frames):
                progress_bar.progress((i + 1) / len(frames))
                time.sleep(0.3)
                
                # Random prediction for demo (replace with real model)
                mineral = random.choice(minerals)
                confidence = random.uniform(0.6, 0.98)
                results.append({
                    "mineral": mineral,
                    "confidence": confidence,
                    "frame": frame
                })
            
            progress_bar.progress(1.0)
        
        # ============================================
        # DISPLAY EXTRACTED FRAMES
        # ============================================
        st.markdown("---")
        st.markdown("### 🖼️ Extracted Frames")
        
        st.markdown('<div class="frame-grid">', unsafe_allow_html=True)
        cols = st.columns(min(5, len(frames)))
        for i, result in enumerate(results):
            with cols[i % 5]:
                st.image(result["frame"], caption=f"Frame {i+1}", use_container_width=True)
                st.markdown(f'<div class="frame-label">{result["mineral"]} | {result["confidence"]*100:.1f}%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ============================================
        # AGGREGATE RESULTS
        # ============================================
        st.markdown("---")
        st.markdown("### 📊 Aggregate Analysis")
        
        # Find most common mineral
        mineral_votes = {}
        for result in results:
            mineral = result["mineral"]
            if mineral not in mineral_votes:
                mineral_votes[mineral] = []
            mineral_votes[mineral].append(result["confidence"])
        
        # Average confidence per mineral
        avg_minerals = {}
        for mineral, confidences in mineral_votes.items():
            avg_minerals[mineral] = np.mean(confidences)
        
        # Sort by average confidence
        best_mineral = max(avg_minerals, key=avg_minerals.get)
        best_confidence = avg_minerals[best_mineral]
        agreement = len(mineral_votes[best_mineral]) / len(results) * 100
        
        # ============================================
        # RESULT BANNER
        # ============================================
        st.markdown(f"""
        <div class="result-banner">
            <h3 style="color:#8892B0; margin:0;">MOST LIKELY MINERAL</h3>
            <div class="result-mineral">{best_mineral}</div>
            <p style="color:#00E5FF; font-size:1.2rem; margin:10px 0;">Confidence: {best_confidence*100:.1f}%</p>
            <p style="color:#8892B0;">Frame Agreement: {agreement:.0f}% ({len(mineral_votes[best_mineral])}/{len(results)} frames)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ============================================
        # CONFIDENCE DISTRIBUTION
        # ============================================
        st.markdown("### 📈 Confidence Distribution")
        
        fig = go.Figure()
        for mineral, conf in avg_minerals.items():
            fig.add_trace(go.Bar(
                x=[mineral],
                y=[conf*100],
                name=mineral,
                marker_color='#FFD700' if mineral == best_mineral else '#1F2A44'
            ))
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E0E0'),
            xaxis_title="Mineral",
            yaxis_title="Confidence (%)",
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # ============================================
        # FRAME-BY-FRAME TABLE
        # ============================================
        st.markdown("### 📋 Frame-by-Frame Results")
        
        table_data = []
        for i, result in enumerate(results):
            table_data.append({
                "Frame": f"Frame {i+1}",
                "Mineral": result["mineral"],
                "Confidence": f"{result['confidence']*100:.1f}%"
            })
        
        st.dataframe(table_data, use_container_width=True)
        
        # ============================================
        # QUICK ACTIONS
        # ============================================
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Save Results", use_container_width=True):
                st.success("Results saved to vault")
        with col2:
            if st.button("📄 Download Report", use_container_width=True):
                st.info("Report generation coming soon")
        with col3:
            if st.button("🔊 Voice Explanation", use_container_width=True):
                st.info("Voice coming soon")
    
    # Clean up temp file
    os.unlink(tfile.name)

else:
    # Placeholder
    st.markdown("""
    <div style="text-align:center; padding:3rem; background:#0D1B2A; border:2px dashed #1F2A44; border-radius:16px;">
        <div style="font-size:5rem;">🎥</div>
        <h3 style="color:#00E5FF;">Waiting for Video Upload</h3>
        <p style="color:#8892B0;">Upload a video of your mineral sample to begin analysis</p>
        <p style="color:#FFD700; font-size:0.9rem;">Supported formats: MP4, MOV, AVI, WEBM</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#8892B0; padding:1rem;">
    ⚡ Video Analysis Engine v1.0<br>
    Extracts up to 20 frames per video for mineral identification
</div>
""", unsafe_allow_html=True)
