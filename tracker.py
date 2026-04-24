import os
import json
from datetime import datetime

DATA_PATH = "data/history.json"


# ---------------- LOAD ----------------
def load_history():
    if not os.path.exists(DATA_PATH):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, "w") as f:
            json.dump([], f)
        return []

    try:
        with open(DATA_PATH, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except:
        with open(DATA_PATH, "w") as f:
            json.dump([], f)
        return []


# ---------------- SAVE ----------------
def save_history(data):
    try:
        temp_path = DATA_PATH + ".tmp"
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(temp_path, DATA_PATH)
    except Exception as e:
        print("Save error:", e)


# ---------------- TRACK ----------------
def track_videos(videos, query):

    history = load_history()
    timestamp = datetime.now().isoformat()

    for v in videos:
        history.append({
            "query": query,
            "video_id": v.get("video_id", ""),
            "title": v.get("title", ""),
            "channel": v.get("channel", ""),
            "published_at": v.get("published_at", ""),
            "timestamp": timestamp
        })

    save_history(history)


# ---------------- ANALYZE ----------------
def analyze_reposts(videos):

    history = load_history()
    reposts = []

    for v in videos:
        for h in history:

            if v["video_id"] == h["video_id"]:
                continue

            if v["title"][:20].lower() == h["title"][:20].lower():
                reposts.append({
                    "current": v["channel"],
                    "original": h["channel"],
                    "title": v["title"]
                })

    return reposts