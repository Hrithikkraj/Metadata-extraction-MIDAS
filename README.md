# Metadata Extraction and Audio Downloading

This project provides Python utilities for building a local dataset from YouTube
video URLs. It can download audio, collect video metadata, extract available
manual subtitles/transcripts, check download completeness, remove completed URLs
from the input CSV, clean an output directory, and calculate the total duration
of downloaded MP3 files.

## Features

- Read YouTube URLs from `videos.csv`.
- Download audio as 192 kbps MP3 files.
- Save video metadata and available subtitle text as JSON.
- Support common subtitle languages such as English, Spanish, French, German,
  Hindi, Japanese, Chinese, Portuguese, Arabic, and Russian.
- Skip duplicate URLs and already completed downloads.
- Identify missing or extra output files.
- Remove completed downloads from the input CSV.
- Calculate the total duration of MP3 files.
- Perform a dry-run cleanup of files that are not part of valid audio/metadata
  pairs.

## Project structure

| File | Purpose |
| --- | --- |
| [`main.py`](./main.py) | Downloads YouTube audio, metadata, and manual subtitles. |
| [`audio_downloading.py`](./audio_downloading.py) | Alternative downloader that checks for a Creative Commons license before downloading. |
| [`check_file.py`](./check_file.py) | Validates that each URL has both an MP3 and JSON output. |
| [`cleanup_csv.py`](./cleanup_csv.py) | Removes completed video URLs from the input CSV. |
| [`time calculation.py`](./time%20calculation.py) | Calculates the total duration of MP3 files in a directory. |
| [`delete file script.py`](./delete%20file%20script.py) | Finds valid MP3/metadata pairs and previews unrelated files for deletion. |
| [`videos.csv`](./videos.csv) | Input file containing video URLs in a `link` column. |
| [`www.youtube.com_cookies.txt`](./www.youtube.com_cookies.txt) | Optional browser cookie export used by `yt-dlp`; do not commit real cookies. |

## Requirements

- Python 3.9 or newer
- FFmpeg available on `PATH` for MP3 extraction
- Python packages:
  - `yt-dlp`
  - `mutagen`

Install the Python dependencies with:

```bash
python -m pip install yt-dlp mutagen
```

Verify that FFmpeg is installed:

```bash
ffmpeg -version
```

## Input format

`videos.csv` must contain a column named `link`:

```csv
link
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
```

Blank rows are ignored. Duplicate URLs are removed by `main.py`.

## Configuration

The scripts currently use Windows paths defined near the top of each file.
Before running them on another machine, update the following values:

- `CSV_PATH`: location of the input CSV file
- `OUTPUT_DIR`: directory where audio and JSON files are saved
- `COOKIE_FILE` or `COOKIES_FILE`: optional cookies file
- `COOLDOWN_RANGE`: delay between downloads

For easier portability, use paths relative to the project directory or replace
the hard-coded paths with paths appropriate for your system.

## Usage

### Download audio and metadata

```bash
python main.py
```

For each successfully processed video, the main downloader creates files
similar to:

```text
output/
├── VIDEO_ID.mp3
└── VIDEO_ID.json
```

The JSON file contains fields such as the title, uploader, upload date,
duration, view count, source URL, local MP3 filename, and transcription text
grouped by language.

### Validate downloads

```bash
python check_file.py
```

This reports completed, missing, and extra files. It then rewrites the CSV to
keep only URLs whose MP3 or JSON output is missing. Keep a backup of
`videos.csv` if the original list must be preserved.

### Remove completed URLs from the CSV

```bash
python cleanup_csv.py
```

This performs a similar completion check and removes rows for videos that
already have both expected output files.

### Use the Creative Commons downloader

```bash
python audio_downloading.py
```

This is an alternative workflow that only downloads videos whose metadata
matches the configured Creative Commons license. It also writes a separate
`*_metadata.json` file.

### Calculate total audio duration

Update `directory_to_scan` in `time calculation.py`, then run:

```bash
python "time calculation.py"
```

### Preview output cleanup

Update `OUTPUT_DIR` in `delete file script.py`, then run:

```bash
python "delete file script.py"
```

The script runs in dry-run mode by default and does not delete files. Review
the proposed list carefully before changing `dry_run=True` to `dry_run=False`.

## Cookies and security

Cookies can grant access to an account. Never commit a real cookie export,
share it publicly, or include it in issue reports. The repository contains an
empty cookie file as a placeholder. If cookies are required, create a local
copy and keep it ignored by Git.

Only download content that you are authorized to access and process. Follow
YouTube's Terms of Service, applicable copyright law, and the license
conditions of each video.

## Troubleshooting

- **`ModuleNotFoundError`**: install the dependencies with
  `python -m pip install yt-dlp mutagen`.
- **MP3 conversion fails**: install FFmpeg and ensure its executable directory
  is on `PATH`.
- **CSV column error**: confirm that the first row contains exactly `link`.
- **Cookie errors**: verify the cookie file path and export a fresh cookie file
  locally when necessary.
- **Files are reported as missing**: confirm that `OUTPUT_DIR` is the same in
  the downloader and validation scripts.

## License

No license file is currently included. Add a license before distributing or
reusing this project publicly.
