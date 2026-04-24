import torch
import clip
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# semantic labels you care about
LABELS = [
    "a sports match",
    "a cricket match",
    "a movie scene",
    "a fight scene",
    "a song performance",
    "a vlog video",
    "people talking",
    "a crowd",
    "a stadium",
    "an indoor scene"
]

def get_embedding(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        emb = model.encode_image(image)
    return emb / emb.norm(dim=-1, keepdim=True)

def clip_similarity(img1, img2):
    emb1 = get_embedding(img1)
    emb2 = get_embedding(img2)

    sim = (emb1 @ emb2.T).item() * 100

    # 🔥 semantic labeling
    text = clip.tokenize(LABELS).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        probs1 = (emb1 @ text_features.T).softmax(dim=-1)
        probs2 = (emb2 @ text_features.T).softmax(dim=-1)

    label1 = LABELS[probs1.argmax().item()]
    label2 = LABELS[probs2.argmax().item()]

    return sim, label1, label2