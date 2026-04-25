import torch
import clip
from PIL import Image
import numpy as np
import cv2

device = "cuda" if torch.cuda.is_available() else "cpu"
model = None
preprocess = None
CLIP_READY = False

try:
    model, preprocess = clip.load("ViT-B/32", device=device)
    CLIP_READY = True
except Exception:
    CLIP_READY = False

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
    if not CLIP_READY:
        return None
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        emb = model.encode_image(image)
    return emb / emb.norm(dim=-1, keepdim=True)

def clip_similarity(img1, img2):
    if not CLIP_READY:
        return 0.0, "clip_unavailable", "clip_unavailable"
    emb1 = get_embedding(img1)
    emb2 = get_embedding(img2)
    if emb1 is None or emb2 is None:
        return 0.0, "clip_unavailable", "clip_unavailable"

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


def _extract_first_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    ok, frame = cap.read()
    cap.release()
    if not ok or frame is None:
        return None
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def compute_clip_similarity(video1_path, video2_path):
    if not CLIP_READY:
        return 0.0
    frame1 = _extract_first_frame(video1_path)
    frame2 = _extract_first_frame(video2_path)
    if frame1 is None or frame2 is None:
        return 0.0

    image1 = preprocess(frame1).unsqueeze(0).to(device)
    image2 = preprocess(frame2).unsqueeze(0).to(device)

    with torch.no_grad():
        emb1 = model.encode_image(image1)
        emb2 = model.encode_image(image2)
        emb1 = emb1 / emb1.norm(dim=-1, keepdim=True)
        emb2 = emb2 / emb2.norm(dim=-1, keepdim=True)
        sim = (emb1 @ emb2.T).item() * 100

    return round(float(max(0.0, sim)), 2)