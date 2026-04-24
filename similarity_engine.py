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
    # simple check
    return 100 if d1 == d2 else 50

def compute_similarity(v1, v2):

    thumb_score = thumbnail_similarity(v1["thumbnail"], v2["thumbnail"])
    dur_score = duration_similarity(v1["duration"], v2["duration"])

    final_score = (0.7 * thumb_score) + (0.3 * dur_score)

    return round(final_score, 2)