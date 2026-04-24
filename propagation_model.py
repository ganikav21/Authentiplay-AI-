def generate_propagation(similarity):

    nodes = ["YouTube", "Telegram", "WhatsApp", "Pirate Sites", "Users"]

    base = similarity / 100

    edges = []

    # REALISTIC LOGIC (NO RANDOMNESS)
    if base >= 0.8:

        edges = [
            {"from": "YouTube", "to": "Telegram", "probability": round(base, 2)},
            {"from": "Telegram", "to": "WhatsApp", "probability": round(base - 0.05, 2)},
            {"from": "WhatsApp", "to": "Pirate Sites", "probability": round(base - 0.1, 2)},
            {"from": "Pirate Sites", "to": "Users", "probability": round(base, 2)},
        ]

    elif base >= 0.5:

        edges = [
            {"from": "YouTube", "to": "Telegram", "probability": round(base, 2)},
            {"from": "Telegram", "to": "Users", "probability": round(base - 0.2, 2)},
        ]

    else:

        edges = [
            {"from": "YouTube", "to": "Users", "probability": round(base, 2)},
        ]

    return {
        "origin": "YouTube",
        "nodes": nodes,
        "edges": edges
    }