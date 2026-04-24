import requests
from similarity_engine import compute_similarity


def download_thumbnail(url):
    try:
        return requests.get(url, timeout=5).content
    except:
        return None


def match_uploaded_with_youtube(uploaded_video_info, youtube_videos):

    best_match = None
    best_score = 0

    for vid in youtube_videos:

        # 🔥 similarity using your existing engine
        sim = compute_similarity(uploaded_video_info, vid)

        if sim > best_score:
            best_score = sim
            best_match = vid

    if best_match:
        return {
            "title": best_match["title"],
            "channel": best_match["channel"],
            "similarity": round(best_score, 2)
        }

    return None