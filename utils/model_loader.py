
import os
import requests
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
import timm

MODEL_URL = "https://github.com/darkmoorltd-jpg/Spectra/releases/download/v1.0-384/open_set_mineral_model_384.pt"
MODEL_PATH = "models/open_set_mineral_model_384.pt"

def ensure_model():
    """Download the model if not present or too small."""
    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 10_000_000:  # 10 MB
        os.makedirs("models", exist_ok=True)
        print(f"Downloading model from {MODEL_URL} ...")
        r = requests.get(MODEL_URL, stream=True, timeout=300)
        r.raise_for_status()
        total_size = 0
        with open(MODEL_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=32768):
                if chunk:
                    f.write(chunk)
                    total_size += len(chunk)
        print(f"Downloaded {total_size/1024/1024:.1f} MB")
    return MODEL_PATH

@torch.no_grad()
def load_mineral_model():
    """Load the trained model, prototypes, threshold, class_names, img_size.
    Returns a dict with everything needed for inference, or None on failure."""
    try:
        path = ensure_model()
        checkpoint = torch.load(path, map_location="cpu", weights_only=False)
        class_names = checkpoint['class_names']
        prototypes = checkpoint['prototypes']
        threshold = checkpoint['threshold']
        img_size = checkpoint['img_size']

        # Rebuild the ViT-Small 384 model with correct number of classes
        model = timm.create_model("vit_small_patch16_384", pretrained=False, num_classes=len(class_names))
        model.load_state_dict(checkpoint['model_state'])
        model.eval()

        # Create feature extractor (everything except final head)
        feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])
        feature_extractor.eval()

        # Convert prototypes to torch tensors for faster computation
        proto_tensors = {cls: torch.tensor(v, dtype=torch.float32) for cls, v in prototypes.items()}

        return {
            'feature_extractor': feature_extractor,
            'prototypes': proto_tensors,
            'threshold': threshold,
            'class_names': class_names,
            'img_size': img_size
        }
    except Exception as e:
        print(f"Model loading failed: {e}")
        return None

def predict_mineral(model_dict, image: Image.Image):
    """Run open‑set inference.
    Returns (mineral_name, confidence, grade) where:
      - mineral_name is "Unknown" if max similarity < threshold
      - confidence is the cosine similarity (0..1), can be used as confidence score
      - grade is set to None for unknown; for known minerals we still return a placeholder (0.0)
    """
    if model_dict is None:
        return "Unknown", 0.0, 0.0

    feature_extractor = model_dict['feature_extractor']
    prototypes = model_dict['prototypes']
    threshold = model_dict['threshold']
    class_names = model_dict['class_names']
    img_size = model_dict['img_size']

    # Preprocess image
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img_tensor = transform(image).unsqueeze(0)

    # Extract embedding
    with torch.no_grad():
        features = feature_extractor(img_tensor)  # [1, N, D]
        embedding = features[:, 0, :].squeeze()   # CLS token

    # Compute cosine similarity to each prototype
    def cosine_sim(a, b):
        return torch.dot(a, b) / (torch.norm(a) * torch.norm(b) + 1e-8)

    sims = {cls: cosine_sim(embedding, proto) for cls, proto in prototypes.items()}
    best_cls = max(sims, key=sims.get)
    best_sim = sims[best_cls].item()

    if best_sim < threshold:
        return "Unknown", best_sim, None
    else:
        return best_cls, best_sim, None  # grade to be filled later if needed
