# AGENTS.md — Cine Remix workflow

This file is the single source of truth for how to use this repository. It follows the
[AGENTS.md](https://agents.md) convention, so any agentic coding tool that reads that file
(OpenAI Codex, and many others) picks this up automatically. Tool-specific entry points
(`.claude/skills/cine-remix/SKILL.md` for Claude Code, `.cursor/rules/cine-remix.mdc` for
Cursor, `.github/copilot-instructions.md` for Copilot, `CLAUDE.md` at the repo root) are thin
pointers back to this document — edit the workflow here, not in those files.

If you're a human (or a model with no file-reading harness at all, e.g. pasted straight into a
DeepSeek or GLM chat), you can just paste this whole file into the conversation along with the
contents of `references/` as needed — nothing here depends on any specific tool's plumbing.

## What this produces

Given a film-commentary video URL, **or** just a movie/show title with no link at all, produce
a complete deep-dive package:

1. A full **8–16 minute commentary script** — act-structured, timestamped, with a cold-open
   hook, verifiable historical/critical context, and a cross-work comparison.
2. A fully **original animated short screenplay** — a brand-new fable world every time, with
   its own hook, an echoing open/close, a foil character, and a tonal mix of dark wit and
   depth — inspired by the film's themes but not a retelling of it.
3. A **technique cross-reference table** mapping the devices used in both pieces.

Trigger on requests like: a movie name plus "写一份解说文案" / "commentary script for this
film"; a film-review video link plus "写一份更有深度的版本" / "give me a deeper, more original
take"; "把这部电影改编成动画" / "adapt this into an animated short".

## Copyright boundary (applies throughout, no exceptions)

The inputs here are frequently copyrighted material themselves (film dialogue, source novels,
someone else's commentary script). Every output must be **original commentary and original
adaptation** — never a copy with the names changed:

- The **commentary script** may freely discuss plot, characters, and historical background —
  that's standard film-criticism practice — but must not quote film dialogue or source-novel
  text at length. At most one short quote (≈15 characters/words), used only to illustrate a
  specific technique or a well-known line.
- If a **reference commentary video** was fetched, only extract *which techniques it uses*
  (hook style, argument shape, pacing) — do not reuse its specific wording, jokes, or
  arguments. The new script's thesis, structure, and phrasing must be independently designed.
- The **animated short must be 100% fictional**: new world, new character names, new specific
  plot. It should be inspired by the film's theme/structure, not be "the film's animated
  version." Simple test: someone who hasn't seen the source film shouldn't be able to identify
  it from the screenplay alone.
- Real historical/biographical facts (a director's or author's real fate, a real historical
  event) can be cited freely — facts aren't copyrightable — but only when you're confident
  they're accurate. Hedge uncertain details ("according to records...") or leave them out;
  never invent specifics to make the piece sound more authoritative.

## Workflow

### Step 1 — Determine the input type

- **A video URL was given** → go to Branch A.
- **Only a movie/show title was given (no link)** → go to Branch B.

### Branch A — Starting from a reference commentary video

Run `scripts/fetch_content.py` to fetch the reference video's info:

```bash
python3 scripts/fetch_content.py "<video_url>"
```

The script tries, in order of cost: platform captions → the video's own description/caption
text → local ASR fallback (see comments in the script for details). Once you have the content,
do a **lightweight teardown** only — what hook it uses, the rough shape of its argument, how it
closes — as input to "why this kind of content works," not a minute-by-minute structural
analysis. Then move to Step 2 and design an independent new script; don't hug the reference
video's specific wording or argument.

### Branch B — Only a movie/show title

Don't fetch any video. Use your own knowledge (and web search to fact-check specifics when
available) to gather what you need: director, writer(s), cast, release year, source-material
background if it's an adaptation, real historical/social context, and the film's real-world
critical reception if you know it. These facts need to hold up — hedge or skip anything you're
not sure of rather than inventing a specific year, a person's fate, or a reception detail to
make the piece feel more substantial.

### Step 2 — Design the script's thesis and structure

Don't start from a plot recap. First decide **the core thesis this particular script will
argue** — ideally an angle that diverges from (or productively complicates) the most common
reading of the film. That's what makes a script feel deep — not vocabulary. Once the thesis is
set, design the act structure backwards from it.

See [`references/script_format_guide.md`](references/script_format_guide.md) for hook
patterns, per-act closing-line conventions, and pacing guidance. Reuse the *method*, not any
specific example sentence in that file.

### Step 3 — Write the full commentary script

Fixed format: acts + timecodes + `【画面】`/`【音效】`/`【文案】` markers (see the template in
`references/script_format_guide.md`).

Hard requirements:
- Total runtime **8–16 minutes** (roughly 250–300 Chinese characters per minute at spoken
  pace — size the script accordingly; don't submit a 300-character outline and call it done).
- A genuine **hook** at the open: a counter-intuitive either/or question, a "state the
  conclusion, then undercut it" opening, or a striking scene fragment — not "Hi everyone,
  today let's talk about a movie."
- At least **one cross-work comparison** (a real, thematically related work), used to sharpen
  a specific point of difference — not just "this is similar to X."
- A **closing elevation**: collapse the film's specific story into a more universal claim the
  viewer can relate to their own life, followed by a short sign-off / call to action.

### Step 4 — Design the animated short's world

Before designing anything, check
[`references/used_concepts_log.md`](references/used_concepts_log.md) — it logs the carrier
images already used by past runs. **This run must use a new one.** Even if the theme is
similar to a past film, the concrete vehicle for it must be different.

See [`references/animation_fable_guide.md`](references/animation_fable_guide.md) for the
method: how to find a concrete, visual "carrier image" for an abstract theme, how to design an
echoing open/close, and how to mix dark wit with a serious theme without trivializing it.

Once designed, append one line to
[`references/used_concepts_log.md`](references/used_concepts_log.md) describing the carrier
image used, so future runs can avoid repeating it.

### Step 5 — Write the full animated screenplay

Fixed format: project info (title / runtime / visual style / tone) + character list + scene-by-
scene script (template in `references/animation_fable_guide.md`).

Hard requirements:
- Every scene needs a **visual description**, not just an abstract scene concept.
- A clear **echo design**: one line of dialogue or one visual symbol appears near the start and
  again at the end, with its meaning or tone shifted.
- At least one or two **foil/turning-point characters** (a skeptic, an heir) — don't let the
  protagonist carry the whole thing alone.
- Dialogue can carry dark wit, but pull back the tone for the reveal/emotional climax —
  don't turn the serious beats into jokes too.

### Step 6 — Assemble the final document

Follow [`references/output_template.md`](references/output_template.md): commentary script
first, then the animated screenplay, then a "technique cross-reference table" showing what
device each piece used and how they echo each other. That table is a third deliverable in its
own right — it's what makes the underlying method reusable, not just the two finished pieces.

## Edge cases

- **Can't fetch the film/video info**: report the actual error; don't fill in missing details
  with invented specifics. Write what's confidently known and flag what needs the user to
  supply.
- **Unsure about a historical/biographical detail**: use hedged language ("according to
  records...") or drop it — never invent a year, a person's fate, or a reception figure for
  dramatic effect.
- **The film itself is politically or historically contentious**: the commentary can take a
  clear thesis and stance, but don't hand down a final historical/political verdict on the
  user's behalf — keep the "this is one reading" framing. Same for the animated short: the
  fable can be sharp, but shouldn't name-check real political entities or living figures.
- **User only wants one of the two pieces**: skip the other one rather than padding it out to
  force a matched pair.
