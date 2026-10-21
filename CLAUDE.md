# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A publishable skills repo (no plugin manifest). Users install from it with `npx skills add https://github.com/sDaCoder/sda-study-stack --skill <name>`, which copies only `skills/<name>/`. Nothing inside a skill may depend on files outside its own folder.

It currently holds one skill, `youtube-lecture-visualizer`, which turns a YouTube study lecture into an interactive HTML slide deck. The pipeline is:

1. **Fetch:** get a timestamped transcript.
2. **Brief:** mix the transcript with web sources into `lecture-brief.md`, which lists the concepts and an interactive widget for each.
3. **Build:** build the deck by handing off to the external `frontend-slides` skill. That skill shows 3 style previews and the user picks one.

## Layout

- `skills/youtube-lecture-visualizer/references/troubleshooting.md`: setup without uv, plus the error → explanation table. It's loaded only when a fetch fails.
- `dev/evals/evals.json`: test prompts for the skill-creator eval loop. They're kept outside `skills/` so they don't ship with the skill.
- `examples/`: a sample deck linked from `README.md`.
- `lectures/`: output from local test runs of the skill. It's gitignored, so never commit it.

## Commands

```bash
# Fetch a transcript the way the skill does (uv installs the dependency from the script's PEP 723 header)
uv run skills/youtube-lecture-visualizer/scripts/fetch_transcript.py "<youtube_url>" out.txt [--english-only]

# Validate the skill's structure and frontmatter (skill-creator's validator)
uv run --with pyyaml python -m scripts.quick_validate <abs-path-to>/skills/youtube-lecture-visualizer   # run from the skill-creator directory
```

There's no test suite, linter or build step. The skill is checked by running the eval prompts in `dev/evals/evals.json` through the skill-creator workflow.

## Things that span several files

- **The fetch script's printed messages are an interface.** `references/troubleshooting.md` maps each exact line `fetch_transcript.py` prints (`Error: Transcripts are disabled…`, `An unexpected error occurred: <ExceptionName>: <reason>`, and so on) and each exit code (1 = couldn't fetch, 2 = bad URL or arguments, 3 = missing dependency) to what Claude tells the user. If you change a message or an exit code, update that table too.
- **Dependencies are declared twice:** in the script's PEP 723 header for `uv run`, and in `scripts/requirements.txt` for pip and venv. Keep them in step.
- **`youtube-transcript-api` 1.x API:** `YouTubeTranscriptApi().fetch(id)` / `.list(id)` and `FetchedTranscript.to_raw_data()`. The old static `get_transcript` no longer exists.
- **SKILL.md always refers to the script as `<skill-dir>/scripts/...`,** meaning the skill's absolute base directory, because users run the skill from their own folders. Lecture output goes to `lectures/<slug>/` in the current working directory.
- **SKILL.md sends every user decision through `AskUserQuestion`:** the missing link, slide density, style pick and recovery after a failed fetch. That keeps a whole run inside one session. Keep new decision points consistent with this.
- **`frontend-slides` is an external dependency.** It isn't vendored. SKILL.md checks `~/.claude/skills/` and `.claude/skills/` for it and installs it with `npx skills add https://github.com/zarazhangrui/frontend-slides --skill frontend-slides` if it's missing. Deck rules such as the fixed 1920×1080 stage, the inlined `viewport-base.css` and the 3 style previews come from that skill.
- **Deck widgets must not take over keyboard navigation.** The deck ignores keys while a slider or text input has focus. A focused button blocks only Space and Enter; arrow keys still change slides. The browser check found that blocking all keys on a focused button breaks navigation.
