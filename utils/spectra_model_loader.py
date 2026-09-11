
import os
import io
import zipfile
import requests
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms
import timm

MODEL_URL = "https://github.com/darkmoorltd-jpg/Spectra/releases/download/v2.0-mineral-classifier/spectra_model.zip"
MODEL_DIR = "models/spectra_classifier"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pt")
CONFIG_PATH = os.path.join(MODEL_DIR, "config.json")

CLASS_NAMES = ["biotite", "bornite", "chrysocolla", "malachite", "muscovite", "pyrite", "quartz"]

# Common names for display
DISPLAY_NAMES = {
    "biotite": "Biotite (Dark Mica)",
    "bornite": "Bornite (Peacock Ore)",
    "chrysocolla": "Chrysocolla",
    "malachite": "Malachite",
    "muscovite": "Muscovite (White Mica)",
    "pyrite": "Pyrite (Fool's Gold)",
    "quartz": "Quartz",
}

def ensure_model():
    """Download and extract the model if not present."""
    if os.path.exists(MODEL_PATH) and os.path.exists(CONFIG_PATH):
        return True
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    zip_path = os.path.join(MODEL_DIR, "spectra_model.zip")
    
    print(f"📥 Downloading model from {MODEL_URL}")
    r = requests.get(MODEL_URL, stream=True, timeout=300)
    r.raise_for_status()
    
    with open(zip_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)
    
    # Extract
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(MODEL_DIR)
    
    os.remove(zip_path)
    
    # Find model.pt and config.json (they might be in subfolder)
    for root, dirs, files in os.walk(MODEL_DIR):
        if "model.pt" in files:
            os.rename(os.path.join(root, "model.pt"), MODEL_PATH)
        if "config.json" in files:
            os.rename(os.path.join(root, "config.json"), CONFIG_PATH)
    
    return os.path.exists(MODEL_PATH)

def load_model():
    """Load ViT-Small model with trained weights."""
    try:
        ensure_model()
        import json
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        img_size = config.get("img_size", 384)
        class_names = config.get("class_names", CLASS_NAMES)
        
        model = timm.create_model(
            config.get("model_name", "vit_small_patch16_384"),
            pretrained=False,
            num_classes=len(class_names),
        )
        model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
        model.eval()
        return model, class_names, img_size
    except Exception as e:
        print(f"⚠️ Model load failed: {e}")
        return None, CLASS_NAMES, 384

def predict(model, class_names, img_size, image: Image.Image, confidence_threshold=0.60):
    """
    Run inference with confidence threshold.
    Returns dict with: mineral, confidence, all_probs, is_unknown, top_3
    """
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    
    tensor = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        logits = model(tensor)
        probs = F.softmax(logits, dim=1)[0].cpu().numpy()
    
    top_idx = int(probs.argmax())
    confidence = float(probs[top_idx])
    
    # Sort for top-3
    sorted_idx = probs.argsort()[::-1]
    top_3 = [(class_names[i], float(probs[i])) for i in sorted_idx[:3]]
    
    is_unknown = confidence < confidence_threshold
    
    return {
        "mineral": class_names[top_idx] if not is_unknown else "Unknown",
        "display_name": DISPLAY_NAMES.get(class_names[top_idx], class_names[top_idx]) if not is_unknown else "Unknown Mineral",
        "confidence": confidence,
        "all_probs": {class_names[i]: float(probs[i]) for i in range(len(class_names))},
        "is_unknown": is_unknown,
        "top_3": top_3,
        "threshold": confidence_threshold,
    }
