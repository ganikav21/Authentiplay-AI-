import cv2
import imagehash
from PIL import Image


def extract_frames(video_path, skip=15):
    cap = cv2.VideoCapture(video_path)
    frames = []
    i = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if i % skip == 0:
            frames.append(frame)
        i += 1

    cap.release()
    return frames


def _frame_to_hash(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb)
    return imagehash.phash(pil_image)


def compute_hashes(frames):
    hashes = []
    for frame in frames:
        try:
            hashes.append(_frame_to_hash(frame))
        except Exception:
            continue
    return hashes


def compare_hashes(hashes1, hashes2, threshold=10):
    if not hashes1 or not hashes2:
        return 0.0

    matches = 0
    for h1 in hashes1:
        best_distance = min((h1 - h2) for h2 in hashes2)
        if best_distance <= threshold:
            matches += 1

    return round((matches / len(hashes1)) * 100, 2)
