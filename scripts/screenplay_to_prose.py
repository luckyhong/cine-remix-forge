#!/usr/bin/env python3
"""Convert a cine-remix animated-short screenplay into the flat Chinese prose
(plus --visual-plan JSON and --character-lock text) that the
`story-to-handdrawn-video` Remotion renderer expects.

Copyright/safety boundary: this script ONLY reads the animated-short section
of the assembled document -- everything between the "## 二、原创动画短片剧本"
heading and the "## 三、创作手法对照表" heading. It never touches the
"## 一、深度解说词" section, which legitimately discusses the real source
film/director/history and must never leak into image-generation prompts.
This is a structural parsing limit, not a request made of the model.

`story-to-handdrawn-video` is silent by design (no dialogue audio, no BGM) and
treats every sentence as exactly one ~5s "beat" with a hard ~39-usable-char
caption cap. This script does NOT attempt real semantic paraphrasing of
dialogue -- it's a deterministic reformat (strip screenplay-style speaker
labels and quote marks, add a narration verb) so lines read as third-person
narration rather than raw script directions. It is not a substitute for a
human/LLM smoothing pass before you actually render -- that's why this
script always writes a *_render-notes.md file for review, and never
generates anything without an explicit --scope.

See references/video_render_routes.md for the full method this implements.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _screenplay_parser import parse_screenplay  # noqa: E402

TURN_WORDS = ["后来", "然后", "接着", "于是", "但是", "但", "却", "可是",
              "直到", "最后", "没想到", "第二天", "那天", "这时", "随后"]
SENTENCE_END = "。！？!?；;"
SAFE_BEAT_CHARS = 39  # 3 lines x 13 chars, staying under the tool's hard 45-char cap

STYLE_CLUSTERS = {
    ("剪影", "皮影", "木偶", "提线", "偶动画"): ["linocut-editorial", "ink-wash", "organic-contour-doodle"],
    ("寓言", "绘本", "治愈", "温情"): ["sunlit-storybook", "warm-flat-storybook", "nordic-gouache-storybook"],
    ("沉重", "严肃", "历史感", "年代感", "做旧"): ["retro-gouache-concept", "inked-storybook", "emotional-watercolor-sketch"],
    ("荒诞", "戏谑", "黑色幽默", "反讽"): ["ms-paint-bad-doodle", "bean-doodle-infographic", "rawkid-crayon"],
    ("官僚", "讽刺", "社论", "批判"): ["linocut-editorial", "whiteboard-explainer", "zine-riso-collage"],
    ("儿童", "天真", "反差萌"): ["kid-crayon", "rawkid-crayon", "real-crayon-paper"],
    ("水墨", "东方", "古典"): ["ink-wash", "retro-gouache-concept"],
    ("极简", "概念", "说明性", "图解"): ["minimal-line-explainer", "whiteboard-explainer", "bean-doodle-infographic"],
    ("复古", "怀旧", "褪色", "中古"): ["retro-gouache-concept", "nordic-gouache-storybook", "real-crayon-paper"],
    ("拼贴", "独立杂志", "版画"): ["zine-riso-collage", "naive-marker-notes"],
    ("日记", "私人化", "手记"): ["colored-pencil-diary", "emotional-watercolor-sketch", "naive-marker-notes"],
}
DEFAULT_STYLE = "colored-pencil-diary"


def select_scenes(scenes, scope):
    if scope == "full":
        return list(scenes)
    if not scenes:
        return []
    by_role = {}
    for s in scenes:
        by_role.setdefault(s.role, []).append(s)

    def pick(role, fallback):
        return by_role[role][0] if by_role.get(role) else fallback

    first, last = scenes[0], scenes[-1]
    climax = pick("climax", None)
    if scope == "teaser":
        return [climax or first]
    if scope == "highlight":
        loop = pick("loop", None)
        picks = [first]
        if loop and loop not in picks:
            picks.append(loop)
        if climax and climax not in picks:
            picks.append(climax)
        if last not in picks:
            picks.append(last)
        # keep original scene order
        picks_sorted = sorted(set(s.num for s in picks))
        return [s for s in scenes if s.num in picks_sorted]
    raise ValueError(f"unknown scope: {scope}")


def dialogue_to_narration(speaker, mood, content):
    content = content.strip().strip('"“”')
    verb = "说"
    if mood:
        verb = f"{mood}地说" if len(mood) <= 4 else "说"
    return f"{speaker}{verb}：{content}"


def hard_chunk(text, limit=SAFE_BEAT_CHARS):
    """Recursively split text to fit under `limit` chars, same spirit as the
    target tool's own chunking: try turn-words first, then commas, then a
    raw cut as a last resort."""
    text = text.strip()
    if len(text) <= limit:
        return [text] if text else []
    for tw in TURN_WORDS:
        idx = text.find(tw, 2)
        if idx > 0:
            return hard_chunk(text[:idx], limit) + hard_chunk(text[idx:], limit)
    for sep in ("，", "、", ","):
        idx = text.rfind(sep, 0, limit)
        if idx > 0:
            return hard_chunk(text[:idx + 1], limit) + hard_chunk(text[idx + 1:], limit)
    return [text[:limit]] + hard_chunk(text[limit:], limit)


def split_into_beats(paragraph):
    beats = []
    buf = ""
    for ch in paragraph:
        buf += ch
        if ch in SENTENCE_END:
            beats.append(buf.strip())
            buf = ""
    if buf.strip():
        beats.append(buf.strip())
    out = []
    for b in beats:
        out.extend(hard_chunk(b))
    return [b for b in out if b]


def build_prose(selected_scenes):
    beats = []
    for scene in selected_scenes:
        narration_paragraph = "".join(scene.visual_lines)
        beats.extend(split_into_beats(narration_paragraph))
        for speaker, mood, content in scene.dialogue:
            beats.extend(split_into_beats(dialogue_to_narration(speaker, mood, content)))
    prose = "\n".join(beats)
    visual_plan = {}
    for i, scene in enumerate(selected_scenes):
        extra = "；".join(scene.visual_lines)[:80]
        if extra:
            visual_plan[f"{i + 1:02d}"] = f"参考画面细节：{extra}"
    return prose, beats, visual_plan


def build_character_lock(characters):
    if not characters:
        return ""
    lock = "全片角色形象需保持一致：" + "；".join(characters)
    if any("同一" in c or "只" in c and "换" in c for c in characters):
        lock += "。特别注意：不同权威角色应使用同一基础剪影/造型，仅更换指定的标识物，不要画成不同的人。"
    return lock


def suggest_styles(style_keywords):
    hits = []
    for cluster_words, styles in STYLE_CLUSTERS.items():
        if any(w in style_keywords for w in cluster_words):
            for s in styles:
                if s not in hits:
                    hits.append(s)
    if not hits:
        return [DEFAULT_STYLE]
    return hits[:5]


SCOPE_TABLE = [
    ("teaser", "1场（高潮/反转，无明显高潮则用开场）", "~10-14", "~55-80秒"),
    ("highlight", "4场：开场 + 一轮代表性循环 + 高潮/反转 + 结尾（含首尾）", "~28-30", "~2.5-3分钟"),
    ("full", "全部场次", "~65-110", "完整6-9分钟，几十步串行出图+渲染，会很慢"),
]


def print_preview(scenes):
    print("场次角色识别结果（请确认，不要盲信）：")
    for s in scenes:
        print(f"  Scene {s.num} · {s.title_raw}  → 识别为「{s.role}」")
    print()
    print("三档范围预估（镜头数是按实际转写逻辑算出来的真实数字，不是粗略估算）：")
    for scope, desc, _, _ in SCOPE_TABLE:
        picked = select_scenes(scenes, scope)
        _, beats_list, _ = build_prose(picked)
        beats = len(beats_list)
        secs = beats * 5.5
        print(f"  [{scope}] {desc}")
        print(f"    → 本次实际选中场次: {[s.num for s in picked]}, 实际镜头数 {beats}, 预估时长 ~{secs/60:.1f}分钟")
    print()
    print("未指定 --scope，先看上面的预览再决定用哪一档重新运行。")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("doc_path", help="assembled cine-remix markdown document (contains the animated-short section)")
    ap.add_argument("--scope", choices=["preview", "teaser", "highlight", "full"], default="preview",
                     help="which portion to convert; 'preview' (default) only prints the tier table, writes nothing")
    ap.add_argument("--out-dir", default=None, help="directory to write outputs to (default: same dir as doc_path)")
    args = ap.parse_args()

    with open(args.doc_path, encoding="utf-8") as f:
        doc_text = f.read()

    project_info, characters, scenes = parse_screenplay(doc_text)
    if not scenes:
        print("没有解析到任何 Scene，检查文档格式是否匹配 references/animation_fable_guide.md 的模板。", file=sys.stderr)
        sys.exit(1)

    if args.scope == "preview":
        print(f"片名：{project_info.get('片名', '(未识别)')}")
        print_preview(scenes)
        return

    selected = select_scenes(scenes, args.scope)
    prose, beats, visual_plan = build_prose(selected)
    lock = build_character_lock(characters)
    style_candidates = suggest_styles(project_info.get("形式", ""))

    out_dir = args.out_dir or os.path.dirname(os.path.abspath(args.doc_path))
    title = project_info.get("片名", "untitled").strip("《》") or "untitled"
    prefix = os.path.join(out_dir, f"{title}_{args.scope}")

    with open(prefix + ".txt", "w", encoding="utf-8") as f:
        f.write(prose + "\n")
    with open(prefix + ".visual-plan.json", "w", encoding="utf-8") as f:
        json.dump(visual_plan, f, ensure_ascii=False, indent=2)

    notes = [
        f"# {title} — {args.scope} 档渲染准备笔记",
        "",
        f"选中场次：{[s.num for s in selected]}（共{len(selected)}场，{len(beats)}个镜头）",
        "",
        "## 画风候选（未自动锁定，需要用户确认）",
        *[f"- {s}" for s in style_candidates],
        f"- 不确定就用默认：{DEFAULT_STYLE}",
        "",
        "## character-lock",
        lock or "(未解析到人物列表，建议手动补充)",
        "",
        "## 提醒",
        "- 输出是静音视频：没有配音、没有角色声音、没有配乐，台词已转写成第三人称叙述字幕。",
        "- 画面固定竖屏 3:4（1080x1440）。",
        "- 这是机械改写（去掉说话人标签和引号、加一个叙述动词），不是语义润色——生成前建议再读一遍 .txt 顺一下语感。",
    ]
    if args.scope == "full":
        notes.append("- full 档是几十步串行出图+渲染，建议用 story-to-handdrawn-video 自己的 plan → generate → import → render 分阶段跑，不要一次性阻塞调用。")
    with open(prefix + "_render-notes.md", "w", encoding="utf-8") as f:
        f.write("\n".join(notes) + "\n")

    print(f"写入：{prefix}.txt")
    print(f"写入：{prefix}.visual-plan.json")
    print(f"写入：{prefix}_render-notes.md")
    print()
    print("下一步（在 story-to-handdrawn-video 项目里执行，先用 --mode plan 不花钱预检）：")
    print(f'  python3 scripts/run_story_video.py --input "{prefix}.txt" --title "{title}" '
          f'--visual-plan "{prefix}.visual-plan.json" --character-lock "<确认后的 character-lock 文本>" '
          f'--style <确认后的画风id> --mode plan')


if __name__ == "__main__":
    main()
