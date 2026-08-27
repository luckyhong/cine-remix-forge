#!/usr/bin/env python3
"""Fetch metadata + transcript for a short-video URL (YouTube/Douyin/etc.) via yt-dlp.

Tiered transcript strategy, cheapest and most reliable first:
  1. Platform-provided subtitles/captions (works well on YouTube).
  2. The video's own description/caption text -- on Douyin/Xiaohongshu, creators
     very often paste their full voiceover script as the post caption, so this is
     frequently all that's needed and costs nothing.
  3. Local ASR on the extracted audio (faster-whisper), only when 1 and 2 are both
     too thin to reconstruct the spoken content from.

Everything runs locally -- no paid transcription APIs are used. Missing CLI deps
(yt-dlp) are installed on demand via pip; the ASR fallback (faster-whisper) is only
installed/invoked if actually needed, since it pulls a larger model file.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def pip_install(*packages):
    """Install into the user site-packages, working around PEP 668
    'externally managed environment' guards on Homebrew/Debian Pythons."""
    r = run([sys.executable, "-m", "pip", "install", "--user", "-q", *packages])
    if r.returncode == 0:
        return True
    r = run([sys.executable, "-m", "pip", "install", "--user", "--break-system-packages", "-q", *packages])
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return False
    return True


def ensure_yt_dlp():
    if shutil.which("yt-dlp"):
        return True
    print("[setup] yt-dlp not found, installing...", file=sys.stderr)
    if shutil.which("brew"):
        r = run(["brew", "install", "yt-dlp"])
        if r.returncode == 0 and shutil.which("yt-dlp"):
            return True
    if shutil.which("pipx"):
        r = run(["pipx", "install", "yt-dlp"])
        if r.returncode == 0 and shutil.which("yt-dlp"):
            return True
    return pip_install("yt-dlp") and shutil.which("yt-dlp") is not None


def get_metadata(url, workdir):
    r = run(["yt-dlp", "--dump-single-json", "--no-warnings", "--skip-download", url], cwd=workdir)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def get_subtitles(url, workdir):
    sub_langs = "zh-Hans,zh-Hant,zh,en,en-US"
    run([
        "yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
        "--sub-langs", sub_langs, "--sub-format", "vtt/srt/best",
        "--convert-subs", "srt", "-o", os.path.join(workdir, "sub.%(ext)s"),
        url,
    ])
    srt_files = [f for f in os.listdir(workdir) if f.endswith(".srt")]
    if not srt_files:
        return None
    lines = []
    with open(os.path.join(workdir, srt_files[0]), encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.isdigit() or "-->" in line:
                continue
            lines.append(line)
    return "\n".join(lines) if lines else None


def get_comments(url, workdir, limit=15):
    r = run([
        "yt-dlp", "--dump-single-json", "--no-warnings", "--skip-download",
        "--write-comments",
        "--extractor-args", f"youtube:max_comments={limit},comment_sort=top",
        url,
    ], cwd=workdir, timeout=60)
    if r.returncode != 0:
        return []
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return []
    comments = (data or {}).get("comments") or []
    out = []
    for c in comments[:limit]:
        text = (c.get("text") or "").strip()
        if text:
            out.append({"text": text, "likes": c.get("like_count", 0)})
    return out


_METADATA_MARKERS = ("导演:", "导演：", "编剧:", "编剧：", "主演:", "主演：", "imdb",
                     "类型:", "类型：", "制片", "又名:", "又名：", "上映日期")


def looks_like_real_transcript(text):
    """Descriptions on review/commentary channels (film reviews, book reviews,
    product breakdowns) are very often just a structured info block -- cast list,
    release date, IMDb link, one hook sentence -- not the creator's actual spoken
    script. That block can easily be >80 chars while containing near-zero of the
    creator's own narration, so raw length alone is not a reliable signal here."""
    if not text:
        return False
    lowered = text.lower()
    marker_hits = sum(1 for m in _METADATA_MARKERS if m in lowered)
    return len(text) > 80 and marker_hits < 2


def maybe_asr(url, workdir, existing_text):
    if looks_like_real_transcript(existing_text):
        return None, "skipped (enough text already available from captions/description)"
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("[setup] faster-whisper not found, installing (one-time, plus a small model download on first use)...", file=sys.stderr)
        if not pip_install("faster-whisper"):
            return None, "unavailable (pip install faster-whisper failed)"
        try:
            from faster_whisper import WhisperModel
        except ImportError as e:
            return None, f"unavailable (faster-whisper still not importable after install: {e})"

    if not shutil.which("ffmpeg"):
        return None, "unavailable (ffmpeg is required for audio extraction but was not found)"

    audio_path = os.path.join(workdir, "audio.%(ext)s")
    r = run(["yt-dlp", "-f", "bestaudio", "-x", "--audio-format", "mp3", "-o", audio_path, url])
    audio_files = [f for f in os.listdir(workdir) if f.startswith("audio.")]
    if r.returncode != 0 or not audio_files:
        return None, "failed (could not download/extract audio track)"

    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(os.path.join(workdir, audio_files[0]), language=None)
    text = " ".join(seg.text.strip() for seg in segments).strip()
    return (text or None), "local ASR (faster-whisper, small model, CPU)"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url", help="Video URL (YouTube, Douyin, etc. -- anything yt-dlp supports)")
    ap.add_argument("--no-asr", action="store_true", help="never fall back to local ASR, even if no text is found")
    ap.add_argument("--out", default=None, help="write JSON result to this path instead of stdout")
    args = ap.parse_args()

    if not ensure_yt_dlp():
        print(json.dumps({"error": "yt-dlp unavailable and could not be installed"}))
        sys.exit(1)

    with tempfile.TemporaryDirectory() as workdir:
        meta = get_metadata(args.url, workdir)
        if meta is None:
            print(json.dumps({"error": "failed to fetch video metadata -- check the URL and network connection"}))
            sys.exit(1)

        subtitle_text = get_subtitles(args.url, workdir)
        description = (meta.get("description") or "").strip()

        transcript_text, transcript_source = None, None
        if subtitle_text and len(subtitle_text) > 40:
            transcript_text, transcript_source = subtitle_text, "platform subtitles/captions"
        elif looks_like_real_transcript(description):
            transcript_text, transcript_source = description, "video description/caption text"

        asr_note = "not attempted"
        if not args.no_asr and (not transcript_text or len(transcript_text) < 80):
            asr_text, asr_note = maybe_asr(args.url, workdir, transcript_text)
            if asr_text:
                transcript_text, transcript_source = asr_text, asr_note

        comments = get_comments(args.url, workdir)

        result = {
            "url": args.url,
            "title": meta.get("title"),
            "uploader": meta.get("uploader") or meta.get("channel"),
            "duration_seconds": meta.get("duration"),
            "view_count": meta.get("view_count"),
            "like_count": meta.get("like_count"),
            "comment_count": meta.get("comment_count"),
            "description": description,
            "transcript_source": transcript_source or "none found",
            "transcript_text": transcript_text or "",
            "asr_fallback_status": asr_note,
            "top_comments": comments,
        }

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"Wrote {args.out}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
