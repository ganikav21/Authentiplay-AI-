import requests
import os


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