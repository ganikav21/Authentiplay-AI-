import os

from googleapiclient.discovery import build


YOUTUBE_API_ENV_KEY = "YOUTUBE_API_KEY"


def _get_api_key(explicit_key=None):
    if explicit_key:
        return explicit_key
    api_key = os.getenv(YOUTUBE_API_ENV_KEY, "").strip()
    if not api_key:
        raise ValueError(
            f"Missing YouTube API key. Set `{YOUTUBE_API_ENV_KEY}` in your environment."
        )
    return api_key


def _build_youtube(api_key):
    return build("youtube", "v3", developerKey=api_key)


def _chunked(items, size):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def _extract_thumbnail(snippet):
    thumbs = snippet.get("thumbnails", {})
    for key in ("maxres", "standard", "high", "medium", "default"):
        if key in thumbs and "url" in thumbs[key]:
            return thumbs[key]["url"]
    return ""


def ingest_videos(query, max_results=25, api_key=None, order="relevance"):
    """
    Real YouTube ingestion using Data API v3:
    - paginated search collection
    - metadata + stats hydration
    - stable normalized output
    """
    if not query or not str(query).strip():
        return []

    api_key = _get_api_key(api_key)
    youtube = _build_youtube(api_key)

    collected = []
    seen_video_ids = set()
    next_page_token = None

    while len(collected) < max_results:
        batch_size = min(50, max_results - len(collected))
        request = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=batch_size,
            type="video",
            order=order,
            pageToken=next_page_token,
        )
        response = request.execute()

        for item in response.get("items", []):
            video_id = item.get("id", {}).get("videoId")
            if not video_id or video_id in seen_video_ids:
                continue
            seen_video_ids.add(video_id)
            collected.append(item)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    if not collected:
        return []

    video_ids = [item["id"]["videoId"] for item in collected]
    details_by_id = {}

    for chunk in _chunked(video_ids, 50):
        details_resp = youtube.videos().list(
            id=",".join(chunk),
            part="snippet,statistics,contentDetails",
        ).execute()

        for detail in details_resp.get("items", []):
            details_by_id[detail.get("id")] = detail

    normalized = []
    for item in collected:
        video_id = item["id"]["videoId"]
        snippet = item.get("snippet", {})
        details = details_by_id.get(video_id, {})
        detail_snippet = details.get("snippet", snippet)
        stats = details.get("statistics", {})
        content = details.get("contentDetails", {})

        normalized.append(
            {
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": detail_snippet.get("title", snippet.get("title", "")),
                "description": detail_snippet.get("description", ""),
                "channel": detail_snippet.get("channelTitle", snippet.get("channelTitle", "")),
                "channel_id": detail_snippet.get("channelId", ""),
                "published_at": detail_snippet.get("publishedAt", snippet.get("publishedAt", "")),
                "thumbnail": _extract_thumbnail(detail_snippet or snippet),
                "duration_iso8601": content.get("duration", ""),
                "view_count": int(stats.get("viewCount", 0)) if str(stats.get("viewCount", "")).isdigit() else 0,
                "like_count": int(stats.get("likeCount", 0)) if str(stats.get("likeCount", "")).isdigit() else 0,
                "comment_count": int(stats.get("commentCount", 0)) if str(stats.get("commentCount", "")).isdigit() else 0,
            }
        )

    return normalized


def search_videos(query, max_results=5, api_key=None):
    """
    Backward-compatible function used by the Streamlit UI.
    """
    return ingest_videos(query=query, max_results=max_results, api_key=api_key)
