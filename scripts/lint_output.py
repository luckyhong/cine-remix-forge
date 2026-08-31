#!/usr/bin/env python3
"""Mechanical checks on an assembled cine-remix document.

Exists because Step 6's checklist had grown to 18 boxes plus Step 6.5's 7 written answers.
A 25-item list gets ticked wholesale on a "felt like I did all that" pass -- which is the exact
failure Step 6.5 was written to catch. Everything in here is machine-decidable, so it should be
run, not attested. What's left in the checklist is only what genuinely needs judgement.

Usage:  python3 scripts/lint_output.py <document.md>
Exit:   0 = clean, 1 = at least one FAIL.
"""
import re
import sys

CH = r'[一-鿿]'
BANNED_SHOT = ["镜头缓缓扫过", "快速闪回若干", "蒙太奇串起", "配合文案节奏切换"]
HOOK_EXPOSITION = ["导演", "改编自", "出品", "获奖", "金鸡", "百花", "编剧"]

FAILS, WARNS, OKS = [], [], []
def fail(m): FAILS.append(m)
def warn(m): WARNS.append(m)
def ok(m):   OKS.append(m)

def cn(s):
    return len(re.findall(CH, s))

def to_sec(ts):
    m, s = ts.split(":")
    return int(m) * 60 + int(s)


def parse_acts(doc):
    acts = []
    for blk in re.split(r"\n### ", doc):
        if not blk.startswith("【"):
            continue
        head = blk.split("\n")[0]
        m = re.match(r"【(\d+:\d+)\s*-\s*(\d+:\d+)】", head)
        if not m:
            continue
        body = re.search(r"\*\*【文案】\*\*(.*?)(?=\n\n|\Z)", blk, re.S)
        pic = re.search(r"\*\*【画面】\*\*(.*?)(?=\n\*\*|\n\n|\Z)", blk, re.S)
        acts.append({
            "title": head[:24],
            "start": to_sec(m.group(1)), "end": to_sec(m.group(2)),
            "text": body.group(1).strip() if body else "",
            "pic": pic.group(1).strip() if pic else "",
        })
    return acts


def check_acts(acts):
    if not acts:
        fail("没有解析到任何幕——检查 ### 【MM:SS-MM:SS】 标记格式")
        return
    cur = acts[0]["start"]
    for a in acts:
        if a["start"] != cur:
            fail(f"幕时间戳不连续：{a['title']} 应从 {cur//60}:{cur%60:02d} 起")
        cur = a["end"]
    total = acts[-1]["end"] - acts[0]["start"]
    if not (480 <= total <= 960):
        fail(f"总时长 {total//60}:{total%60:02d} 不在 8–16 分钟区间")
    else:
        ok(f"总时长 {total//60}:{total%60:02d}，{len(acts)} 幕")
    if not (5 <= len(acts) <= 7):
        warn(f"幕数 {len(acts)}，常规区间是 5–7 幕")

    body_all = 0
    for a in acts:
        dur = a["end"] - a["start"]
        n = cn(re.sub(r"[\*·/\[\]]", "", a["text"]))
        body_all += n
        density = n / (dur / 60)
        if n * 0.2 > dur * 1.1:
            fail(f"{a['title']} 文案超量：{n}字最快也念不完 {dur}s")
        elif density > 260:
            warn(f"{a['title']} 密度 {density:.0f} 字/分 偏高（>260，画面没有呼吸）")
        elif density < 200:
            warn(f"{a['title']} 密度 {density:.0f} 字/分 偏低（<200，留白过多）")
        # 气口段
        segs = [cn(x) for x in re.split(r"[，。；：？！、—…]+", re.sub(r"[\*·/]", "", a["text"])) if cn(x)]
        if segs and max(segs) > 40:
            fail(f"{a['title']} 有气口段 {max(segs)} 字 > 40（配音会断气）")
        # 加粗判断句
        bolds = re.findall(r"\*\*([^*]+)\*\*", a["text"])
        if len(bolds) != 1:
            warn(f"{a['title']} 加粗判断句 {len(bolds)} 处（每幕应恰好 1 处，且在幕末）")
        elif not a["text"].rstrip().endswith("**") and bolds[0] not in a["text"][-len(bolds[0]) - 80:]:
            warn(f"{a['title']} 加粗判断句不在幕末")
        # 画面：单一信源
        NUM = r"[0-9〇一二三四五六七八九十百两]+"
        for kw, why in ((NUM + r"\s*秒", "秒数"), (NUM + r"\s*个?镜头", "镜头数"), (r"\d+:\d+", "时间码")):
            if re.search(kw, a["pic"]):
                fail(f"{a['title']}【画面】出现{why}——时长信息只能在剪辑执行表里（七.0）")
        for b in BANNED_SHOT:
            if b in a["pic"]:
                fail(f"{a['title']}【画面】使用了禁用描述「{b}」（七.1④）")
    spoken = body_all * 0.24
    ok(f"全片文案 {body_all} 字；语速口径 {body_all/(spoken/60):.0f} 字/分，密度口径 {body_all/(total/60):.0f} 字/分")

    # 钩子
    h = acts[0]
    plain = re.sub(r"[\*·/\[\]]", "", h["text"])
    head15 = plain[:int(15 / 0.24)]
    hits = [w for w in HOOK_EXPOSITION if w in head15]
    if hits:
        fail(f"钩子前15秒出现背景介绍词 {hits}——导演/年份/获奖属于第二幕（2.1 C）")
    else:
        ok("钩子前 15 秒无背景介绍")


def check_delivery(doc):
    if "剪辑执行表" not in doc:
        fail("缺少剪辑交付块（素材清单 / 剪辑执行表 / 配音提示）")
        return
    sheet = doc.rsplit("剪辑执行表", 1)[1]
    rows = re.findall(r"^\| (\d+:\d+) \| (\d+)s \| ([^|]*) \|", sheet, re.M)
    if not rows:
        fail("剪辑执行表没有解析到数据行")
        return
    cur, gaps = 0, []
    for tc, d, _ in rows:
        ip = to_sec(tc)
        if ip != cur:
            gaps.append(f"{tc}（应为 {cur//60}:{cur%60:02d}）")
        cur = ip + int(d)
    if gaps:
        fail(f"剪辑执行表入点不连续：{'; '.join(gaps)}")
    else:
        ok(f"剪辑执行表 {len(rows)} 行，入点连续，加总 {cur//60}:{cur%60:02d}")

    acts = parse_acts(doc)
    if acts:
        total = acts[-1]["end"] - acts[0]["start"]
        if cur != total:
            fail(f"剪辑执行表加总 {cur}s ≠ 解说词总时长 {total}s")

    # 素材清单 <-> 执行表
    if "素材清单" in doc:
        man_blk = doc.rsplit("素材清单", 1)[1].split("剪辑执行表")[0]
        manifest = set(re.findall(r"^\|\s*\*{0,2}([SE]\d\d)", man_blk, re.M))
        used = set(re.findall(r"[SE]\d\d", "".join(r[2] for r in rows)))
        if manifest - used:
            fail(f"素材清单里有、执行表未使用：{sorted(manifest - used)}")
        if used - manifest:
            fail(f"执行表使用了、素材清单没有：{sorted(used - manifest)}")
        if not (manifest - used) and not (used - manifest):
            ok(f"素材清单 ↔ 执行表 双向一致（{len(manifest)} 条素材）")
        real_tc = re.findall(r"\|\s*\d+:\d+:\d+\s*\|", man_blk)
        if real_tc:
            fail(f"素材清单里有 {len(real_tc)} 处填好的原片时间码——必须留 ⬜ 待填，绝不编造")
        else:
            ok(f"原片时间码 {man_blk.count('⬜')} 处全部待填，无编造")


def check_header(doc):
    for field in ["外部查重", "关键细节查重", "三层反驳", "讲法查重", "事实清单"]:
        if field not in doc:
            fail(f"头部缺少必填声明：{field}")
    if "事实清单" in doc:
        rows = re.findall(r"^\| \d+ \|([^|]*)\|([^|]*)\|([^|]*)\|", doc.rsplit("事实清单", 1)[1], re.M)
        bad = [r for r in rows if ("一级" in r[1] or "二级" in r[1]) and "✅" not in r[2]]
        if bad:
            fail(f"事实清单有 {len(bad)} 条一级/二级未标 ✅")
        elif rows:
            ok(f"事实清单 {len(rows)} 条，一级/二级全部已核实")
    m = re.search(r"文字：([^\n]+)", doc)
    if "封面提案" not in doc:
        fail("缺少封面提案")
    elif m and cn(m.group(1)) > 12:
        fail(f"封面文字 {cn(m.group(1))} 字 > 12")
    else:
        ok("封面提案存在，文字长度合规")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    doc = open(sys.argv[1], encoding="utf-8").read()
    check_header(doc)
    check_acts(parse_acts(doc))
    check_delivery(doc)
    for m in OKS:
        print(f"  ok   {m}")
    for m in WARNS:
        print(f"  WARN {m}")
    for m in FAILS:
        print(f"  FAIL {m}")
    print(f"\n{len(OKS)} ok / {len(WARNS)} warn / {len(FAILS)} fail")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
