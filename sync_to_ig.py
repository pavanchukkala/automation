import os
import subprocess
import feedparser
from instagrapi import Client
from yt_dlp import YoutubeDL

# 1. Fetch latest YouTube Short ID
feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={os.getenv('YT_CHANNEL_ID')}"
feed     = feedparser.parse(feed_url)
video_id = feed.entries[0].yt_videoid
video_url = f"https://youtu.be/{video_id}"
filename = f"{video_id}.mp4"

# 2. Extract metadata (title, description, tags) via yt-dlp API
ydl_opts = {'quiet': True, 'skip_download': True}
with YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(video_url, download=False)
title       = info.get('title', '').strip()
description = info.get('description', '').strip()
tags_list   = info.get('tags', [])

# Build a hashtag string from up to 10 tags
hashtags = ' '.join('#' + t.replace(' ', '') for t in tags_list[:10])

# Combine into one Instagram caption
caption = f"{title}\n\n{description}\n\n{hashtags}"

# 3. Download the Short video via yt-dlp CLI
subprocess.run([
    "yt-dlp",
    video_url,
    "-o", filename,
    "--format", "mp4",
    "--max-downloads", "1"
], check=True)

# 4. Log in to Instagram (session cached in .session/)
os.makedirs(".session", exist_ok=True)
cl = Client(session_folder=".session")
cl.login(os.getenv("IG_USERNAME"), os.getenv("IG_PASSWORD"))

# 5. Post as a Reel with full metadata
cl.video_upload(filename, caption=caption)
print(f"✅ Posted {filename} with title, description & tags to Instagram Reels")
