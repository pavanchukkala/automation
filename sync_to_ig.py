import feedparser
import yt_dlp
from instagrapi import Client
import os

# Hardcoded credentials – for testing ONLY
YT_CHANNEL_ID = "UCjECts5K34yUPWAQ-QziZJA"
IG_USERNAME = "kegth_group"
IG_PASSWORD = "Kegth@2025"

# Login to Instagram
cl = Client()
cl.login(IG_USERNAME, IG_PASSWORD)

# Fetch latest YouTube Short
rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={YT_CHANNEL_ID}"
feed = feedparser.parse(rss_url)
latest = feed.entries[0]
video_url = latest.link
title = latest.title
description = latest.get("media_description", "") or latest.get("summary", "")
tags = latest.get("media_keywords", "").split(",") if latest.get("media_keywords") else []

# Download video using yt-dlp
video_opts = {
    "outtmpl": "short.mp4",
    "format": "mp4",
    "quiet": True,
    "noplaylist": True,
    "merge_output_format": "mp4"
}
with yt_dlp.YoutubeDL(video_opts) as ydl:
    ydl.download([video_url])

# Create IG caption
caption = f"{title}\n\n{description}\n\n" + " ".join([f"#{tag.strip().replace(' ', '')}" for tag in tags if tag.strip()])[:2200]

# Upload to Instagram Reels
cl.clip_upload("short.mp4", caption=caption)

# Cleanup
os.remove("short.mp4")
print("✅ Uploaded to Instagram successfully.")
