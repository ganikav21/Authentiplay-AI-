def generate_explanation(similarity, risk, match_found):

    reasons = []

    # similarity reasoning
    if similarity > 75:
        reasons.append("High frame-level similarity detected across multiple segments.")
        reasons.append("Visual structure strongly matches known content patterns.")

    elif similarity > 40:
        reasons.append("Partial similarity found in key frames.")
        reasons.append("Some segments resemble known content.")

    else:
        reasons.append("Low similarity across analyzed frames.")
        reasons.append("No strong reuse detected.")

    # match reasoning
    if match_found:
        reasons.append("Matching content found on external platform (YouTube).")
    else:
        reasons.append("No direct external match found.")

    # risk reasoning
    if risk == "HIGH RISK":
        reasons.append("Classified as HIGH RISK due to strong similarity signals.")

    elif risk == "MEDIUM RISK":
        reasons.append("Moderate risk due to partial matches.")

    else:
        reasons.append("Content appears safe under current thresholds.")

    return reasons