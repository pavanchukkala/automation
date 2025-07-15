```python
#!/usr/bin/env python3
import os
import tempfile
import sys
from googleapiclient.discovery import build
from pytube import YouTube
from instagrapi import Client

# ─── CONFIG (hard‑coded) ────────────────────────────────────────────────────
API_KEY    = 'AIzaSyB7KGpmU2JRQ80SQUoDeeqnSkgiu311VC8'
IG_USER    = 'kegth_group'
IG_PASS    = 'Kegth@2004'
CHANNEL_ID = 'UCjECts5K34yUPWAQ-QziZJA'
# Path for saving Instagram session (cookie jar)
SESSION_FN = os.path.expanduser('~/automation/ig_session.json')
# ────────────────────────────────────────────────────────────────────────────

def fetch_latest_short():
    yt = build('youtube', 'v3', developerKey=API_KEY)
    resp = yt.search().list(
        part='id,snippet',
        channelId=CHANNEL_ID,
        maxResults=1,
        order='date',
        type='video'
    ).execute()
    item = resp['items'][0]
    vid_id = item['id']['videoId']
    snip = item['snippet']
    return vid_id, snip.get('title', ''), snip.get('description', ''), snip.get('tags', [])


def download_video(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    yt = YouTube(url)
    # highest MP4 stream ≥ 720p
    stream = yt.streams.filter(file_extension='mp4', res__gte='720p').order_by('resolution').desc().first()
    if not stream:
        raise RuntimeError('No suitable MP4 stream found')
    return stream.download(output_path=tempfile.gettempdir(), filename='latest_short.mp4')


def get_ig_client():
    cl = Client()
    # reuse session if exists
    if os.path.isfile(SESSION_FN):
        try:
            cl.load_settings(SESSION_FN)
        except Exception:
            pass
    cl.login(IG_USER, IG_PASS)
    cl.dump_settings(SESSION_FN)
    return cl


def post_to_ig(video_path, caption):
    client = get_ig_client()
    client.clip_upload(video_path, caption)
    client.logout()


def main():
    try:
        vid_id, title, desc, tags = fetch_latest_short()
        video_path = download_video(vid_id)
        hashtags = ' '.join(f"#{tag.replace(' ', '')}" for tag in tags)
        caption = f"{title}\n\n{desc}\n\n{hashtags}"
        post_to_ig(video_path, caption)
        print(f"✅ Successfully posted video {vid_id}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```
