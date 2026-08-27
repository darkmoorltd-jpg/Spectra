
import os
import tempfile
import base64
import io
import hashlib
import numpy as np
import cv2
from PIL import Image
import qrcode

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def generate_blockchain_hash(scan_data):
    hash_obj = hashlib.sha256()
    hash_obj.update(scan_data.encode('utf-8'))
    return hash_obj.hexdigest()

def overlay_heatmap(image, grade, mineral):
    img_array = np.array(image)
    hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, (0, 50, 50), (180, 255, 255))
    overlay = img_array.copy()
    if grade > 0.5:
        overlay[mask > 0] = [0, 255, 0]
    else:
        overlay[mask > 0] = [0, 0, 255]
    blended = cv2.addWeighted(img_array, 0.7, overlay, 0.3, 0)
    return Image.fromarray(blended)

def process_video_frames(video_file, num_frames=5):
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(video_file.read())
    tfile.close()
    cap = cv2.VideoCapture(tfile.name)
    frames = []
    count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, total_frames // num_frames) if total_frames > 0 else 1
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % step == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(frame_rgb))
        count += 1
        if len(frames) >= num_frames:
            break
    cap.release()
    os.unlink(tfile.name)
    return frames

def record_scratch_sound(duration=3):
    try:
        import sounddevice as sd
    except Exception as e:
        print(f"sounddevice not available: {e}")
        return None, None
    try:
        fs = 44100
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        return recording.flatten(), fs
    except Exception as e:
        print(f"Recording failed: {e}")
        return None, None

def analyze_sound(recording, fs):
    if recording is None or fs is None:
        return None, None
    try:
        import librosa
        y = recording.astype(np.float32)
        cent = librosa.feature.spectral_centroid(y=y, sr=fs)
        return np.mean(cent), np.std(cent)
    except Exception as e:
        print(f"Sound analysis failed: {e}")
        return None, None
