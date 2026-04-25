import requests
import cv2
import numpy as np

def download_image(url):
    resp = requests.get(url, stream=True).raw
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    return cv2.imdecode(img, cv2.IMREAD_COLOR)

def thumbnail_similarity(url1, url2):
    try:
        img1 = download_image(url1)
        img2 = download_image(url2)

        img1 = cv2.resize(img1, (100, 100))
        img2 = cv2.resize(img2, (100, 100))

        diff = np.mean((img1 - img2) ** 2)

        score = max(0, 100 - diff / 10)
        return score
    except:
        return 0

def duration_similarity(d1, d2):
    if d1 is None or d2 is None:
        return 50
    return 100 if d1 == d2 else 50


def _safe_duration(video):
    # Supports both previous and new ingestion schema.
    if "duration" in video:
        return video.get("duration")
    return video.get("duration_iso8601")

def compute_similarity(v1, v2):

    thumb_score = thumbnail_similarity(v1["thumbnail"], v2["thumbnail"])
    dur_score = duration_similarity(_safe_duration(v1), _safe_duration(v2))

    final_score = (0.7 * thumb_score) + (0.3 * dur_score)

    return round(final_score, 2)