import feedparser
import yt_dlp
from instagrapi import Client
import os

# Get secrets from environment
YT_CHANNEL_ID = os.getenv("YT_CHANNEL_ID")
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

# Login to Instagram
cl = Client()
cl.load_settings(".session/settings.json") if os.path.exists(".session/settings.json") else None
cl.login(IG_USERNAME, IG_PASSWORD)

# Fetch latest video from YouTube channel
rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={YT_CHANNEL_ID}"
feed = feedparser.parse(rss_url)
latest = feed.entries[0]
video_url = latest.link
title = latest.title
description = latest.get("media_description", "") or latest.get("summary", "")
tags = latest.get("media_keywords", "").split(",") if latest.get("media_keywords") else []

# Download video
video_opts = {
    "outtmpl": "short.mp4",
    "format": "mp4",
    "quiet": True,
    "noplaylist": True
}
with yt_dlp.YoutubeDL(video_opts) as ydl:
    ydl.download([video_url])

# Caption with tags
caption = f"{title}\n\n{description}\n\n" + " ".join([f"#{tag.strip().replace(' ', '')}" for tag in tags if tag.strip()])[:2200]

# Upload to IG Reels
cl.clip_upload("short.mp4", caption=caption)

# Save session and cleanup
os.makedirs(".session", exist_ok=True)
cl.dump_settings(".session/settings.json")
os.remove("short.mp4")

print("✅ Auto-posted to Instagram.")
