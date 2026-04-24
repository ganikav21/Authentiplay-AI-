import pandas as pd
import random

# ================= GEO HEATMAP =================
def generate_geo_data(similarity, step):

    countries = ["India", "USA", "UK", "Germany", "Brazil"]

    data = []

    growth_factor = (step + 1) / 4

    for c in countries:
        base = similarity * random.uniform(0.4, 1.0)
        spread = base * growth_factor

        data.append({
            "country": c,
            "spread": round(spread, 2)
        })

    return pd.DataFrame(data)


# ================= COUNTRY DRILLDOWN =================
def generate_country_details(country, similarity):

    fake_sources = [
        "Telegram Leak",
        "Mirror Upload",
        "Edited Re-upload",
        "Third-party Distribution"
    ]

    details = []

    for i in range(3):
        details.append({
            "title": f"{country} Piracy Case {i+1}",
            "source": random.choice(fake_sources),
            "similarity": round(similarity * random.uniform(0.5, 1.0), 2)
        })

    return details


# ================= CASE DRILLDOWN =================
def generate_case_details(case, similarity):

    return {
        "video_title": case["title"],
        "match_score": case["similarity"],
        "frames_matched": int(case["similarity"] * 0.6),
        "frames_total": 100,
        "top_segments": [
            ("00:10 - 00:20", round(case["similarity"] * 0.9, 2)),
            ("01:05 - 01:20", round(case["similarity"] * 0.8, 2)),
            ("02:30 - 02:50", round(case["similarity"] * 0.85, 2)),
        ]
    }