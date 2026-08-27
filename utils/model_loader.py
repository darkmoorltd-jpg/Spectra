
import os
import requests
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
import timm

MODEL_URL = "https://github.com/darkmoorltd-jpg/Spectra/releases/download/v1.0-384-full/open_set_mineral_model_384_full.pt"
MODEL_PATH = "models/open_set_mineral_model_384_full.pt"

def ensure_model():
    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 10_000_000:
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
    try:
        path = ensure_model()
        checkpoint = torch.load(path, map_location="cpu", weights_only=False)
        class_names = checkpoint['class_names']
        prototypes = checkpoint['prototypes']
        threshold = checkpoint['threshold']
        img_size = checkpoint['img_size']

        model = timm.create_model("vit_small_patch16_384", pretrained=False, num_classes=len(class_names))
        model.load_state_dict(checkpoint['model_state'])
        model.eval()

        feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])
        feature_extractor.eval()

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


def estimate_grade(image: Image.Image, mineral: str) -> float:
    """Estimate ore grade based on simple visual heuristics.
    Returns a grade value between 0.1 and 0.9."""
    import numpy as np
    arr = np.array(image.convert("RGB"))
    # Compute average colour intensity and variation
    brightness = arr.mean() / 255.0
    saturation = (arr.max(axis=2) - arr.min(axis=2)).mean() / 255.0

    # Mineral-specific heuristics (approximate)
    if mineral == "Pyrite":
        # Pyrite is bright and metallic
        grade = 0.3 + (brightness * 0.4) + (saturation * 0.1)
    elif mineral in ["Malachite", "Chrysocolla", "Bornite"]:
        # Copper minerals often show vivid colours
        grade = 0.2 + (saturation * 0.6) + (brightness * 0.2)
    elif mineral == "Quartz":
        # Quartz grade for gold-bearing quartz is lower unless visible gold
        grade = 0.1 + (brightness * 0.2) + (saturation * 0.3)
    else:
        grade = 0.2 + (brightness * 0.3) + (saturation * 0.4)

    # Clip to reasonable range
    grade = max(0.1, min(0.9, grade))
    return grade
def predict_mineral(model_dict, image: Image.Image):
    if model_dict is None:
        return "Unknown", 0.0, 0.0

    feature_extractor = model_dict['feature_extractor']
    prototypes = model_dict['prototypes']
    threshold = model_dict['threshold']
    class_names = model_dict['class_names']
    img_size = model_dict['img_size']

    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        features = feature_extractor(img_tensor)
        embedding = features[:, 0, :].squeeze()

    def cosine_sim(a, b):
        return torch.dot(a, b) / (torch.norm(a) * torch.norm(b) + 1e-8)

    sims = {cls: cosine_sim(embedding, proto) for cls, proto in prototypes.items()}
    best_cls = max(sims, key=sims.get)
    best_sim = sims[best_cls].item()

    if best_sim < threshold:
        return "Unknown", best_sim, None
    else:
        return best_cls, best_sim, None
