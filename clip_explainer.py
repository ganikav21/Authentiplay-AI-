import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import cv2

# ================= LOAD MODEL =================
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


# ================= GET KEY FRAMES =================
def get_key_frames(video_path, max_frames=5):
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0

    while cap.isOpened() and count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(Image.fromarray(frame))
        count += 1

    cap.release()
    return frames


# ================= CLASSIFY FRAME =================
def classify_frames(frames):
    labels = [
        "cricket match",
        "football game",
        "people talking",
        "outdoor scene",
        "crowd audience",
        "sports action",
        "dance performance",
        "movie scene"
    ]

    inputs = processor(text=labels, images=frames, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image

    probs = logits_per_image.softmax(dim=1)

    results = []

    for i in range(len(frames)):
        top = torch.argmax(probs[i]).item()
        results.append(labels[top])

    return results


# ================= MAIN EXPLANATION ENGINE =================
def explain_clip(video1, video2):

    frames1 = get_key_frames(video1)
    frames2 = get_key_frames(video2)

    labels1 = classify_frames(frames1)
    labels2 = classify_frames(frames2)

    common = set(labels1) & set(labels2)

    explanation = {
        "video1_concepts": labels1,
        "video2_concepts": labels2,
        "common_concepts": list(common)
    }

    return explanation