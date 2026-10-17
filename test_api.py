import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

url = "https://www.googleapis.com/youtube/v3/videos"
params = {
    "part": "snippet,statistics",
    "chart": "mostPopular",
    "regionCode": "PK",
    "maxResults": 5,
    "key": API_KEY,
}

response = requests.get(url, params=params)
print("Status:", response.status_code)

data = response.json()
for item in data.get("items", []):
    print(item["snippet"]["title"], "|", item["statistics"].get("viewCount"))