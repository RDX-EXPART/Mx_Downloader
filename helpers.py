import re
import asyncio
import aiohttp
import os
import json
import typing
import subprocess
from concurrent.futures import ThreadPoolExecutor

# ──────────────────────────────────────────────
# GLOBAL THREAD POOL EXECUTOR
# All CPU/IO-bound work (yt-dlp, uploads) runs here so the event loop
# is never blocked and every user gets a real OS thread.
# ──────────────────────────────────────────────

_executor = ThreadPoolExecutor(max_workers=16)   # raise if you have more cores

# ──────────────────────────────────────────────
# SPLIT / THUMBNAIL CONSTANTS
# ──────────────────────────────────────────────

MAX_UPLOAD_SIZE_BYTES = int(1.85 * 1024 * 1024 * 1024)   # 1.85 GB
SPLIT_PART_SIZE      = MAX_UPLOAD_SIZE_BYTES              # each part ≤ 1.85 GB


# ──────────────────────────────────────────────
# URL VALIDATOR
# ──────────────────────────────────────────────

def is_mxplayer_url(url: str) -> bool:
    return "mxplayer.in" in url or "mxplay.com" in url


# ──────────────────────────────────────────────
# TITLE EXTRACTOR FROM URL  (NEW)
# e.g. https://www.mxplayer.in/movie/watch-operation-red-sea-movie-online-…
#   → "Operation Red Sea"
# ──────────────────────────────────────────────

def extract_title_from_url(url: str) -> str | None:
    """
    Try to parse a human-readable title from an MX Player URL slug.

    Strategy:
      1. Grab the last path segment before any query string.
      2. Strip common filler words (watch, movie, online, web-series, episode, …).
      3. Title-case what remains.

    Returns None if nothing useful can be extracted.
    """
    try:
        # Remove query string and fragment
        path = url.split("?")[0].split("#")[0]
        # Last non-empty path segment
        slug = [s for s in path.split("/") if s][-1]

        # Remove trailing hex hash (e.g. -b9d5d1f3980ecbb95db74fd12f4960e5)
        slug = re.sub(r'-[0-9a-f]{20,}$', '', slug)

        # Words to strip out (filler / navigation words)
        STOPWORDS = {
            "watch", "movie", "online", "free", "hd", "stream", "streaming",
            "web", "series", "webseries", "episode", "full", "official",
            "trailer", "video", "in", "on", "the", "a", "an",
        }

        words = slug.replace("-", " ").replace("_", " ").split()
        cleaned = [w for w in words if w.lower() not in STOPWORDS]

        if not cleaned:
            return None

        title = " ".join(cleaned).title()
        return title if len(title) >= 3 else None

    except Exception:
        return None


# ──────────────────────────────────────────────
# MX PLAYER API
# ──────────────────────────────────────────────

async def mx_player_api(url: str) -> dict | None:
    api_url = f"https://ott.dkbotzpro.in/mxplayer?url={url}"
    for _ in range(3):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        # ── AUTO-FILL title from URL when API returns None ──
                        if not data.get("show_title"):
                            data["show_title"] = extract_title_from_url(url) or "Unknown"
                        return data
        except Exception:
            pass
        await asyncio.sleep(1)
    return None


# ──────────────────────────────────────────────
# YT-DLP FORMAT PARSER
# ──────────────────────────────────────────────

async def get_available_formats(download_url: str) -> dict:
    """
    Fetches all available formats using yt-dlp and returns:
    {
      "video_formats": [...],
      "audio_formats": [...]
    }
    Runs yt-dlp in the executor so it never blocks the event loop.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, _get_formats_sync, download_url)


def _get_formats_sync(download_url: str) -> dict:
    """Blocking yt-dlp call — always invoked from the executor."""
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-warnings",
        download_url
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        if result.returncode != 0:
            return {"video_formats": [], "audio_formats": []}

        data = json.loads(result.stdout.decode())
        formats = data.get("formats", [])

        video_formats = []
        audio_formats = []

        for fmt in formats:
            format_id = fmt.get("format_id", "")
            ext = fmt.get("ext", "")

            if fmt.get("vcodec") != "none" and fmt.get("height"):
                height = fmt.get("height", 0)
                width = fmt.get("width", 0)
                fps = fmt.get("fps", 0)
                filesize = fmt.get("filesize") or fmt.get("filesize_approx", 0)

                quality_label = f"{height}p"
                if fps and fps > 30:
                    quality_label += f"{int(fps)}"

                resolution = f"{width}x{height}" if width else f"{height}p"
                size_mb = round(filesize / (1024 * 1024), 1) if filesize else 0
                size_str = f" ({size_mb} MB)" if size_mb else ""
                label = f"🎬 {quality_label} - {resolution}{size_str} - {ext}"

                video_formats.append({
                    "format_id": format_id,
                    "label": label,
                    "quality": quality_label,
                    "resolution": resolution,
                    "height": height,
                    "ext": ext,
                    "filesize": filesize,
                    "type": "video"
                })

            elif fmt.get("acodec") != "none" and fmt.get("vcodec") == "none":
                abr = fmt.get("abr", 0)
                language = fmt.get("language", "") or fmt.get("lang", "")
                filesize = fmt.get("filesize") or fmt.get("filesize_approx", 0)

                lang_label = ""
                if language:
                    lang_map = {
                        "en": "English", "hi": "Hindi", "ta": "Tamil",
                        "te": "Telugu", "ml": "Malayalam", "kn": "Kannada",
                        "bn": "Bengali", "mr": "Marathi", "pa": "Punjabi",
                        "gu": "Gujarati",
                    }
                    lang_label = f" - {lang_map.get(language, language.upper())}"

                bitrate_label = f"{int(abr)}kbps" if abr else "Unknown"
                size_mb = round(filesize / (1024 * 1024), 1) if filesize else 0
                size_str = f" ({size_mb} MB)" if size_mb else ""
                label = f"🎵 {bitrate_label}{lang_label}{size_str} - {ext}"

                audio_formats.append({
                    "format_id": format_id,
                    "label": label,
                    "bitrate": int(abr) if abr else 0,
                    "language": language,
                    "ext": ext,
                    "filesize": filesize,
                    "type": "audio"
                })

        video_formats.sort(key=lambda x: x["height"], reverse=True)
        audio_formats.sort(key=lambda x: x["bitrate"], reverse=True)

        return {"video_formats": video_formats, "audio_formats": audio_formats}

    except Exception as e:
        print(f"Error getting formats: {e}")
        return {"video_formats": [], "audio_formats": []}


# ──────────────────────────────────────────────
# FILENAME SANITIZER
# ──────────────────────────────────────────────

def sanitize_filename(name: str | None, max_len: int = 80) -> str:
    """
    Strip characters that are unsafe in filenames / yt-dlp output paths.
    Accepts None safely — returns 'Untitled' instead of crashing.
    """
    if not name:
        return "Untitled"
    name = str(name)
    name = re.sub(r'[^\w\-.]', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    return name[:max_len] if name else "Untitled"


# ──────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────

DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "/tmp")

# Minimum seconds between Telegram edits (avoids flood-wait).
# Progress values are buffered internally and always shown smoothly.
_TELEGRAM_THROTTLE = 2.0   # seconds between actual message edits


# ──────────────────────────────────────────────
# SMOOTH PROGRESS WRAPPER
# ──────────────────────────────────────────────

class SmoothProgress:
    """
    Collects every 0.1 % increment from yt-dlp and forwards them
    to the Telegram callback at most once per _TELEGRAM_THROTTLE seconds
    (plus always the final 100 %).

    This way the bar visually counts every 0.1 % step in the log / internal
    state, but we never flood Telegram's rate-limit.
    """

    def __init__(self, callback, throttle: float = _TELEGRAM_THROTTLE):
        self._cb = callback
        self._throttle = throttle
        self._last_sent_time = 0.0
        self._last_sent_pct = -1.0
        self._lock = asyncio.Lock()

    async def update(self, percent: float, line: str = ""):
        """Call this for every parsed progress value (including 0.1 % steps)."""
        import time
        now = time.time()
        async with self._lock:
            is_final = percent >= 100.0
            elapsed = now - self._last_sent_time
            moved = percent - self._last_sent_pct

            # Send update if: final OR throttle window passed AND moved ≥ 0.1 %
            if is_final or (elapsed >= self._throttle and moved >= 0.1):
                self._last_sent_time = now
                self._last_sent_pct = percent
                await self._cb(percent, line)


# ──────────────────────────────────────────────
# YT-DLP PROGRESS PARSER  (0.1 % granularity)
# ──────────────────────────────────────────────

def _parse_ytdlp_progress(line: str) -> float | None:
    """Extract download percent from a yt-dlp output line (0.1 % granularity)."""
    m = re.search(r'\[download\]\s+(\d{1,3}(?:\.\d+)?)\s*%', line)
    if m:
        return min(float(m.group(1)), 100.0)
    return None


# ──────────────────────────────────────────────
# FFMPEG THUMBNAIL GENERATOR
# Captures a screenshot at 5 % of video duration for a proper thumbnail.
# Falls back to the remote thumb URL if ffmpeg fails.
# ──────────────────────────────────────────────

def generate_thumbnail(video_path: str, fallback_thumb: str | None = None) -> str | None:
    """
    Generate a JPEG thumbnail from the video using ffmpeg.

    Seeks to 5 % of the total duration so the frame is never black (intro).
    Returns the path to the generated .jpg, or fallback_thumb on failure.
    """
    thumb_path = video_path + "_thumb.jpg"
    try:
        # Get video duration in seconds
        probe = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                video_path,
            ],
            capture_output=True, text=True, timeout=30
        )
        duration = float(probe.stdout.strip() or 0)
        seek_time = max(5, duration * 0.05)   # at least 5 s, otherwise 5 %

        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-ss", str(seek_time),
                "-i", video_path,
                "-vframes", "1",
                "-q:v", "2",                  # high quality JPEG
                "-vf", "scale=320:-1",        # Telegram thumb: 320 px wide
                thumb_path,
            ],
            capture_output=True, timeout=60
        )
        if result.returncode == 0 and os.path.exists(thumb_path):
            return thumb_path
    except Exception as e:
        print(f"[thumbnail] ffmpeg error: {e}")

    # ffmpeg failed — try downloading the remote thumbnail
    if fallback_thumb:
        try:
            import urllib.request
            urllib.request.urlretrieve(fallback_thumb, thumb_path)
            if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
                return thumb_path
        except Exception:
            pass

    return None


# ──────────────────────────────────────────────
# FILE SPLITTER  (for files > 1.85 GB)
# Splits a video into byte-exact parts using ffmpeg segment muxer.
# Returns a list of part paths in order.
# ──────────────────────────────────────────────

def split_video_file(file_path: str, max_bytes: int = SPLIT_PART_SIZE) -> list[str]:
    """
    Split *file_path* into parts each ≤ max_bytes using ffmpeg's
    segment muxer (stream-copy — no re-encoding, so it is fast).

    Part files are named:  <base>_part001.mp4, _part002.mp4, …
    Returns an ordered list of part paths.
    Raises RuntimeError if splitting fails.
    """
    base, ext = os.path.splitext(file_path)
    ext = ext or ".mp4"
    pattern = f"{base}_part%03d{ext}"

    # Estimate target duration per part from bitrate
    probe = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration,bit_rate",
            "-of", "default=noprint_wrappers=1",
            file_path,
        ],
        capture_output=True, text=True, timeout=60
    )
    duration = 0.0
    bitrate  = 0

    for line in probe.stdout.splitlines():
        if line.startswith("duration="):
            try:
                duration = float(line.split("=", 1)[1])
            except ValueError:
                pass
        elif line.startswith("bit_rate="):
            try:
                bitrate = int(line.split("=", 1)[1])
            except ValueError:
                pass

    if not bitrate or not duration:
        # Fallback: derive bitrate from file size
        file_bytes = os.path.getsize(file_path)
        bitrate    = int((file_bytes * 8) / duration) if duration else 0

    if not bitrate:
        raise RuntimeError("Could not determine video bitrate for splitting.")

    # seconds per part so each part ≈ max_bytes
    segment_time = int((max_bytes * 8) / bitrate)
    segment_time = max(segment_time, 60)   # at least 60 s per part

    result = subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", file_path,
            "-c", "copy",
            "-map", "0",
            "-f", "segment",
            "-segment_time", str(segment_time),
            "-reset_timestamps", "1",
            "-avoid_negative_ts", "1",
            pattern,
        ],
        capture_output=True, timeout=7200   # 2 h max for huge files
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg split failed:\n{result.stderr.decode()[-1000:]}"
        )

    # Collect parts in order
    dir_search = os.path.dirname(file_path) or "."
    ext_escaped = re.escape(ext)
    parts = sorted(
        p for p in os.listdir(dir_search)
        if re.match(r".+_part\d+" + ext_escaped + r"$", p)
    )

    full_parts = [os.path.join(dir_search, p) for p in parts]

    if not full_parts:
        # Glob more broadly
        import glob
        full_parts = sorted(glob.glob(f"{base}_part*{ext}"))

    if not full_parts:
        raise RuntimeError("Splitting produced no output files.")

    return full_parts


# ──────────────────────────────────────────────
# DOWNLOADER — YT-DLP  (executor-based, no semaphore blocking)
# ──────────────────────────────────────────────

async def download_with_ytdlp(
    download_url: str,
    video_format_id: str,
    audio_format_ids: list,
    output_name: str,
    progress_callback=None,
    user_id: int = 0,
) -> str | None:
    """
    Download video (+ optional audio tracks) using yt-dlp.
    Runs entirely in the ThreadPoolExecutor so multiple users download
    simultaneously without any one blocking another.
    Returns the output file path on success, None on failure.
    """
    safe_name = sanitize_filename(output_name)
    out_path = os.path.join(DOWNLOAD_DIR, safe_name)

    if audio_format_ids:
        format_str = f"{video_format_id}+" + "+".join(audio_format_ids)
    else:
        format_str = f"{video_format_id}+bestaudio"

    cmd = [
        "yt-dlp",
        "-f", format_str,
        "--merge-output-format", "mp4",
        "-o", f"{out_path}.%(ext)s",
        "--no-warnings",
        "--no-playlist",
        "--concurrent-fragments", "4",
        "--newline",          # ← emit progress on every line (0.1 % steps)
        download_url,
    ]

    loop = asyncio.get_event_loop()
    smooth = SmoothProgress(progress_callback) if progress_callback else None

    def _run():
        """Blocking subprocess — runs inside the executor thread."""
        with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            for line in proc.stdout:
                line = line.strip()
                if not line:
                    continue
                if smooth:
                    pct = _parse_ytdlp_progress(line)
                    if pct is not None:
                        # Schedule coroutine on the event loop from this thread
                        asyncio.run_coroutine_threadsafe(
                            smooth.update(pct, line), loop
                        ).result()   # wait so we don't swamp the queue
            proc.wait()

    await loop.run_in_executor(_executor, _run)

    # Final 100 % update
    if smooth:
        await smooth.update(100.0, "[download] 100%")

    # Locate output file
    if os.path.exists(f"{out_path}.mp4"):
        return f"{out_path}.mp4"
    for ext in [".mkv", ".webm", ".mp4"]:
        if os.path.exists(f"{out_path}{ext}"):
            return f"{out_path}{ext}"
    for fname in os.listdir(DOWNLOAD_DIR):
        if fname.startswith(safe_name):
            return os.path.join(DOWNLOAD_DIR, fname)
    return None


async def download_audio_only(
    download_url: str,
    audio_format_ids: list,
    output_name: str,
    progress_callback=None,
    user_id: int = 0,
) -> str | None:
    """
    Download audio-only using yt-dlp.
    Runs entirely in the ThreadPoolExecutor (same as video downloader).
    Returns the output file path on success, None on failure.
    """
    safe_name = sanitize_filename(output_name)
    out_path = os.path.join(DOWNLOAD_DIR, safe_name)

    if len(audio_format_ids) > 1:
        format_str = "+".join(audio_format_ids)
    else:
        format_str = audio_format_ids[0] if audio_format_ids else "bestaudio"

    cmd = [
        "yt-dlp",
        "-f", format_str,
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", f"{out_path}.%(ext)s",
        "--no-warnings",
        "--no-playlist",
        "--concurrent-fragments", "4",
        "--newline",          # ← emit progress on every line (0.1 % steps)
        download_url,
    ]

    loop = asyncio.get_event_loop()
    smooth = SmoothProgress(progress_callback) if progress_callback else None

    def _run():
        with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            for line in proc.stdout:
                line = line.strip()
                if not line:
                    continue
                if smooth:
                    pct = _parse_ytdlp_progress(line)
                    if pct is not None:
                        asyncio.run_coroutine_threadsafe(
                            smooth.update(pct, line), loop
                        ).result()
            proc.wait()

    await loop.run_in_executor(_executor, _run)

    if smooth:
        await smooth.update(100.0, "[download] 100%")

    if os.path.exists(f"{out_path}.mp3"):
        return f"{out_path}.mp3"
    for ext in [".mp3", ".m4a", ".opus", ".ogg"]:
        if os.path.exists(f"{out_path}{ext}"):
            return f"{out_path}{ext}"
    for fname in os.listdir(DOWNLOAD_DIR):
        if fname.startswith(safe_name):
            return os.path.join(DOWNLOAD_DIR, fname)
    return None
