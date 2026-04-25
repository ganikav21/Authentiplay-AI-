import requests
import os
import json
from datetime import datetime, timezone

from youtube_collector import ingest_videos
from youtube_downloader import download_video as download_youtube_video


# ================= DOWNLOAD VIDEO =================
def download_video(url, path):

    r = requests.get(url, stream=True)

    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return path


# ================= INGEST MULTIPLE SOURCES =================
def ingest_sources(urls):

    os.makedirs("data/live", exist_ok=True)

    paths = []

    for i, url in enumerate(urls):

        path = f"data/live/video_{i}.mp4"
        download_video(url, path)

        paths.append(path)

    return paths


def _utc_timestamp():
    return datetime.now(timezone.utc).isoformat()


def ingest_youtube_query(
    query,
    max_results=25,
    api_key=None,
    download_assets=False,
    download_dir="data/live/youtube_videos",
):
    """
    End-to-end YouTube ingestion pipeline:
    1) Search and hydrate video metadata from YouTube Data API
    2) Optionally download video assets using yt-dlp
    3) Return normalized records ready for matching/indexing
    """
    videos = ingest_videos(query=query, max_results=max_results, api_key=api_key)
    ingested_at = _utc_timestamp()
    records = []

    if download_assets:
        os.makedirs(download_dir, exist_ok=True)

    for video in videos:
        record = dict(video)
        record["ingested_at"] = ingested_at
        record["ingestion_query"] = query

        if download_assets:
            local_path = download_youtube_video(video["video_id"], output_path=download_dir)
            record["local_video_path"] = local_path
        else:
            record["local_video_path"] = None

        records.append(record)

    return records


def persist_ingestion_records(
    records,
    output_jsonl_path="data/live/youtube_ingestion.jsonl",
):
    """
    Persists ingestion records as JSON Lines for reproducible downstream runs.
    """
    os.makedirs(os.path.dirname(output_jsonl_path), exist_ok=True)
    with open(output_jsonl_path, "a", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=True) + "\n")
    return output_jsonl_path