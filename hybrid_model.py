def compute_hybrid_score(frame_sim, thumb_sim, duration1, duration2):

    duration_sim = max(0, 100 - abs(duration1 - duration2))

    final_score = (
        0.6 * frame_sim +
        0.25 * thumb_sim +
        0.15 * duration_sim
    )

    return round(final_score, 2)