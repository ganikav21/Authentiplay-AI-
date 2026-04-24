import json
from collections import defaultdict

DATA_PATH = "data/history.json"

def load_history():
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def detect_source(videos, similarity_map):

    history = load_history()

    scores = defaultdict(float)

    for v in videos:

        channel = v["channel"]

        # 🧠 base score: earlier upload = higher score
        scores[channel] += 30

        # 🧠 similarity influence
        for (v1, v2), sim in similarity_map.items():

            if v["video_id"] == v1:
                scores[channel] += sim * 0.2

        # 🧠 repost penalty
        repost_count = sum(1 for h in history if h["channel"] == channel)
        scores[channel] -= repost_count * 2

    # normalize
    best_channel = max(scores, key=scores.get)
    confidence = min(100, round(scores[best_channel], 2))

    return best_channel, confidence, dict(scores)