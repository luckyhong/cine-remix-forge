#!/usr/bin/env python3
"""Convert a cine-remix animated-short screenplay into a ready-to-paste
prompt document for text-to-video web tools (Jimeng/即梦, Seedance, or
similar) -- Route 2 "Phase 1" from references/video_render_routes.md.

There is no API/MCP integration for these tools in this environment, so this
script does NOT call anything -- it only writes a markdown file with one
self-contained prompt block per screenplay scene, meant to be copied by hand
into whichever tool the user picks.

Unlike scripts/screenplay_to_prose.py (route 1), this does not force a
5-second-single-sentence beat structure -- these tools' web UIs take richer
per-shot prompts, so one block = one screenplay scene, no scope tiers needed.

Copyright/safety boundary: shares scripts/_screenplay_parser.py with route 1,
so it only ever reads the animated-short section of the assembled document,
never the real-film commentary section. See references/video_render_routes.md.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _screenplay_parser import parse_screenplay  # noqa: E402

CAMERA_BY_ROLE = {
    "open": "建立镜头，缓慢推进（establishing shot, slow push-in）",
    "loop": "固定机位，尽量与前一轮循环构图一致，强调重复感（locked-off, mirror previous iteration's framing）",
    "climax": "缓慢推向人物面部特写（slow push-in to close-up on face）",
    "close": "缓慢拉远至全景（slow pull-back to wide shot）",
    "other": "中景，随画面描述调整（medium shot, follow the scene description）",
}


def dialogue_to_subtitle_instruction(dialogue):
    if not dialogue:
        return None
    lines = []
    for speaker, mood, content in dialogue:
        content = content.strip().strip('"“”')
        mood_part = f"（{mood}）" if mood else ""
        lines.append(f'  - {speaker}{mood_part}："{content}"')
    return "画面中以字幕形式呈现以下台词（是否配音由具体工具决定，这里只给字幕文本）：\n" + "\n".join(lines)


def build_bible(project_info, characters):
    lines = ["## 风格/角色设定（每个场次生成前先看一遍，保持全片一致）", ""]
    if project_info.get("形式"):
        lines.append(f"- 视觉风格：{project_info['形式']}")
    if project_info.get("基调"):
        lines.append(f"- 基调：{project_info['基调']}")
    if characters:
        lines.append("- 角色：")
        lines.extend(f"  - {c}" for c in characters)
    return "\n".join(lines)


def build_scene_block(scene, idx):
    visual = "".join(scene.visual_lines).strip()
    lines = [
        f"### 场次 {idx} · {scene.title_raw}",
        "",
        f"**画面描述**：{visual}",
        f"**建议运镜**：{CAMERA_BY_ROLE.get(scene.role, CAMERA_BY_ROLE['other'])}",
    ]
    subtitle = dialogue_to_subtitle_instruction(scene.dialogue)
    if subtitle:
        lines.append(f"**字幕**：\n{subtitle}")
    lines.append("")
    lines.append("*(粘贴时请在提示词开头带上上方「风格/角色设定」内容，保持跨场次一致性)*")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("doc_path", help="assembled cine-remix markdown document (contains the animated-short section)")
    ap.add_argument("--out-dir", default=None, help="directory to write output to (default: same dir as doc_path)")
    args = ap.parse_args()

    with open(args.doc_path, encoding="utf-8") as f:
        doc_text = f.read()

    project_info, characters, scenes = parse_screenplay(doc_text)
    if not scenes:
        print("没有解析到任何 Scene，检查文档格式是否匹配 references/animation_fable_guide.md 的模板。", file=sys.stderr)
        sys.exit(1)

    title = project_info.get("片名", "untitled").strip("《》") or "untitled"
    out_dir = args.out_dir or os.path.dirname(os.path.abspath(args.doc_path))
    out_path = os.path.join(out_dir, f"{title}_video_prompts.md")

    parts = [
        f"# 《{title}》文生视频提示词（即梦 / Seedance / 类似工具，手动粘贴使用）",
        "",
        "> 这份文件不锁定具体平台，也不是自动化脚本的产物——本机没有接入任何文生视频 API，"
        "这里只生成可以直接复制粘贴进网页版工具的提示词。逐场次粘贴，注意每次都带上下面的风格/角色设定，"
        "保持跨场次一致性。",
        "",
        build_bible(project_info, characters),
        "",
        "---",
        "",
    ]
    for i, scene in enumerate(scenes, start=1):
        parts.append(build_scene_block(scene, i))
        parts.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    print(f"写入：{out_path}（共 {len(scenes)} 个场次的提示词）")


if __name__ == "__main__":
    main()
