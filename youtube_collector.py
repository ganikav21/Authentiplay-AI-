from googleapiclient.discovery import build

API_KEY = "AIzaSyBecJWTMhCPA4DGGeUVbLz5J8H3mrUHgnY"

def search_videos(query, max_results=5):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video",
        order="relevance"
    )

    response = request.execute()

    videos = []

    for item in response["items"]:
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]

        videos.append({
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "published_at": snippet["publishedAt"],
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "video_id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}"
        })

    return videos
