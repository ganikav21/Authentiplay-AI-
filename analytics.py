def generate_stats(videos, similarity):

    total_uploads = len(videos)
    avg_similarity = similarity

    piracy_index = min(100, (similarity * total_uploads) / 2)

    return {
        "total_uploads": total_uploads,
        "avg_similarity": avg_similarity,
        "piracy_index": piracy_index
    }