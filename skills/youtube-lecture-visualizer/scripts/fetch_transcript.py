# /// script
# requires-python = ">=3.10"
# dependencies = ["youtube-transcript-api>=1.2.4"]
# ///
"""Fetch a YouTube transcript and save it as timestamped lines.

Usage:
    uv run fetch_transcript.py <youtube_url> <output.txt> [--english-only]

Writes one line per caption snippet, e.g. "[03:44] say you want to predict housing prices".
English captions are preferred. If there are none, the first available track is used,
machine-translated to English when YouTube allows it (disable with --english-only).

Exit codes: 0 = saved, 1 = transcript could not be fetched, 2 = bad URL or arguments,
3 = dependency missing. Every failure prints a one-line "Error: ..." message to stdout.
"""
import re
import sys

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
except ImportError:
    print("Error: youtube-transcript-api is not installed. "
          "Run with `uv run` or `pip install -r requirements.txt`.")
    sys.exit(3)


def extract_video_id(url: str) -> str:
    """Extracts the 11-character YouTube video ID from various URL formats."""
    pattern = r'(?:v=|\/shorts\/|\/embed\/|\/v\/|youtu\.be\/|\/watch\?v=|\&v=)([^#\&\?]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL: Could not extract Video ID.")


def _short(e: Exception) -> str:
    """One-line error: the library's 'most likely caused by' reason, else the first line."""
    lines = [l.strip() for l in str(e).splitlines() if l.strip()]
    for i, line in enumerate(lines):
        if line.endswith("caused by:") and i + 1 < len(lines):
            return f"{type(e).__name__}: {lines[i + 1]}"
    return f"{type(e).__name__}: {lines[0] if lines else ''}"


def get_transcript(video_id: str, allow_fallback: bool = True):
    """Return (snippets, language_note) or (None, None) after printing an error.

    snippets is a list of {text, start, duration} dicts.
    """
    ytt_api = YouTubeTranscriptApi()

    try:
        fetched_transcript = ytt_api.fetch(video_id)
        return fetched_transcript.to_raw_data(), "English"

    except TranscriptsDisabled:
        print("Error: Transcripts are disabled for this video.")
    except NoTranscriptFound:
        if not allow_fallback:
            print("Error: No transcript found for the requested language.")
            return None, None
        return _fetch_any_language(ytt_api, video_id)
    except Exception as e:
        print(f"An unexpected error occurred: {_short(e)}")
    return None, None


def _fetch_any_language(ytt_api, video_id: str):
    """No English track: take the first available one, translated to English if possible."""
    try:
        transcript = next(iter(ytt_api.list(video_id)))
        source = transcript.language
        if transcript.is_translatable:
            transcript = transcript.translate("en")
            note = f"translated to English from {source}"
        else:
            note = f"{source} (not translatable; the deck must still be written in English)"
        return transcript.fetch().to_raw_data(), note
    except StopIteration:
        print("Error: No transcript found for the requested language.")
    except Exception as e:
        print(f"An unexpected error occurred: {_short(e)}")
    return None, None


def write_transcript(snippets, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for s in snippets:
            t = int(s["start"])
            f.write(f"[{t // 60:02d}:{t % 60:02d}] {s['text']}\n")


def main(argv) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2:
        print("Usage: fetch_transcript.py <youtube_url> <output.txt> [--english-only]")
        return 2
    url, out_path = args

    try:
        video_id = extract_video_id(url)
    except ValueError as e:
        print(f"Error: {e}")
        return 2

    snippets, language = get_transcript(video_id, allow_fallback="--english-only" not in argv)
    if not snippets:
        return 1

    write_transcript(snippets, out_path)
    end = snippets[-1]["start"] + snippets[-1].get("duration", 0)
    print(f"{len(snippets)} snippets, {end / 60:.1f} min, language: {language} -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
