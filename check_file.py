import os
import csv
import re

# === CONFIG ===
CSV_PATH = r"C:\Users\lenovo\Desktop\sem 5\IP\videos.csv"
OUTPUT_DIR = r"C:\Users\lenovo\Desktop\sem 5\IP\output"
CSV_LINK_COLUMN = "link"
# ==============

def extract_video_id(url: str) -> str:
    """Extracts YouTube video ID from URL."""
    m = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", url)
    if m:
        return m.group(1)
    m = re.search(r"v=([A-Za-z0-9_-]{11})", url)
    if m:
        return m.group(1)
    m = re.search(r"embed/([A-Za-z0-9_-]{11})", url)
    if m:
        return m.group(1)
    return None

def read_csv_rows(csv_path, col):
    """Reads rows and extracts video IDs."""
    rows = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if col not in (reader.fieldnames or []):
            raise ValueError(f"CSV must contain '{col}' column, found {reader.fieldnames}")
        for row in reader:
            url = (row.get(col) or "").strip()
            if not url:
                continue
            vid = extract_video_id(url)
            if vid:
                rows.append({"id": vid, "url": url})
    return rows

def validate_outputs(csv_rows, outdir):
    existing = set(os.path.splitext(f)[0] for f in os.listdir(outdir))
    ok, missing = [], []
    for row in csv_rows:
        vid = row["id"]
        has_mp3 = os.path.exists(os.path.join(outdir, f"{vid}.mp3"))
        has_json = os.path.exists(os.path.join(outdir, f"{vid}.json"))
        if has_mp3 and has_json:
            ok.append(row)
        else:
            missing.append(row)
    extras = existing - set(r["id"] for r in csv_rows)
    return ok, missing, extras

def overwrite_csv(csv_path, col, rows):
    """Rewrite CSV with only missing rows."""
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[col])
        writer.writeheader()
        for r in rows:
            writer.writerow({col: r["url"]})

def main():
    try:
        csv_rows = read_csv_rows(CSV_PATH, CSV_LINK_COLUMN)
    except Exception as e:
        print(f"❌ Failed to read CSV: {e}")
        return

    print(f"Found {len(csv_rows)} unique video IDs in CSV.")

    ok, missing, extras = validate_outputs(csv_rows, OUTPUT_DIR)

    print(f"\n✅ OK: {len(ok)} downloaded")
    print(f"❌ Missing: {len(missing)}")
    print(f"⚠️ Extra files in output: {len(extras)}")

    if missing:
        print("\nMissing IDs:")
        for r in missing:
            print(" -", r["id"])

    if extras:
        print("\nExtra files:")
        for vid in extras:
            print(" -", vid)

    # Update CSV to only keep missing
    overwrite_csv(CSV_PATH, CSV_LINK_COLUMN, missing)
    print(f"\n✏️ Updated {CSV_PATH} → kept only {len(missing)} missing rows.")

if __name__ == "__main__":
    main()
