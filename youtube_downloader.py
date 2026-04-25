import os
import shutil
import subprocess

def download_video(video_id, output_path="downloads"):
    """
    Download a YouTube video using yt-dlp (if available).
    Returns local file path on success, else None.
    """
    os.makedirs(output_path, exist_ok=True)

    if not video_id:
        return None

    yt_dlp_path = shutil.which("yt-dlp")
    if yt_dlp_path is None:
        return None

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    output_template = os.path.join(output_path, f"{video_id}.%(ext)s")

    cmd = [
        yt_dlp_path,
        "-f",
        "mp4/best",
        "--no-playlist",
        "-o",
        output_template,
        video_url,
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except Exception:
        return None

    # Find downloaded file by prefix.
    for file_name in os.listdir(output_path):
        if file_name.startswith(f"{video_id}."):
            return os.path.join(output_path, file_name)
    return None