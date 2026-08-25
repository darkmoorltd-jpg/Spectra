
import streamlit as st
import hashlib
import qrcode
import io
import base64
from PIL import Image
import numpy as np
import cv2

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def generate_blockchain_hash(scan_data):
    """Create a SHA-256 hash for verification."""
    hash_obj = hashlib.sha256()
    hash_obj.update(scan_data.encode('utf-8'))
    return hash_obj.hexdigest()

def overlay_heatmap(image, grade, mineral):
    """Simulate grade heatmap by highlighting regions based on color."""
    img_array = np.array(image)
    # Convert to HSV for color segmentation
    hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
    # Example: highlight high-saturation regions (mineral rich)
    mask = cv2.inRange(hsv, (0, 50, 50), (180, 255, 255))
    # Overlay semi-transparent red/ green depending on grade
    overlay = img_array.copy()
    if grade > 0.5:
        overlay[mask > 0] = [0, 255, 0]   # green for high grade
    else:
        overlay[mask > 0] = [0, 0, 255]   # red for low grade
    blended = cv2.addWeighted(img_array, 0.7, overlay, 0.3, 0)
    return Image.fromarray(blended)

def process_video_frames(video_file, num_frames=5):
    """Extract frames from a video and return list of PIL Images."""
    import tempfile
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(video_file.read())
    tfile.close()
    cap = cv2.VideoCapture(tfile.name)
    frames = []
    count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, total_frames // num_frames)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % step == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(frame_rgb))
        count += 1
    cap.release()
    os.unlink(tfile.name)
    return frames

def record_scratch_sound(duration=3):
    """Record audio from microphone for scratch test."""
    import sounddevice as sd
    fs = 44100
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return recording.flatten(), fs

def analyze_sound(recording, fs):
    """Extract frequency features from scratch sound."""
    import librosa
    # Ensure float32
    y = recording.astype(np.float32)
    # Compute spectral centroid
    cent = librosa.feature.spectral_centroid(y=y, sr=fs)
    return np.mean(cent), np.std(cent)
