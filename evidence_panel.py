import cv2
import numpy as np
from frame_hash import extract_frames, compute_hashes


# ================= FRAME SIMILARITY TIMELINE =================
def compute_frame_match_timeline(video1, video2):

    frames1 = extract_frames(video1)
    frames2 = extract_frames(video2)

    hashes1 = compute_hashes(frames1)
    hashes2 = compute_hashes(frames2)

    timeline = []

    min_len = min(len(hashes1), len(hashes2))

    for i in range(min_len):

        h1 = hashes1[i]
        h2 = hashes2[i]

        # Hamming-like similarity (simple diff score)
        diff = abs(h1 - h2)

        similarity = max(0, 100 - diff)

        timeline.append({
            "frame": i,
            "similarity": similarity
        })

    return timeline


# ================= FIND STRONG MATCH FRAMES =================
def get_evidence_frames(video1, video2, threshold=85):

    frames1 = extract_frames(video1)
    frames2 = extract_frames(video2)

    matches = []

    min_len = min(len(frames1), len(frames2))

    for i in range(min_len):

        f1 = frames1[i]
        f2 = frames2[i]

        # resize for comparison
        f1 = cv2.resize(f1, (64,64)).flatten()
        f2 = cv2.resize(f2, (64,64)).flatten()

        diff = np.mean(np.abs(f1 - f2))
        score = max(0, 100 - diff)

        if score > threshold:
            matches.append({
                "frame_index": i,
                "score": float(score)
            })

    return matches