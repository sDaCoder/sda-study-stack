---
name: youtube-lecture-visualizer
description: Turn a YouTube study lecture into an interactive HTML presentation that makes the concepts visual — fetches the transcript, extracts the concepts, designs a hands-on visualization for each one (sliders, step-through animations, clickable diagrams, quizzes), then builds the deck with the frontend-slides skill after showing style previews. Use this whenever the user shares a YouTube link to a lecture, tutorial, course video, or class recording and wants notes, a summary, slides, a visual explainer, study material, or help understanding it — even if they don't say "presentation" or "visualize" (e.g. "help me understand this video", "make study material from this lecture", "explain this Andrew Ng video visually").
---

# YouTube Lecture Visualizer

The goal is not a summary of the video. It is a deck where a learner *plays with* each idea from the lecture and sees it click — the kind of visual a great teacher would draw on the whiteboard, made interactive. A transcript only gives you words; your job is to recover the mental pictures the lecturer was trying to build and make them tangible.

The pipeline has three stages:

1. **Fetch** the transcript with this skill's own script, `scripts/fetch_transcript.py`.
2. **Understand & design** — combine the transcript with supporting material from the web into a lecture brief: concepts, their order, and a concrete interactive visualization for each.
3. **Build** — hand the brief to the `frontend-slides` skill, which shows the user style previews, lets them pick, and generates the deck.

Keep all files for one lecture together in `lectures/<slug>/` in the current working directory (slug = short kebab-case version of the lecture title, e.g. `lectures/supervised-learning-intro/`).

Throughout this file, `<skill-dir>` means this skill's base directory: the absolute path shown as "Base directory for this skill" when the skill loads. Always call the script by that absolute path, because the user's working directory is usually not the skill folder.

---

## Before you start: get the lecture link

If the skill was invoked with no input, or the message has no YouTube URL, don't guess and don't pick a video yourself. Ask for the link **with the `AskUserQuestion` tool**, not with a plain-text question that ends your turn. The prompt pane collects the answer and hands it back in the same response, so the pipeline carries straight on into Stage 1 without the user having to start a new message.

`AskUserQuestion` needs 2–4 options, and it always adds an "Other" choice with a free-text box, which is where the URL goes. Ask both questions in a single call:

```yaml
questions:
  - question: "Which YouTube lecture should I turn into an interactive deck? Choose 'Other' and paste the video link."
    header: "Lecture"
    multiSelect: false
    options:
      - label: "I'll paste a YouTube link"
        description: "Choose 'Other' below and paste the URL (watch?v=…, youtu.be/…, shorts or embed)."
      - label: "I'll paste a transcript instead"
        description: "No usable link. Choose 'Other' and paste the transcript or your notes."
  - question: "What should the visuals focus on?"
    header: "Focus"
    multiSelect: false
    options:
      - label: "Whole lecture, evenly (Recommended)"
        description: "One interactive visual per core concept."
      - label: "The parts I find hard"
        description: "Choose 'Other' and name them; those get the richest widgets."
```

Read the answer:

- **A URL in the "Other" text:** continue to Stage 1 with it.
- **Pasted transcript or notes:** save them to `lectures/<slug>/transcript.txt` and skip to Stage 2.
- **An option label with no URL or text attached** (the user picked an option instead of typing): ask once more with `AskUserQuestion`, saying the link needs to go in the "Other" box.

Use the same tool for every other decision in this pipeline: recovery choices after a failed fetch (see references/troubleshooting.md), and anything else you need from the user mid-run. That keeps the whole run inside one request/response session.

---

## Stage 1: Fetch the transcript

The skill fetches transcripts with its own script, `<skill-dir>/scripts/fetch_transcript.py`. It needs Python 3.10+ and `youtube-transcript-api`, and you take care of that yourself rather than asking the user to.

**Check for uv** with `uv --version`. If it's there, nothing else is needed: the script declares its dependency in an inline metadata header (PEP 723), so `uv run` installs it into a cached, isolated environment on first use, without touching the user's project. If uv is missing, follow "Setting up without uv" in [references/troubleshooting.md](references/troubleshooting.md) (pip, or a venv inside the skill folder).

Create `lectures/<slug>/` first. If you don't know the title yet, use the video ID as a temporary slug and rename later, or get the title from `https://www.youtube.com/oembed?format=json&url=<YOUTUBE_URL>`. Then run:

```bash
uv run <skill-dir>/scripts/fetch_transcript.py "<YOUTUBE_URL>" lectures/<slug>/transcript.txt
```

On success it prints one line, e.g. `168 snippets, 6.9 min, language: English -> lectures/<slug>/transcript.txt`, and writes one `[mm:ss] text` line per caption. It prefers English captions. If a video has none, it falls back on its own to the first available track, machine-translated to English, and the `language:` part says so (e.g. `translated to English from Hindi`). Write the deck in English either way, and tell the user when the transcript was translated.

**If it fails** (non-zero exit with a one-line message), explain the error to the user in plain language, then offer a way forward with `AskUserQuestion`. [references/troubleshooting.md](references/troubleshooting.md) maps each message to its explanation and lists the recovery options. Read it whenever a fetch fails.

Timestamps matter: keep them, because every concept in the final deck links back to the moment it's taught (`https://www.youtube.com/watch?v=<ID>&t=<seconds>s`).

---

## Stage 2: Understand the lecture and design the visuals

Read the **entire** transcript before writing anything. Auto-captions have no punctuation and mangle technical terms (e.g. "grade in descent" → gradient descent, "sigmoid" → "sig Lloyd"); repair these silently using context.

### Mix in resources from the web

A transcript loses everything the lecturer drew or wrote on the board: equations, diagrams, slide titles. So after reading it, use WebSearch/WebFetch to find supporting material for the same lecture and topic. Get the title and channel from oEmbed first (`https://www.youtube.com/oembed?format=json&url=<URL>`), then look for:

- the course's official lecture notes, slides or syllabus page (e.g. CS229 notes for an Andrew Ng lecture, the 3Blue1Brown lesson page for a 3b1b video);
- the exact formulas, notation and definitions behind what the lecturer says aloud;
- a reputable reference (textbook chapter, university notes, Wikipedia) for terms the transcript garbles or skips over.

Use these to **fill gaps and confirm details**, while the transcript stays the backbone. Keep the lecture's own order, examples and emphasis. Where a source adds something important that the video doesn't cover, put it in clearly marked "Going further" notes rather than mixing it into the lecturer's flow. If a source disagrees with the lecture, follow the lecture and mention the difference. List the sources you used under a `## Sources` heading in the brief, so the deck can credit them. Two to four good sources are enough. Don't spend long searching if the transcript is already clear.

If there was no transcript (Stage 1 failed and the user chose this route), these sources become the main content. Say so at the top of the brief and on the deck's title slide, and don't add `▶ Watch mm:ss` timestamps you can't verify.

Then write `lectures/<slug>/lecture-brief.md`. This brief is the single source of content for the deck, so make it complete enough that someone who never saw the video could build the slides from it. Use this structure:

```markdown
# <Lecture title>
Source: <URL> · <channel if known> · <duration>

## Learning objectives
3–5 things the learner should be able to do/explain afterwards.

## Concept flow
One line on how the concepts build on each other (the narrative arc).

## Concepts
### 1. <Concept name>  [mm:ss]
- **Core idea:** 1–2 sentences, in plain language.
- **Lecturer's example:** the specific example/analogy/numbers used in the video.
- **Common confusion:** what learners typically get wrong here (only if real).
- **Interactive visual:** <widget type> — what the learner manipulates, what they see change, and what insight that change reveals. Include concrete data/values to use.
- **Slide text:** the few words that go on screen.

### 2. ...

## Check your understanding
3–6 quiz questions (multiple choice or predict-the-outcome) with answers and one-line explanations. Prefer questions that test the visual intuition, not recall of wording.

## Recap
The 3–5 takeaways, each one line.

## Sources
The video, plus each web resource used (title + URL) and what it contributed.
```

### Designing the interactive visuals

This is where the deck earns its value, so spend real thought here. For each concept ask: *what would I draw on a whiteboard to explain this, and what would I want the learner to poke at?* Pick the interaction that exposes the concept's essential mechanism:

| Concept shape | Interaction that tends to work |
| --- | --- |
| Relationship between quantities (functions, trade-offs, parameters) | Slider(s) driving a live SVG/canvas plot; show the number updating |
| Process / algorithm / pipeline | Step-through animation with Next/Prev, highlighting the active step and state |
| Input → output mapping | Pick an input (buttons/cards) and watch it flow to its output |
| Categories / taxonomy | Click-to-sort or drag items into buckets with instant feedback |
| Comparison of two approaches | Toggle or split view on the same data |
| Hierarchy / structure | Expandable tree or click-to-reveal layers |
| Formula | Formula with each term hoverable/highlighted, linked to a slider-driven picture |
| Sequence in time | Scrubbable timeline |

Guidelines that keep the visuals honest and useful:

- **Faithful to the lecture.** Use the lecturer's own examples and numbers where they exist. If you add a supporting example the video didn't use, keep it consistent with what was taught — don't introduce new theory.
- **One insight per interaction.** A widget that shows everything teaches nothing. Each should make one "oh, *that's* why" moment possible.
- **Feasible inline.** Everything will be hand-written HTML/CSS/SVG/vanilla JS inside a single file — no chart libraries. Design widgets that are buildable that way (simple plots, a few dozen data points, small state machines).
- **Not every slide needs a widget**, but every core concept does. Title, section, and recap slides can be static.

---

## Stage 3: Build the deck with frontend-slides

**Check it's installed first.** Look for `frontend-slides` in your available skills, or for `~/.claude/skills/frontend-slides/SKILL.md` or `.claude/skills/frontend-slides/SKILL.md` in the project root. If none is found, install it:

```bash
npx skills add https://github.com/zarazhangrui/frontend-slides --skill frontend-slides
```

Then confirm `SKILL.md` exists in the installed location before continuing. If the install fails, tell the user. Don't fall back to building the deck without it, because its style-preview step is part of what the user asked for.

Invoke the `frontend-slides` skill (via the Skill tool) and follow its workflow, with these lecture-specific inputs so the user isn't asked things you already know:

- **Purpose:** Teaching / Tutorial
- **Content:** All content ready — the lecture brief at `lectures/<slug>/lecture-brief.md`
- **Length:** roughly title + one slide per concept (two for heavy ones) + quiz + recap
- **Density:** still ask the user (the one Phase 1 question worth asking) — suggest *High density / reading-first* as the default for self-study

Ask the density question, and later the style pick, through `AskUserQuestion` too. For the style pick, make one option per preview, with the preview file path in its description, so the user can open the previews and choose without leaving the session.

**Always let frontend-slides run its style-discovery phase** — generate the 3 style previews and let the user pick before building. The user explicitly wants to choose the design. Choose preview moods that suit studying (calm, focused, legible) but keep the three genuinely different.

When generating the full deck, pass along these extra requirements on top of frontend-slides' own rules:

1. **Every concept slide implements the interactive visual from the brief**, inside the fixed 1920×1080 stage, with inline JS. Interactions must not hijack deck navigation: stop arrow-key/space propagation while a slider or input is focused, and keep click targets large.
2. **A "▶ Watch mm:ss" link** on each concept slide, opening the video at that timestamp in a new tab.
3. **Quiz slide(s)** with clickable answers that reveal correct/incorrect and the explanation.
4. **Recap slide** with the takeaways, and the source video link on the title or closing slide, along with the web sources from the brief.

Save the final deck as `lectures/<slug>/<slug>.html`.

### Verify before delivering

Open the deck in a browser and click through it: every widget responds, nothing overflows or overlaps the 16:9 stage, and keyboard navigation still works after using a slider. Fix anything broken — a dead widget is worse than none.

### Delivery

Follow frontend-slides' delivery phase, and also tell the user: the concepts covered, how many interactive slides there are, and where the transcript and brief live (they can edit the brief and ask you to regenerate).

---

## Running without a user present

If you're running non-interactively (no one to answer questions or pick a style — e.g. an automated test), don't stall. If there's no link, stop and say a link is needed, because you can't ask for one. Otherwise choose *High density / reading-first*, generate the previews anyway, pick the one that best fits a study context, and note your choice in the final summary.
