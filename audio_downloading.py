import os
import csv
import time
import json
import random
from yt_dlp import YoutubeDL

# === CONFIG ===
CSV_PATH = r"C:\Users\lenovo\Desktop\sem 5\IP\videos.csv"
OUTPUT_DIR = r"C:\Users\lenovo\Desktop\sem 5\IP\output"
EXPECTED_LICENSE = "Creative Commons Attribution license (reuse allowed)"
COOLDOWN_RANGE = (15, 25)
COMMON_LANGS = {"en", "es", "fr", "de", "hi"}
COOKIES_FILE = r"C:\Users\lenovo\Desktop\sem 5\IP\youtube_cookies.txt"
os.makedirs(OUTPUT_DIR, exist_ok=True)  


def has_common_language_subs(subtitles_dict):
    """Check if subtitles have any of the common languages."""
    if not subtitles_dict:
        return False
    available_langs = set(subtitles_dict.keys())
    return not COMMON_LANGS.isdisjoint(available_langs)


def process_video(video_url):
    base_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'noplaylist': True,
        'cookiefile': COOKIES_FILE
    }

    with YoutubeDL(base_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        license_text = info.get("license", "").strip()
        title = info.get("title", "untitled").replace("/", "_").replace("\\", "_")
        author = info.get("uploader", "unknown")
        description = info.get("description", "")
        duration_sec = info.get("duration", 0)
        duration_min = round(duration_sec / 60, 2)
        video_id = info.get("id")
        subtitles_info = info.get("subtitles", {})

        print(f"▶ License found: {license_text}")

        if license_text != EXPECTED_LICENSE:
            print("⛔ Skipping download: Not Creative Commons.")
            return

        # Decide if we should download subtitles
        download_subs = has_common_language_subs(subtitles_info)
        if download_subs:
            print("✅ Common language subtitles found — will download subs, metadata, and audio.")
        else:
            print("⚠️ No common language subtitles found — will only download metadata and audio.")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(OUTPUT_DIR, f'{title}_{video_id}.%(ext)s'),
            'writesubtitles': download_subs,
            'writeautomaticsub': download_subs,
            'subtitlesformat': 'json3',
            'quiet': False,
            'cookiefile': COOKIES_FILE,
            'postprocessors': [
                {   # Extract audio to MP3
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ]
        }

        with YoutubeDL(ydl_opts) as ydl_dl:
            ydl_dl.download([video_url])

        metadata = {
            "title": title,
            "author": author,
            "source": video_url,
            "license": "CC",  # Changed to generic CC
            "description": description.strip(),
            "duration_minutes": duration_min,
            "subtitles_in_common_lang": download_subs
        }

        meta_path = os.path.join(OUTPUT_DIR, f"{title}_{video_id}_metadata.json")
        with open(meta_path, 'w', encoding='utf-8') as out_json:
            json.dump(metadata, out_json, ensure_ascii=False, indent=2)

        print(f"📄 Metadata saved to: {meta_path}")


# === Main ===
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        video_url = row.get('link')
        if video_url:
            try:
                print(f"\n⏳ Processing video: {video_url}")
                process_video(video_url)
                cooldown = random.randint(*COOLDOWN_RANGE)
                print(f"⏸️ Cooling down for {cooldown} seconds...")
                time.sleep(cooldown)
            except Exception as e:
                print(f"❌ Error processing {video_url}: {e}")
