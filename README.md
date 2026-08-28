<div align="center">

# 🎬 Cine Remix Forge

**Deep film commentary scripts. Original animated short screenplays. Generated, not copied.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AGENTS.md](https://img.shields.io/badge/AGENTS.md-tool--agnostic-6b5b95)](AGENTS.md)
[![Python 3](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://www.python.org/)

English&nbsp;·&nbsp;[简体中文](README.zh-CN.md)

</div>

---

## Overview

Give it a film-commentary video URL, or just the name of a movie — nothing else required — and **Cine Remix Forge** produces a complete creative package:

1. **A deep-dive commentary script** — 8–16 minutes, act-structured with timecodes, a cold-open hook, verifiable historical/critical context, and at least one cross-work comparison. Not a plot recap with commentary bolted on.
2. **An original animated short screenplay** — a brand-new fable world every run, thematically inspired by the film but with its own characters, setting, and plot. Never a reskin of the source material.
3. **A technique cross-reference table** — maps the devices used in both pieces (hook, thesis, foil character, callback) so the underlying method is reusable, not just the output.

The document is always saved as a real `.md` file — you're asked where (see [Output](#output)) — and optionally, the animated short can go one step further and become an actual video (see [Optional: Render as Video](#optional-render-the-animated-short-as-video)).

The workflow itself is defined once, in [`AGENTS.md`](AGENTS.md), and is **not tied to any single AI tool**. Whatever agent you point at this repository — as long as it can read a markdown file and run a Python script — can execute it.

## Works With

| Tool | How it picks this up |
|---|---|
| **Claude Code** | Install as a skill (`~/.claude/skills/cine-remix/`, or clone the repo and open it directly) — `.claude/skills/cine-remix/SKILL.md` triggers automatically and defers to `AGENTS.md`. `CLAUDE.md` at the repo root covers the "opened the repo without installing it as a skill" case. Can also be invoked explicitly with `/cine-remix <request>` instead of relying on auto-triggering. |
| **Codex CLI** and other [agents.md](https://agents.md)-aware tools | Reads `AGENTS.md` at the repo root natively — no adapter needed. |
| **Cursor** | `.cursor/rules/cine-remix.mdc` triggers on matching requests and defers to `AGENTS.md`. |
| **GitHub Copilot** | `.github/copilot-instructions.md` points it at `AGENTS.md`. |
| **DeepSeek, GLM, or any bare chat model** | These are models, not tools with their own project-file convention — there's nothing to "install." Paste the contents of `AGENTS.md` (and the relevant `references/*.md` files) directly into the chat, or point a harness like Cline/Continue/opencode that already reads `AGENTS.md`-style rules at one of these models as the backend. |

Nothing in `AGENTS.md` or `references/` assumes a specific tool. The per-tool files above exist purely to get each tool to *find and follow* it — the actual workflow, copyright rules, and format requirements live in exactly one place, so they can't drift out of sync between tools.

## Why this exists

Most "video teardown" tools stop at reproducing the source almost verbatim with the serial numbers filed off. This project takes the opposite bet: real value comes from extracting *why something works* and building something new on top of that understanding — not from repackaging what already exists. Every constraint in this repo (see [Copyright Principles](#copyright-principles)) exists to enforce that bet.

## Quick Start

In any of the tools above, once it's pointed at this repo:

```text
Write a deep commentary script for <film title>, plus an original animated short inspired by it.
```

```text
https://youtube.com/watch?v=xxxx — this is a film commentary video. Write a deeper,
more original take, plus an animated short adaptation.
```

In Claude Code specifically, you can also invoke it explicitly by name instead of relying on auto-triggering:

```text
/cine-remix Write a deep commentary script for <film title>, plus an original animated short.
```

(This `/skill-name` syntax is specific to Claude Code — the other tools listed above rely on description-based auto-triggering, not a manual invocation prefix.)

The workflow detects which input mode you're in automatically:

| Input | What happens |
|---|---|
| **Movie title only** | The model researches the film directly (own knowledge + web search for fact-checking) — no video is fetched. |
| **Video URL** | `scripts/fetch_content.py` pulls the reference video's metadata/transcript/comments first, purely to extract *which techniques it uses* — not to reuse its wording. |

Both paths converge on the same output pipeline: thesis-first script design → full commentary script → a fresh fable concept (checked against previously used ones) → full animated screenplay → cross-reference table.

## Output

The assembled document is always saved as a real `.md` file — never left sitting only in the chat transcript. Once it's ready, you're asked where to put it:

```text
文档写好了，存到哪？
A) 当前目录（...）
B) 当前目录下的 works/（...，如果不存在会新建）
C) 你自己指定一个路径
```

If nothing answers (a non-interactive/unattended run), it falls back to a sensible default — an existing `works/`-style folder if one is present, otherwise the current directory — so a file is guaranteed either way.

## Optional: Render the Animated Short as Video

The two text deliverables are the default output — nothing below happens unless you explicitly ask for it, since rendering is slower and sometimes has real generation cost.

| Route | What it needs | What you get |
|---|---|---|
| **Route 1 — hand-drawn Remotion video** | A separately-installed `story-to-handdrawn-video` Claude Code skill (not part of this repo — it's a different project that must already be set up on your machine) | `scripts/screenplay_to_prose.py` converts the screenplay into that tool's flat-prose input (auto-generating its `--character-lock` and `--visual-plan`, and suggesting 3–5 of its 20 visual styles via `references/style_keyword_mapping.md`), producing a **silent**, **vertical 3:4** MP4. You're always asked which scope first — `teaser` (~1 scene), `highlight` (~4 scenes, recommended), or `full` (all scenes, explicitly flagged as slow) — run `--scope preview` to see the real scene selection and beat count before committing to one. |
| **Route 2 — richer AI video prompts** | Nothing — pure text output | `scripts/screenplay_to_video_prompts.py` emits one paste-ready prompt block per scene, for you to manually drop into Jimeng (即梦), Seedance, or any similar text-to-video tool. No API, no browser automation, no credentials — this environment doesn't have those wired up yet, so this stays a manual step by design (see `references/video_render_routes.md` for the documented, not-yet-built roadmap for automating it). |

Both scripts share the same copyright-safe parser (`scripts/_screenplay_parser.py`): they only ever read the animated-short section of the assembled document, never the commentary section that discusses the real film.

## Project Structure

```
AGENTS.md                             # Source of truth: workflow, copyright rules, output specs
CLAUDE.md                             # Pointer to AGENTS.md, for Claude Code opened directly on this repo
scripts/
├── fetch_content.py                  # Reference-video fetch (yt-dlp + local ASR fallback)
├── _screenplay_parser.py             # Shared, copyright-safe screenplay parser (route 1 & 2)
├── screenplay_to_prose.py            # Route 1: screenplay → story-to-handdrawn-video input
└── screenplay_to_video_prompts.py    # Route 2: screenplay → paste-ready Jimeng/Seedance prompts
references/
├── script_format_guide.md            # Act structure, hook patterns, closing devices
├── animation_fable_guide.md          # Fable design method: carrier imagery, cyclic
│                                        structure, foil characters, tone balance
├── used_concepts_log.md              # Append-only log of fable premises already used
├── output_template.md                # Final document assembly template
├── video_render_routes.md            # Route 1 & 2 mechanics, scope tiers, roadmap
└── style_keyword_mapping.md          # Screenplay style keywords → story-to-handdrawn-video style ids
examples/
└── ...                                # A real generated run, kept as a quality baseline
.claude/skills/cine-remix/SKILL.md    # Claude Code adapter → defers to AGENTS.md
.cursor/rules/cine-remix.mdc          # Cursor adapter → defers to AGENTS.md
.github/copilot-instructions.md       # Copilot adapter → defers to AGENTS.md
```

## Copyright Principles

Every output here is **original commentary and original adaptation** — never a copy with the names changed:

- Commentary scripts may freely discuss plot, characters, and history (standard film-criticism practice), but do not quote film dialogue or source-novel text at length — short, clearly-attributed quotes only.
- When a reference video is fetched, only its *technique* (hook style, pacing, argument shape) is extracted — its specific wording, jokes, and arguments are not reused.
- Animated shorts are 100% fictional: new world, new characters, new plot. The test is simple — someone who hasn't seen the source film shouldn't be able to identify it from the screenplay alone.
- Real biographical/historical facts may be cited freely (they aren't copyrightable), but only when the model is confident they're accurate — uncertain details are hedged or omitted, never invented.
- The same boundary extends to video rendering: both conversion scripts only ever read the animated-short section of the assembled document, never the commentary section.

Full rules live in [`AGENTS.md`](AGENTS.md).

## Requirements

`fetch_content.py` depends on [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) and installs it on first use if missing (tries `brew`, then `pipx`, then `pip --user` in that order). Local ASR via [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) only kicks in as a last resort, when a reference video has neither usable captions nor a substantive description — and only in URL mode. Movie-title mode needs no extra dependencies at all.

`screenplay_to_video_prompts.py` (Route 2) needs nothing beyond Python 3 — it only ever produces text. `screenplay_to_prose.py` (Route 1) also only needs Python 3 to run, but the actual video rendering it feeds into requires the separate `story-to-handdrawn-video` project/skill (Node 20+, ffmpeg, and an image-generation backend) to already be set up — that's outside this repo.

## Status

Extracted into its own repository after the underlying method was validated across several real film examples in a working session — see `examples/` for a full sample run.

## License

[MIT](LICENSE)
