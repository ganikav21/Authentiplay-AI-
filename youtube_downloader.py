import os

def download_video(video_id, output_path="downloads"):
    """
    SAFE VERSION (NO PYTUBE)
    """

    os.makedirs(output_path, exist_ok=True)

    # always return local file for stable demo
    return "sample_videos/official.mp4"