<div align="center">

# 🎬 Cine Remix Forge

**Deep film commentary scripts. Original animated short screenplays. Generated, not copied.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-6b5b95)](https://claude.com/product/claude-code)
[![Python 3](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://www.python.org/)

English&nbsp;·&nbsp;[简体中文](README.zh-CN.md)

</div>

---

## Overview

Give it a film-commentary video URL, or just the name of a movie — nothing else required — and **Cine Remix Forge** produces a complete creative package:

1. **A deep-dive commentary script** — 8–16 minutes, act-structured with timecodes, a cold-open hook, verifiable historical/critical context, and at least one cross-work comparison. Not a plot recap with commentary bolted on.
2. **An original animated short screenplay** — a brand-new fable world every run, thematically inspired by the film but with its own characters, setting, and plot. Never a reskin of the source material.
3. **A technique cross-reference table** — maps the devices used in both pieces (hook, thesis, foil character, callback) so the underlying method is reusable, not just the output.

It ships as a [Claude Code](https://claude.com/product/claude-code) **skill** — a self-contained workflow definition plus supporting scripts and reference guides that Claude follows when invoked.

## Why this exists

Most "video teardown" tools stop at reproducing the source almost verbatim with the serial numbers filed off. This project takes the opposite bet: real value comes from extracting *why something works* and building something new on top of that understanding — not from repackaging what already exists. Every constraint in this repo (see [Copyright Principles](#copyright-principles)) exists to enforce that bet.

## Quick Start

Inside a Claude Code session with this skill enabled:

```text
Write a deep commentary script for <film title>, plus an original animated short inspired by it.
```

```text
https://youtube.com/watch?v=xxxx — this is a film commentary video. Write a deeper,
more original take, plus an animated short adaptation.
```

The skill detects which input mode you're in automatically:

| Input | What happens |
|---|---|
| **Movie title only** | Claude researches the film directly (own knowledge + web search for fact-checking) — no video is fetched. |
| **Video URL** | `scripts/fetch_content.py` pulls the reference video's metadata/transcript/comments first, purely to extract *which techniques it uses* — not to reuse its wording. |

Both paths converge on the same output pipeline: thesis-first script design → full commentary script → a fresh fable concept (checked against previously used ones) → full animated screenplay → cross-reference table.

## Project Structure

```
.claude/skills/cine-remix/
├── SKILL.md                          # Workflow, copyright rules, output requirements
├── scripts/
│   └── fetch_content.py              # Reference-video fetch (yt-dlp + local ASR fallback)
├── references/
│   ├── script_format_guide.md        # Act structure, hook patterns, closing devices
│   ├── animation_fable_guide.md      # Fable design method: carrier imagery, cyclic
│   │                                   structure, foil characters, tone balance
│   ├── used_concepts_log.md          # Append-only log of fable premises already used
│   └── output_template.md            # Final document assembly template
└── examples/
    └── ...                           # A real generated run, kept as a quality baseline
```

## Copyright Principles

Every output here is **original commentary and original adaptation** — never a copy with the names changed:

- Commentary scripts may freely discuss plot, characters, and history (standard film-criticism practice), but do not quote film dialogue or source-novel text at length — short, clearly-attributed quotes only.
- When a reference video is fetched, only its *technique* (hook style, pacing, argument shape) is extracted — its specific wording, jokes, and arguments are not reused.
- Animated shorts are 100% fictional: new world, new characters, new plot. The test is simple — someone who hasn't seen the source film shouldn't be able to identify it from the screenplay alone.
- Real biographical/historical facts may be cited freely (they aren't copyrightable), but only when the model is confident they're accurate — uncertain details are hedged or omitted, never invented.

Full rules live in [`SKILL.md`](.claude/skills/cine-remix/SKILL.md).

## Requirements

`fetch_content.py` depends on [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) and installs it on first use if missing (tries `brew`, then `pipx`, then `pip --user` in that order). Local ASR via [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) only kicks in as a last resort, when a reference video has neither usable captions nor a substantive description — and only in URL mode. Movie-title mode needs no extra dependencies at all.

## Status

Extracted into its own repository after the underlying method was validated across several real film examples in a working session — see `examples/` for a full sample run.

## License

[MIT](LICENSE)
