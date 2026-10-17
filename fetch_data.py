import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE = "https://www.googleapis.com/youtube/v3"

HANDLE = "@MrBeast"  # any channel name
MAX_VIDEOS = 200


def get_uploads_playlist(handle):
    r = requests.get(f"{BASE}/channels", params={
        "part": "contentDetails",
        "forHandle": handle,
        "key": API_KEY,
    })
    r.raise_for_status()
    items = r.json().get("items", [])
    if not items:
        raise ValueError("No channel found!")
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_video_ids(playlist_id, limit):
    ids, token = [], None
    while len(ids) < limit:
        params = {
            "part": "contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": API_KEY,
        }
        if token:
            params["pageToken"] = token
        r = requests.get(f"{BASE}/playlistItems", params=params)
        r.raise_for_status()
        data = r.json()
        ids += [i["contentDetails"]["videoId"] for i in data["items"]]
        token = data.get("nextPageToken")
        if not token:
            break
    return ids[:limit]          # loop ke BAAD


def get_video_stats(video_ids):
    rows = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        r = requests.get(f"{BASE}/videos", params={
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(batch),
            "key": API_KEY,
        })
        r.raise_for_status()
        for item in r.json()["items"]:
            s = item["statistics"]
            rows.append({
                "video_id": item["id"],
                "title": item["snippet"]["title"],
                "published_at": item["snippet"]["publishedAt"],
                "duration": item["contentDetails"]["duration"],
                "views": int(s.get("viewCount", 0)),
                "likes": int(s.get("likeCount", 0)),
                "comments": int(s.get("commentCount", 0)),
            })
    return rows


if __name__ == "__main__":
    playlist = get_uploads_playlist(HANDLE)
    ids = get_video_ids(playlist, MAX_VIDEOS)
    print(f"{len(ids)} videos mili")

    df = pd.DataFrame(get_video_stats(ids))

    # cleaning
    df["published_at"] = pd.to_datetime(df["published_at"], utc=True).dt.tz_localize(None)
    df["duration_min"] = pd.to_timedelta(df["duration"]).dt.total_seconds() / 60
    df["engagement_rate"] = (df["likes"] + df["comments"]) / df["views"].replace(0, pd.NA) * 100
    df = df.drop(columns=["duration"]).drop_duplicates("video_id")

    os.makedirs("data", exist_ok=True)
    df.to_excel("data/youtube_data.xlsx", index=False)
    print("Excel save ho gayi")
    print(df.head())