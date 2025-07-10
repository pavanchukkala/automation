# File: sync_to_ig.py
import os
import subprocess
import feedparser
from instagrapi import Client

# 1. Fetch latest YouTube Short ID
feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={os.getenv('YT_CHANNEL_ID')}"
feed     = feedparser.parse(feed_url)
video_id = feed.entries[0].yt_videoid
filename = f"{video_id}.mp4"

# 2. Download via yt-dlp
subprocess.run([
    "yt-dlp",
    f"https://youtu.be/{video_id}",
    "-o", filename,
    "--format", "mp4",
    "--max-downloads", "1"
], check=True)

# 3. Log in to Instagram (session cached in .session/)
os.makedirs(".session", exist_ok=True)
cl = Client(session_folder=".session")
cl.login(os.getenv("IG_USERNAME"), os.getenv("IG_PASSWORD"))

# 4. Post as a Reel
caption = "🔥 New YouTube Short just dropped—watch now!"
cl.video_upload(filename, caption=caption)

print(f"✅ Posted {filename} to Instagram Reels")
