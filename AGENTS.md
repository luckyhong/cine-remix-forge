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

### Step 1.5 — Fact-check before you design anything (mandatory, both branches)

**Do this before Step 2, not after.** Full method:
[`references/fact_check_guide.md`](references/fact_check_guide.md).

This step exists because a real test run (《高山下的花环》, 2026-08-31) passed every checklist in
this document and still shipped three factual errors — and its entire thesis was built on one of
them, so the correction wasn't an edit, it was a rewrite. The old flow had no step that owned
"is this true": `外部查重` owns *originality*, not accuracy, and "facts you're confident about"
is self-assessed, which never triggers because the model is always confident about training data.

Two rules override everything else here:

- **Highest-confidence facts are the highest-priority facts to check.** All three errors in that
  run landed on information the run itself had declared "highly stable, changes little over the
  years": the production studio, the awards, and how a famous scene actually ended. Famous scenes
  are dangerous precisely because their *first half* (who got angry, what they said) circulates
  widely while their *ending* gets filled in by narrative inertia.
- **Unverified means unwritten — hedging is not a substitute.** "据记载……" is for genuinely
  disputed facts, not for "I didn't look it up." If you can't verify it, cut the sentence and
  write one you can.

Produce a **事实清单** table (format in the guide; it ships in the document header per
[`references/output_template.md`](references/output_template.md)). Tier-1 (the facts the thesis
rests on, and how famous scenes actually ended) and tier-2 (studio, year, awards, source
publication) entries **must be externally searched — "I know this" is not accepted**. Tier-1
load-bearing facts need two independent sources. Awards must be precise to *which edition, which
award, won vs. merely nominated* — Chinese film awards (金鸡 vs. 百花) are a known trap.

Then do the step most likely to be skipped: **ask whether the verified reality is more
interesting than what you had planned to argue.** In the run above it plainly was — "justice
depends on who happens to be in the room" (built on a false premise) became "everything that
got honored was handed over privately; nothing the rules owed ever arrived" (built on what the
film actually shows). Fact-checking is not only mine-clearing; it is a source of depth.

Tell the user what the check found in one or two lines before moving on — a silent pass and a
silent skip look identical from their side.

### Step 2 — Design the script's thesis and structure

Don't start from a plot recap. **Start from the 事实清单 Step 1.5 just produced** — the thesis
must rest only on ✅ entries, and you must be able to name which entries it rests on (those are
its 承重事实). A thesis that needs an unverified fact is not a thesis yet; go verify it or pick
a different angle. Then decide **the core thesis this particular script will argue** — ideally an angle that diverges from (or productively complicates) the most common
reading of the film. That's what makes a script feel deep — not vocabulary. Once the thesis is
set, design the act structure backwards from it.

Before locking the thesis in, run three checks so "diverges from the most common reading" is an
actual verified step, not something left to happen by accident:

- **External check (must produce a visible declaration, not a silent mental step)**: name the
  film's most common existing reading(s). Then write one of these two lines into the assembled
  document's header (see [`references/output_template.md`](references/output_template.md)) and
  say it to the user before Step 3 begins:

  `外部查重：已搜索确认——[搜到的关键信息/来源]`, or
  `外部查重：未搜索，基于训练知识，置信度[高/中/低]——[为什么]`

  "Search if you're not confident" is too easy to rationalize past — the model almost always
  *feels* confident about training data, so the search never actually triggers. Writing a
  confidence label down makes the skip visible instead of invisible. **Since Step 1.5 now makes
  an external search mandatory anyway, `未搜索` here is close to indefensible** — you are already
  online for the facts, and "which readings of this film are common" costs one more query. Treat
  the 未搜索 branch as reserved for a genuinely offline environment, and say so when you use it. Applies to both Branch A and
  Branch B; a reference video's specific wording is a separate concern already covered above.

  A "common reading" declaration by itself is not enough — a run was found to have searched the
  topic-level reading in good faith, declared 已搜索确认, and still built its "reversal" around a
  specific plot detail (a line, a scene, a single observation) that was *itself* already one of
  the most commonly-discussed details of the film, making the "reversal" a repackaging of two
  already-common observations rather than a genuinely new one. So: once the thesis is designed,
  name the **single most load-bearing specific detail** it depends on — the one detail without
  which the argument would collapse — and separately declare whether *that detail's
  interpretation* (not just the film's general reading) is itself already commonly discussed:

  `关键细节查重：[细节] 本身已经是常见解读的一部分 / 本身不算常见解读`

  If it's already common (often true — famous scenes are famous because they're already
  discussed), that's not disqualifying, but the depth then has to come from how you *recombine or
  extend* it, not from presenting the detail's existence as the reversal itself. Say explicitly in
  the declaration what the added value is beyond the detail being pointed out.
- **Internal check**: look up [`references/used_theses_log.md`](references/used_theses_log.md).
  If this film has been covered before, this run's thesis must take a materially different
  angle, not the same angle with new phrasing.
- **Sameness check (讲法, not 论点)**: look up
  [`references/used_devices_log.md`](references/used_devices_log.md) and obey its four hard rules —
  no cross-work comparison film reused within the last 5 runs, no hook type used 3 times running,
  don't land on the same act count every time, and don't always place the "common reading" act in
  the same slot. Two different logs already guard the *thesis* and the *fable's carrier image*;
  neither notices that six consecutive runs opened the same way and shaped the acts the same way.
  What an audience actually experiences as "this channel repeats itself" is usually this, not the
  thesis. Append a line to that log once the hook type, comparison work, and act structure are
  settled.
- **Third-layer check**: your thesis already diverges from the common reading (external check) —
  now find the strongest objection *to your own thesis itself*, not a restatement of the common
  reading's objection. This is [`references/script_format_guide.md`](references/script_format_guide.md)
  六's "third layer": intuitive reading → your reversal → this reversal complicated further.

  Generate **at least two structurally different objections** first — not two phrasings of the
  same idea, two different angles of attack (e.g., one that challenges the thesis's *evidence* —
  "doesn't this one scene actually cut the other way" — and one that challenges its *underlying
  logic or motive framing* — "even granting the evidence, isn't the deeper driver something your
  thesis doesn't name"). A run was found to state and answer a real objection while a harder,
  structurally different one — attacking the thesis's whole framing rather than one scene — went
  unconsidered, because the first objection that came to mind was answerable and nothing forced a
  comparison against a second. Compare the two, and engage **whichever one is actually harder to
  answer**, not whichever occurred to you first or is easiest to rebut. If you can't generate two
  structurally distinct objections, your reversal is probably too clean to be the deepest
  available reading — go back and complicate it further before drafting Step 3.

  Decide which specific act will engage the chosen objection (usually the closing act, but any
  specific act is valid) — the act you name must contain an actual sentence that states the
  objection and answers it, not just gesture near it.

Once the thesis is locked in, append one line to
[`references/used_theses_log.md`](references/used_theses_log.md) stating it, **the load-bearing
detail and its own-familiarity declaration**, and **both candidate objections with which one was
chosen and why**, so future runs — on this film or others — can check against the angle, the
depth achieved, and see the objection that was set aside.

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
- Total runtime **8–16 minutes**, and keep two different numbers straight — conflating them has
  already caused a false defect report (七.2):
  - **语速 (speaking rate)** = characters ÷ seconds actually spoken → **250–300 chars/min**.
  - **密度 (timeline density)** = characters ÷ act duration → **200–260 chars/min**.
  The difference between them is screen time with no narration, which is legitimate and designed —
  it gets covered by cut-sheet rows marked 无旁白, not by padding the copy. Under 200 means the
  timecodes are stretched (tighten them rather than adding words); over 260 means the visuals never
  breathe; `字数 × 0.2 > 幕时长 × 1.1` is a hard violation (unreadable at any sane pace). Don't
  submit a 300-character outline and call it done.
- A genuine **hook** at the open. Picking one of the four patterns is not enough — "isn't a
  plain greeting" was the only bar here for a long time, and it is far too low for a channel
  where the first 15 seconds decide completion rate. The hook must clear every content bar
  in [`references/script_format_guide.md`](references/script_format_guide.md) 2.1: **a concrete,
  filmable anomalous fact lands within the first 15 seconds** (an abstract rhetorical question
  may follow it, never lead); **a one-sentence information gap the viewer could say out loud**
  (write that sentence down as a self-check — if it comes out as "what is this film about," the
  hook fails); **no background exposition in the hook act at all** — director, year, source
  novel, awards all belong to act two; and the **双观众测试** — a film-commentary audience always
  splits in two, and a hook that works on only one half throws away half the completion rate:
  someone who hasn't seen the film needs a gap that stands on its own with zero prior knowledge,
  and someone who has seen it needs something that overturns the impression they already hold.
  Write down both reactions; if either is "so what?" or "I already knew that," rewrite. The strongest hook material is usually whatever Step 1.5's
  fact-check turned up that contradicts the popular impression, so don't finalize the opening
  before that check is done.
- At least **one cross-work comparison** (a real, thematically related work), used to sharpen
  a specific point of difference — not just "this is similar to X." Check the comparison film
  against [`references/used_devices_log.md`](references/used_devices_log.md) first: reusing one
  within 5 runs reads to an audience as "this channel has only seen two movies."
- A **closing elevation**: collapse the film's specific story into a more universal claim the
  viewer can relate to their own life, followed by a short sign-off / call to action.
- **画面 must be chosen before it is measured**: the density rules below are an engineering
  fix (don't leave screen time empty); they do not make the visuals *good*, and shipped runs
  have passed every density check while describing shots as "交叉剪辑三条线" — compliant and
  unwatchable. Apply [`references/script_format_guide.md`](references/script_format_guide.md)
  7.0 to **every** 【画面】 field, including the ones that never trigger a shot list: the first
  shot of each act is that act's visual evidence, not atmosphere; prefer a **pair that can be
  intercut** over one pretty frame; **give every absence a picture** (an empty line on a roster,
  a drum that doesn't sound) wherever the thesis says "never" or "didn't"; and the four banned
  phrasings ("镜头缓缓扫过", "快速闪回若干画面", "用蒙太奇串起…", "配合文案节奏切换") are
  unusable because an editor cannot act on them.
- A **剪辑交付 block** — this is what turns the file from a creative document into one someone can
  actually cut from. Full spec:
  [`references/edit_delivery_guide.md`](references/edit_delivery_guide.md). Three tables, all
  required: a **素材清单** (every distinct source clip, deduplicated, each with a
  scrub-recognizable visual signature and a **`⬜ 待填` timecode column — never invent a source
  timecode**, a wrong one is worse than none because the editor will go looking for it; reused
  shots must be flagged in the 用在 column, since the open/close echo this workflow always builds
  means some frames are deliberately used twice); a **剪辑执行表** covering the whole film shot by
  shot, with continuous in-points whose durations sum exactly to the runtime; and **配音提示**
  (target chars/min, per-act character counts to check the read against, the one line that is the
  film's emotional peak, pause marks, and where — or whether — a channel intro goes).
- **【文案】 is the VO script, not a draft to be rewritten before recording**: no **breath group**
  — the run of characters between two punctuation marks — over ~40 characters, and numerals and
  ordinals spelled out as spoken ("第八届", not "第8届"). Measure between punctuation, not between
  full stops: a 90-character sentence carrying six commas reads fine aloud, while 45 characters
  with no comma at all is what runs the reader out of breath. When it trips, add punctuation
  rather than chopping the sentence up — chopping destroys the long-buildup-into-short-verdict
  rhythm the act structure depends on.
- A **封面提案** at the end of the script (format: 7.0's sibling section 八): one cover frame —
  which must be a shot that already appears in a 【画面】 field, not a new invention — plus a
  ≤12-character cover line and one alternate. The cover line must open the *same* information
  gap the hook closes. Clickbait formulas (震惊/细思极恐/99%的人没看懂) are out: they trade
  against the depth this whole workflow exists to produce.
- **One source of truth for timing**: `【画面】` carries the *visual argument* (which shots, and
  why) and **never a duration, a shot count, or a timecode** — all of that lives in the cut sheet.
  Two places holding the same numbers is not redundancy, it is a guarantee that an edit to one
  will contradict the other; that exact failure has already been observed. See
  [`references/script_format_guide.md`](references/script_format_guide.md) 七.0.

### Step 4 — Design the animated short's world

Before designing anything, check
[`references/used_concepts_log.md`](references/used_concepts_log.md) — it logs both the carrier
images **and the circulation mechanisms** already used by past runs. **This run must use both a
new carrier image and, if the theme calls for a circulation structure, a circulation mechanism
not structurally identical to a past entry's** — a different carrier image alone is not
sufficient if the underlying machine (periodic ritual + a rotating figure who announces it +
an unfulfilled promise) is the same as a past entry's; see
[`references/animation_fable_guide.md`](references/animation_fable_guide.md) 三 for alternate
mechanisms.

See [`references/animation_fable_guide.md`](references/animation_fable_guide.md) for the
method: how to find a concrete, visual "carrier image" for an abstract theme, how to choose a
circulation mechanism that isn't a repeat of a past entry's underlying shape, how to design an
echoing open/close, and how to mix dark wit with a serious theme without trivializing it.

Once designed, append one line to
[`references/used_concepts_log.md`](references/used_concepts_log.md) describing **both** the
carrier image and the circulation mechanism used (see that file's format), so future runs can
avoid repeating either.

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

- [ ] **Run the linter and get a clean pass** — `python3 scripts/lint_output.py <the .md>`. It
      mechanically checks act-timecode continuity, total runtime, 语速/密度 bands per act, breath
      groups ≤40 chars, that no 【画面】 field carries a duration/shot-count/timecode (七.0's single
      source of truth), the four banned shot phrasings, one bolded verdict per act, the hook's
      first 15 seconds being free of exposition, cut-sheet in-point continuity and its sum matching
      the runtime, source-manifest ↔ cut-sheet agreement in both directions, that every source
      timecode is still `⬜ 待填` rather than fabricated, tier-1/2 fact rows all ✅, and the cover
      line's length. These were seven checklist boxes until 2026-08-31; boxes this mechanical get
      ticked wholesale on a "felt like I did that" pass, which is the very failure Step 6.5 exists
      to catch — so they are now executed instead of attested. **A FAIL is a blocker, not a note.**
- [ ] The opening hook clears every bar in `script_format_guide.md` 2.1 (A–F), not just "isn't a
      plain 今天聊聊 greeting": a concrete filmable anomalous fact inside 15 seconds; **the
      one-sentence viewer question written out explicitly** (write it in the working note — if it
      reads "what's this film about," rewrite the hook); zero background exposition (director /
      year / source novel / awards) anywhere in the hook act; and it survives the restate test.
- [ ] `used_devices_log.md`'s four hard rules all hold for this run (comparison film not reused
      within 5 runs; hook type not the third consecutive use; act count not the third identical
      one; the common-reading act is not in the default slot for the Nth time running), and the
      new line was appended.
- [ ] At least one cross-work comparison is present and names a **specific difference point**,
      not just "this is similar to X."
- [ ] The closing act does both things: a universal claim tied to the viewer's own life, and a
      short sign-off. A fast-paced persona (e.g. ⑤悬疑节奏型) can and should keep this brief —
      "收得快，不做长篇抒情" is about length and tone, not permission to drop the viewer
      connection entirely; a bare abstract judgment with no link to the viewer's own life doesn't
      satisfy this even if it's punchy.
- [ ] The narration persona chosen in Step 2 is actually reflected in the hook/transition/closing
      wording — re-read a transition sentence and confirm it matches that persona's template in
      [`references/narration_style_library.md`](references/narration_style_library.md), not a
      generic default.
- [ ] Copyright check: no film dialogue or source-novel text quoted beyond ~15 characters/words;
      every historical/biographical fact is either one you're confident is accurate or explicitly
      hedged ("据记载...") — nothing was invented for dramatic effect.
- [ ] All four Step 2 declarations are present in the document header, not skipped or vague:
      外部查重 (`已搜索确认.../未搜索...置信度...`), 关键细节查重 (with the added-value note if
      the detail is already common), and 三层反驳 (both candidate objections named, with which
      one was chosen and why).
- [ ] The animated short passes the "hasn't seen the source film" test: no reused names, no
      recognizable specific plot beats from the real film.
- [ ] The animated short has its echo (an opening line/symbol that returns changed at the close)
      and at least one foil/turning-point character — it isn't the protagonist carrying the whole
      thing alone.
- [ ] The new carrier image **and circulation mechanism** were appended to
      [`references/used_concepts_log.md`](references/used_concepts_log.md) in the two-part
      format, and the thesis angle **and its third-layer objection** were appended to
      [`references/used_theses_log.md`](references/used_theses_log.md).
- [ ] The technique cross-reference table's rows are substantive and specific to this run — and
      each row's **label itself** (not just its content) was checked against what the script
      actually does, per `output_template.md`（三）; a label inherited from a past example
      (e.g. "循环结构") was renamed if it doesn't structurally fit this film (e.g. a sustained
      parallel contrast is "平行对照", not "循环结构").

If any box doesn't hold up, fix the draft before saving — don't note the gap and move on anyway.

### Step 6.5 — Adversarial second pass: try to break the draft, don't just confirm it

The checklist above is an **affirmative** pass — every item asks "does X hold," and a first-pass
generation that wrote each of those things in good faith will tick every box without real
scrutiny. This is a known, observed failure mode of this exact workflow: a real test run passed
every item on that list and still had five substantive problems, found only when the same model
was made to switch into a genuinely different review mode — actively hunting for the weakest
point, not confirming compliance. Do not skip this step and do not fold it into the checklist
above as more boxes; it must be a **separate pass with a different task shape**: instead of
"does X hold" (yes/no), each item below asks you to **attempt to falsify a specific claim** and
requires a **quoted or counted answer**, not a checkmark. Do this after Step 6's checklist
passes, before Step 7.

Answer each of these in writing (a few lines each is enough — this isn't a new deliverable, it's
a working note you can discard after fixing what it finds):

1. **Thesis counter-argument**: quote the exact sentence (or two) in the script where the chosen
   third-layer objection (Step 2) is actually stated and answered. If you can't point to a
   specific sentence, it isn't there — go add it, don't describe it in the abstract. Then look
   back at the *other* candidate objection you generated and set aside — reread it once more and
   confirm it's genuinely the weaker of the two, not just the one that happened to get picked
   first. A run was found to answer a real objection while a structurally harder one (attacking
   the thesis's whole framing, not one scene) went unconsidered — this re-check exists specifically
   to catch that.
2. **Table row labels**: for each row in the technique cross-reference table, quote one specific
   line from the script or screenplay that the row's label word (e.g. "循环", "对照", "呼应")
   actually describes. If a row's key word doesn't have a real textual match, the label is wrong
   — rename it ([`references/output_template.md`](references/output_template.md) 三).
3. **Shot-technique count**: literally count, across the whole script, how many times each of
   the 8 techniques in [`references/script_format_guide.md`](references/script_format_guide.md)
   七.4 is used as the dominant/延展 technique in a triggering act. Write the tally. If one
   technique's count exceeds half the triggering acts, fix it per 七.4.1 — don't eyeball this,
   count it.
4. **Circulation mechanism**: state which mechanism category
   ([`references/animation_fable_guide.md`](references/animation_fable_guide.md) 三) this run's
   fable uses, then open `used_concepts_log.md` and check it against every past entry's
   mechanism field, not just the carrier image. If two entries share a mechanism, name the two
   and confirm this is a genuinely intentional repeat you're prepared to log as-is, not an
   accident.
5. **Load-bearing detail check**: re-read your own 关键细节查重 declaration. If the detail is
   marked already-common, quote the specific sentence where the script's *added value* — the
   recombination or extension beyond the detail itself — actually appears. A "reversal" built by
   repackaging one already-famous detail under a new label is not depth; if you can't quote where
   the script goes beyond the detail, it's a repackaging, not a reversal — go add the extension or
   pick a different load-bearing detail.

6. **Fact-check falsification**: pick the **two facts in the script you feel most certain about**
   — not the ones you feel shakiest on — and state, for each, the specific source that confirmed
   it in Step 1.5. This ordering is deliberate and is the whole point of the item: on 2026-08-31
   all three shipped errors were facts the run had explicitly rated as stable and obvious, while
   every fact it felt unsure about was either checked or cut. If your answer for either one is a
   paraphrase of "everyone knows this," you have just reproduced that failure — go search it now.
   Then, separately: name any famous scene the script describes and quote the sentence stating
   **how it actually ended**. A scene whose ending you cannot cite is a scene whose ending you
   inferred.

7. **Hook cold-read**: read only the first act's 【文案】, as if you had never heard of this film,
   and write the single question it makes you want answered. Then compare that question to the
   thesis. If the question is vague ("what happens next?"), or if answering it wouldn't require
   the thesis, the hook is decorative — rewrite it against 2.1 before saving.

If any of the seven produces a "no, I can't point to that" answer, that is a finding — fix the
draft, then re-answer that one item to confirm the fix actually lands (don't just assume it
does). This pass is not optional, and skipping it because Step 6's checklist already passed is
exactly the mistake this section exists to prevent.

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

## Optional Step 9 — Publish an interactive visual page

Also **opt-in only**, same rule as Step 8: never trigger this off "写一份深度解说词" — it only
activates on an explicit, separate ask ("发布成网页" / "做个可视化页面" / "生成一个交互页面看看" /
"把对照表做成图").

Full mechanics live in
[`references/interactive_output_guide.md`](references/interactive_output_guide.md). Short
version: this depends on the host tool having a "publish an interactive page" capability (e.g.
Artifact in Claude Code) — if it doesn't, say so plainly instead of falling back to a local HTML
file nobody will open. The page visualizes three things the assembled `.md` document can't show
well as plain text: the full-film act timeline, a per-act 画面/文案 alignment bar (making the
shot-density rule's output actually visible), and the technique cross-reference table as a
connected two-column diagram instead of a markdown table. Tone must scale with the film's actual
weight — never default to a cheerful/decorative treatment for content that involves real
historical trauma. It's a re-presentation of already-approved content, not new content: never
invent a filler detail to make the page feel fuller.

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
