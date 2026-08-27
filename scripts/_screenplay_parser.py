"""Shared parser for cine-remix animated-short screenplays.

Used by both scripts/screenplay_to_prose.py (route 1: story-to-handdrawn-video)
and scripts/screenplay_to_video_prompts.py (route 2: Jimeng/Seedance-style
paste-ready prompts) so the parsing/safety logic only lives in one place.

Copyright/safety boundary: extract_animation_section() ONLY returns text
between the "## 二、原创动画短片剧本" heading and the "## 三、创作手法对照表"
heading. It never returns the "## 一、深度解说词" section, which legitimately
discusses the real source film/director/history and must never leak into
image/video-generation prompts. This is a structural parsing limit.
"""
import re

SECTION_START_RE = re.compile(r"^##\s*二、\s*原创动画短片剧本.*$", re.MULTILINE)
SECTION_END_RE = re.compile(r"^##\s*三、\s*创作手法对照表.*$", re.MULTILINE)
SCENE_HEADER_RE = re.compile(r"^###\s*Scene\s*(\d+)\s*[·\.]?\s*(.*)$")
PROJECT_FIELD_RE = re.compile(r"^-\s*\*\*(片名|时长|形式|基调)\*\*\s*[:：]\s*(.+)$")
# A "speaker: line" style dialogue line -- short leading label (<=12 chars,
# optionally with a parenthetical mood note), not one of the known
# narration/stage-direction labels.
DIALOGUE_RE = re.compile(r"^([^\s：:（(]{1,12})(?:（([^）]*)）)?\s*[：:]\s*(.+)$")
NARRATION_LABELS = {"画面", "音效", "字幕", "字卡", "旁白", "台词", "台词/旁白", "下一场", "镜头"}


def _looks_like_narration_label(speaker):
    """A real speaker name never contains sentence punctuation, and a
    narration line that happens to fit the DIALOGUE_RE shape (e.g. "画面切黑，
    字卡：...") always does, or contains one of NARRATION_LABELS as a
    substring even when prefixed by other text."""
    if any(p in speaker for p in "，、。"):
        return True
    return any(label in speaker for label in NARRATION_LABELS)

ROLE_KEYWORDS = {
    "open": ["开场", "冷开场"],
    "climax": ["高潮", "真相", "反转"],
    "loop": ["循环", "轮"],
    "close": ["尾声", "呼应", "收束", "结尾"],
}


class Scene:
    def __init__(self, num, title_raw):
        self.num = num
        self.title_raw = title_raw.strip()
        self.visual_lines = []
        self.dialogue = []  # list of (speaker, mood, content)

    @property
    def role(self):
        for role, kws in ROLE_KEYWORDS.items():
            if any(kw in self.title_raw for kw in kws):
                return role
        return "other"

    def raw_text_len(self):
        return sum(len(l) for l in self.visual_lines) + sum(len(c) for _, _, c in self.dialogue)


def extract_animation_section(doc_text):
    start_m = SECTION_START_RE.search(doc_text)
    if not start_m:
        raise ValueError('未找到 "## 二、原创动画短片剧本" 标题，无法定位动画剧本部分')
    end_m = SECTION_END_RE.search(doc_text, start_m.end())
    return doc_text[start_m.end():end_m.start()] if end_m else doc_text[start_m.end():]


def parse_project_info(section):
    info = {}
    for line in section.splitlines():
        m = PROJECT_FIELD_RE.match(line.strip())
        if m:
            info[m.group(1)] = m.group(2).strip()
    return info


def parse_characters(section):
    m = re.search(r"^###\s*人物\s*$", section, re.MULTILINE)
    if not m:
        return []
    rest = section[m.end():]
    next_section = re.search(r"^###\s", rest, re.MULTILINE)
    block = rest[:next_section.start()] if next_section else rest
    return [l.strip("- ").strip() for l in block.splitlines() if l.strip().startswith("-")]


def parse_scenes(section):
    lines = section.splitlines()
    scenes = []
    current = None
    for line in lines:
        stripped = line.strip()
        header_m = SCENE_HEADER_RE.match(stripped)
        if header_m:
            if current:
                scenes.append(current)
            current = Scene(int(header_m.group(1)), header_m.group(2))
            continue
        if current is None or not stripped:
            continue
        dm = DIALOGUE_RE.match(stripped)
        if dm and not _looks_like_narration_label(dm.group(1)):
            current.dialogue.append((dm.group(1), dm.group(2) or "", dm.group(3)))
        else:
            text = stripped
            for label in NARRATION_LABELS:
                prefix = f"**{label}**"
                if text.startswith(prefix):
                    text = text[len(prefix):].lstrip("：: ")
                    break
                if text.startswith(label + "：") or text.startswith(label + ":"):
                    text = text[len(label) + 1:].strip()
                    break
            current.visual_lines.append(text)
    if current:
        scenes.append(current)
    return scenes


def parse_screenplay(doc_text):
    """Convenience wrapper: returns (project_info, characters, scenes)."""
    section = extract_animation_section(doc_text)
    return parse_project_info(section), parse_characters(section), parse_scenes(section)
