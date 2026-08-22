
import torch
import numpy as np
from PIL import Image
from torchvision import transforms

def load_mineral_model():
    """Placeholder: returns None to use demo predictions.
       In future, load a trained ViT/ConvNeXt model here."""
    return None

def predict_mineral(model, image: Image.Image):
    """Run inference if model exists; otherwise return random demo."""
    if model is None:
        import random
        minerals = ["Gold", "Cassiterite", "Coltan", "Lithium (Spodumene)",
                    "Copper Ore", "Iron Ore", "Lead-Zinc", "Quartz", "Bauxite", "Tin"]
        mineral = random.choice(minerals)
        confidence = random.uniform(0.75, 0.98)
        grade = random.uniform(0.2, 0.9)
        return mineral, confidence, grade
    # Real inference code will go here
    pass
