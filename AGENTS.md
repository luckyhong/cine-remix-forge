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

Also decide the narration persona before drafting the hook — persona shapes how the thesis
gets phrased, so it should be picked here, not bolted on after Step 3 is written. See
[`references/narration_style_library.md`](references/narration_style_library.md) for the full
roster and per-persona wording rules.

- If the user's original request already signals a tone ("写个吐槽向的", "温情一点",
  "悬疑感拉满", "学术一点别整虚的"), match it to the corresponding persona and just state which
  one you're using — no need to ask.
- If there's no tone signal in the request, ask once, using the same interaction pattern as
  Step 7 (plain-text question, numbered options, stated default):

  ```
  这次的深度解说词想用哪种叙述人设？
  1. 严肃反转型（默认，目前的标准调性——论点层层反转，判断句克制有分量）
  2. 学术严谨型（克制冷静，重证据轻煽情，像一篇讲究的影评）
  3. 犀利吐槽型（辛辣吐槽，敢损，但笑点不越过悲剧的红线）
  4. 温情人文型（贴近角色，情感真挚，收尾更像一封信）
  5. 悬疑节奏型（短句快节奏，留悬念，每幕结尾都埋一个钩子）
  不回复的话默认用 1. 严肃反转型（跟现在的输出保持一致）。
  ```

- Non-interactive/unattended runs: default silently to 严肃反转型 — same rule as Step 7, this
  choice must never block the script from being written.

### Step 3 — Write the full commentary script

Fixed format: acts + timecodes + `【画面】`/`【音效】`/`【文案】` markers (see the template in
`references/script_format_guide.md`).

Hard requirements (this whole list is the **film-commentary domain's default profile**, not a
project-wide constant — it's calibrated for and validated against `examples/`, the only domain
this repo has actually shipped so far; a future domain, e.g. a person or a historical event
instead of a film, may reasonably need a different runtime/pacing profile of its own rather than
inheriting this one by default):
- Total runtime **8–16 minutes** (roughly 250–300 Chinese characters per minute at spoken
  pace — size the script accordingly; don't submit a 300-character outline and call it done).
- A genuine **hook** at the open: a counter-intuitive either/or question, a "state the
  conclusion, then undercut it" opening, or a striking scene fragment — not "Hi everyone,
  today let's talk about a movie."
- At least **one cross-work comparison** (a real, thematically related work), used to sharpen
  a specific point of difference — not just "this is similar to X."
- A **closing elevation**: collapse the film's specific story into a more universal claim the
  viewer can relate to their own life, followed by a short sign-off / call to action.
- **画面跟得上文案的疏密**: when an act's narration duration (at 250–300 chars/min) is
  meaningfully shorter than the act's own timecode span, `【画面】` must become a timestamped
  shot list that fills the gap with concrete techniques — never just one lazy line like
  "镜头缓缓扫过". When narration is too dense to fit the span at all, trim the copy or adjust
  the timecodes instead. Thresholds and the shot-technique library:
  [`references/script_format_guide.md`](references/script_format_guide.md)（七）.

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

**Before moving to Step 7, self-check the assembled draft against this list** — don't rely on
having followed each rule correctly the first time around; go back and actually verify line by
line, and fix anything that doesn't hold up:

- [ ] Commentary script runtime is genuinely 8–16 minutes at 250–300 chars/min, not a
      lightly-padded outline (Step 3).
- [ ] The opening hook is one of the counter-intuitive patterns, not a plain "今天聊聊..." greeting.
- [ ] At least one cross-work comparison is present and names a **specific difference point**,
      not just "this is similar to X."
- [ ] The closing act does both things: a universal claim tied to the viewer's own life, and a
      short sign-off.
- [ ] The narration persona chosen in Step 2 is actually reflected in the hook/transition/closing
      wording — re-read a transition sentence and confirm it matches that persona's template in
      [`references/narration_style_library.md`](references/narration_style_library.md), not a
      generic default.
- [ ] Every act where narration duration falls meaningfully short of the act's timecode span has
      a timestamped shot list per [`references/script_format_guide.md`](references/script_format_guide.md)
      （七）— no act is left with a single vague "镜头缓缓扫过" line.
- [ ] Copyright check: no film dialogue or source-novel text quoted beyond ~15 characters/words;
      every historical/biographical fact is either one you're confident is accurate or explicitly
      hedged ("据记载...") — nothing was invented for dramatic effect.
- [ ] The animated short passes the "hasn't seen the source film" test: no reused names, no
      recognizable specific plot beats from the real film.
- [ ] The animated short has its echo (an opening line/symbol that returns changed at the close)
      and at least one foil/turning-point character — it isn't the protagonist carrying the whole
      thing alone.
- [ ] The new carrier image was appended to
      [`references/used_concepts_log.md`](references/used_concepts_log.md).
- [ ] The technique cross-reference table's rows are substantive and specific to this run, not
      filler that could apply to any film.

If any box doesn't hold up, fix the draft before saving — don't note the gap and move on anyway.

### Step 7 — Save it as a markdown file (don't stop at printing it in chat)

The deliverable is a document, not a chat message — **write it to an actual `.md` file** if
your environment has any file-writing capability at all (Claude Code, Cursor, Codex CLI, and
similar all do). Only skip this step if you are genuinely a bare chat model with no file
access (e.g. pasted straight into a DeepSeek/GLM conversation with no tools) — in that case,
print the full markdown in the response instead and say so.

**Where to save it is the user's choice, not something to decide silently.** Once the content
is assembled, ask — this is a plain-text question, so it works the same in Claude Code, Cursor,
Codex CLI, or a bare chat interface. Name what was actually written (not the generic word
"文档") and the film title, so the question reads like it's about the actual deliverable:

```
《<film title>》的深度解说词和动画短片剧本都写好了，存到哪？
A) 当前目录（<resolved cwd>）
B) 当前目录下的 works/（<resolved cwd>/works，如果不存在会新建）
C) 你自己指定一个路径
不回复的话默认用 <A, or B if a works/-like folder already exists in cwd>。
```

If only one of the two pieces was actually generated (per the "user only wants one" edge case
below), name that one specifically instead — e.g. "《<film title>》的深度解说词写好了，存到哪？"
— don't claim both exist when only one does.

Fill in the actual resolved paths, don't leave the placeholders literal. If a `works/` folder
(or something clearly playing that role) already exists in the current working directory, make
B the stated default in the last line; otherwise A is the default. This default only matters
for non-interactive/unattended runs where nobody will answer — **it must never block the
document from being written at all**, since Step 7's whole point is guaranteeing a real file
gets produced every time. In an interactive session, wait for the actual answer before writing.

Filename: `<film title>_深度解说词与动画短片.md` (romanize or translate the title if it's not
already convenient as a filename — see `examples/` for the naming pattern this repo itself
uses). Don't overwrite an existing file for the same film without asking; if one already
exists, either version it (`_v2`) or confirm with the user first.

After saving, tell the user the file path — don't just say "done," name where it landed.

## Optional Step 8 — Render the animated short as video

This step is **opt-in only**. Never trigger it off the same requests that trigger Steps 1–7 —
"写一份深度解说词" must never silently kick off image/video generation. It only activates on an
explicit, separate ask ("把这个动画短片做成视频" / "render this as a video" / "帮我配上手绘风格视频"
/ "生成即梦/Seedance 的提示词"), because unlike Steps 1–7 (pure text), this is slow and/or has
real generation cost.

Full mechanics live in [`references/video_render_routes.md`](references/video_render_routes.md).
The top-level decision tree:

1. Confirm the user actually wants this before doing anything.
2. Ask which route: **Route 1** (`scripts/screenplay_to_prose.py` → hand-drawn silent video via
   the `story-to-handdrawn-video` skill, ready today) or **Route 2**
   (`scripts/screenplay_to_video_prompts.py` → paste-ready prompts for Jimeng/Seedance or similar,
   ready today; live automation not available yet).
3. For Route 1: **always ask which scope** (`teaser`/`highlight`/`full`) — run the script with
   `--scope preview` first to show the actual scene selection and beat/duration estimate for this
   specific screenplay, then re-run with the confirmed scope. Never assume a default.
4. State plainly what they'll get before generating anything: Route 1 output is silent (no
   dialogue audio, no voice, no music — dialogue becomes paraphrased on-screen captions) and
   vertical 3:4; Route 2 output is a prompt list to paste elsewhere, not a rendered video.

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
- **Video rendering (Step 8)**: the conversion scripts only ever read the animated-short section
  of the assembled document, never the commentary section — this is what keeps the real film's
  title/director/history out of image/video-generation prompts. Don't work around that boundary
  by hand-copying commentary-section content into a render prompt.
