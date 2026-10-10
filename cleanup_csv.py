import os
import csv
from urllib.parse import urlparse, parse_qs

# ================== CONFIG ==================
# These paths should match your main.py configuration
CSV_PATH = r"C:\Users\lenovo\Desktop\sem 5\IP\videos.csv"
OUTPUT_DIR = r"C:\Users\lenovo\Desktop\sem 5\IP\output"
CSV_LINK_COLUMN = "link"
# ============================================

def get_video_id_from_url(url: str):
    """
    (Fast, No-Network) Extracts the YouTube video ID from a URL string.
    """
    if not url:
        return None
    try:
        parsed_url = urlparse(url)
        if "youtube.com" in parsed_url.hostname:
            if parsed_url.path == "/watch":
                return parse_qs(parsed_url.query).get("v", [None])[0]
            if parsed_url.path.startswith("/embed/"):
                return parsed_url.path.split("/")[2]
            if parsed_url.path.startswith("/v/"):
                return parsed_url.path.split("/")[2]
        elif "youtu.be" in parsed_url.hostname:
            return parsed_url.path[1:]
    except Exception:
        # Fallback for any parsing errors
        return None
    return None

def main():
    """
    Reads the CSV file, checks for existing downloaded files,
    and writes back only the rows for videos that are not yet downloaded.
    """
    try:
        with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            if CSV_LINK_COLUMN not in (fieldnames or []):
                print(f"❌ Error: CSV must contain a '{CSV_LINK_COLUMN}' column.")
                return
            all_rows = list(reader)
    except FileNotFoundError:
        print(f"❌ Error: CSV file not found at {CSV_PATH}")
        return
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    rows_to_keep = []
    removed_count = 0

    print(f"Found {len(all_rows)} rows in {os.path.basename(CSV_PATH)}. Checking for downloaded files...")

    for row in all_rows:
        url = (row.get(CSV_LINK_COLUMN) or "").strip()
        if not url:
            rows_to_keep.append(row)
            continue

        video_id = get_video_id_from_url(url)

        if video_id:
            mp3_path = os.path.join(OUTPUT_DIR, f"{video_id}.mp3")
            json_path = os.path.join(OUTPUT_DIR, f"{video_id}.json")

            if os.path.exists(mp3_path) and os.path.exists(json_path):
                # Files exist, so this row will be removed.
                removed_count += 1
            else:
                # Files are missing, so we keep the row.
                rows_to_keep.append(row)
        else:
            # Could not parse an ID, so keep the row to be safe.
            print(f"⚠️  Could not parse video ID from URL, keeping it: {url}")
            rows_to_keep.append(row)

    if removed_count > 0:
        try:
            with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows_to_keep)
            print(f"\n🎉 Successfully removed {removed_count} downloaded entries from the CSV.")
            print(f"{len(rows_to_keep)} entries remain.")
        except Exception as e:
            print(f"\n❌ Error writing to CSV file: {e}")
    else:
        print("\nNo downloaded entries found to remove. The CSV file is unchanged.")


if __name__ == "__main__":
    main()