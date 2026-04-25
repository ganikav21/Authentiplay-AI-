import cv2
import numpy as np


CORNER_NAMES = ("top_left", "top_right", "bottom_left", "bottom_right")


def _sample_corner_patches(video_path, skip=20, max_frames=50, corner_ratio=0.22):
    cap = cv2.VideoCapture(video_path)
    patches = {name: [] for name in CORNER_NAMES}
    frame_count = 0
    i = 0

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        if i % skip == 0:
            h, w = frame.shape[:2]
            ch = max(16, int(h * corner_ratio))
            cw = max(16, int(w * corner_ratio))

            corners = {
                "top_left": frame[0:ch, 0:cw],
                "top_right": frame[0:ch, w - cw:w],
                "bottom_left": frame[h - ch:h, 0:cw],
                "bottom_right": frame[h - ch:h, w - cw:w],
            }

            for name, patch in corners.items():
                gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, (64, 64))
                patches[name].append(gray)

            frame_count += 1

        i += 1

    cap.release()
    return patches


def _corner_metrics(corner_patches):
    if len(corner_patches) < 2:
        return {"stability": 0.0, "edge_density": 0.0, "score": 0.0}

    diffs = []
    edge_scores = []

    for i in range(1, len(corner_patches)):
        prev_patch = corner_patches[i - 1]
        curr_patch = corner_patches[i]
        diffs.append(float(np.mean(np.abs(curr_patch.astype(np.float32) - prev_patch.astype(np.float32)))))

    for patch in corner_patches:
        edges = cv2.Canny(patch, 60, 120)
        edge_density = float(np.count_nonzero(edges)) / edges.size
        edge_scores.append(edge_density * 100)

    mean_diff = float(np.mean(diffs))
    stability = max(0.0, 100.0 - (mean_diff / 255.0) * 100.0)
    edge_density = float(np.mean(edge_scores))

    # Static logo-like regions are usually stable over time and contain edge structure.
    combined_score = (0.65 * stability) + (0.35 * edge_density)
    return {
        "stability": round(stability, 2),
        "edge_density": round(edge_density, 2),
        "score": round(combined_score, 2),
    }


def detect_watermark(video_path):
    try:
        patches = _sample_corner_patches(video_path)
        corner_scores = {name: _corner_metrics(corner_patches) for name, corner_patches in patches.items()}

        best_corner = max(corner_scores, key=lambda key: corner_scores[key]["score"])
        best_score = corner_scores[best_corner]["score"]
        detected = best_score >= 45.0

        return {
            "detected": detected,
            "location": best_corner if detected else "unknown",
            "confidence": round(best_score, 2),
            "corner_scores": corner_scores,
        }
    except Exception:
        return {
            "detected": False,
            "location": "unknown",
            "confidence": 0.0,
            "corner_scores": {},
        }


def compare_watermarks(video1_path, video2_path):
    wm1 = detect_watermark(video1_path)
    wm2 = detect_watermark(video2_path)

    if wm1["detected"] and wm2["detected"]:
        location_bonus = 20.0 if wm1["location"] == wm2["location"] else 0.0
        confidence_gap = abs(wm1["confidence"] - wm2["confidence"])
        similarity = max(0.0, 80.0 - confidence_gap + location_bonus)
    elif not wm1["detected"] and not wm2["detected"]:
        similarity = 50.0
    else:
        similarity = 20.0

    return round(similarity, 2), wm1, wm2
