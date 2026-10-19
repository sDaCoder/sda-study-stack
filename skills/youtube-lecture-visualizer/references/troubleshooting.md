# Troubleshooting the transcript fetch

Read this when `uv` isn't available, or when `scripts/fetch_transcript.py` exits non-zero.
`<skill-dir>` is the skill's base directory, as in SKILL.md.

## Contents

- [Setting up without uv](#setting-up-without-uv)
- [Explaining a failed fetch](#explaining-a-failed-fetch)
- [Offering a way forward](#offering-a-way-forward)

## Setting up without uv

The script needs Python 3.10+ and `youtube-transcript-api` (listed in `scripts/requirements.txt`). Set it up yourself rather than asking the user to.

1. Check `python3 --version` is 3.10 or newer, then install the dependency:

   ```bash
   python3 -m pip install -r <skill-dir>/scripts/requirements.txt
   ```

2. If pip refuses with "externally-managed-environment" (Homebrew and Debian Pythons do this), create a venv inside the skill folder and use its Python from then on:

   ```bash
   python3 -m venv <skill-dir>/.venv && <skill-dir>/.venv/bin/pip install -r <skill-dir>/scripts/requirements.txt
   <skill-dir>/.venv/bin/python <skill-dir>/scripts/fetch_transcript.py "<YOUTUBE_URL>" lectures/<slug>/transcript.txt
   ```

3. If there's neither uv nor Python 3.10+, tell the user what's missing. `curl -LsSf https://astral.sh/uv/install.sh | sh` installs uv, which brings its own Python. Ask with `AskUserQuestion` whether to run that installer for them, or to continue by pasting a transcript.

Don't reinstall on every run. Once a fetch has worked in this session, go straight to the command.

## Explaining a failed fetch

The script always prints a one-line message and exits non-zero: 1 = couldn't fetch, 2 = bad URL or arguments, 3 = dependency missing. Explain it to the user in plain language: what went wrong, the likely cause, and what can be done. Don't just paste the output, and don't silently move on.

| What you see | What to tell the user |
| --- | --- |
| `Error: Invalid YouTube URL: Could not extract Video ID.` (exit 2) | The link isn't a recognisable YouTube video URL (e.g. a channel, playlist-only or search link). Ask for the video's own link (`watch?v=…`, `youtu.be/…`, shorts or embed). |
| `Error: Transcripts are disabled for this video.` | The uploader turned off captions, so there's nothing to fetch. |
| `Error: No transcript found for the requested language.` | The video has no captions in any language, so even the translation fallback had nothing to use. |
| `An unexpected error occurred: RequestBlocked / IpBlocked / …too many requests` | YouTube is blocking transcript requests from this network (common on cloud/VPN IPs). Retrying later or from another network may help. |
| `An unexpected error occurred: VideoUnavailable / AgeRestricted / …private` | The video was removed, is private, or needs sign-in, so it can't be read. |
| `Error: youtube-transcript-api is not installed` (exit 3), `ModuleNotFoundError`, or a `uv` error | A dependency problem. Redo the setup (above, or `uv run` if uv exists), then retry once before reporting it. |
| Anything else | Quote the one-line message, say what you think it means, and say so if you're unsure. |

## Offering a way forward

Write the explanation as text, then in the same response call `AskUserQuestion` (header "Next step") to choose a way forward:

- **"Try a different link"**: the new URL goes in "Other"; rerun Stage 1.
- **"Paste the transcript or notes"**: the text goes in "Other"; save it to `lectures/<slug>/transcript.txt` and continue from Stage 2.
- **"Build from web resources"**: build the brief from web material about the same lecture (SKILL.md, Stage 2), with a clear note that the deck isn't based on the video's own words.

Leave out options that can't help. For example, after a blocked request, a different link from the same network will fail too.
