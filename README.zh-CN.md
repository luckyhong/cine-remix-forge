<div align="center">

# 🎬 Cine Remix Forge

**有深度的电影解说词，全新的原创动画短片剧本——是重新创作，不是复制粘贴。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-6b5b95)](https://claude.com/product/claude-code)
[![Python 3](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://www.python.org/)

[English](README.md)&nbsp;·&nbsp;简体中文

</div>

---

## 项目简介

给一个电影解说视频链接，或者直接给一个电影名字——不需要别的输入——**Cine Remix Forge** 就能产出一份完整的创作文档：

1. **深度解说词** —— 8-16分钟，分幕+时间轴结构，有开篇钩子，有经得起核实的历史/评论背景，至少一处跨作品对照。不是"剧情复述+感想"的拼接。
2. **原创动画短片剧本** —— 每次生成都是全新的寓言世界，主题上呼应原电影，但人物、设定、情节完全原创，不是换个媒介的翻拍。
3. **创作手法对照表** —— 把两份成稿里用到的手法（钩子、论点、对照角色、首尾呼应）拆开对应列出，让这套方法论本身可以被复用，而不只是拿到两篇成品。

它是一个 [Claude Code](https://claude.com/product/claude-code) **skill**——一份自包含的工作流定义，配合脚本和参考文档，Claude 在被调用时会照着执行。

## 为什么做这个

大多数"视频拆解"类工具，最终停留在"把原内容换个说法重新说一遍"。这个项目押的是相反的方向：真正的价值在于拆出"它为什么有效"，再在这份理解之上造出全新的东西——而不是把已有内容重新包装一遍。仓库里的每一条约束（见下方[版权原则](#版权原则)）都是为了兑现这个方向而存在的。

## 快速开始

在启用了这个 skill 的 Claude Code 会话里，直接说：

```text
帮我写一份《XXX》的深度解说词，再配一个原创动画短片剧本。
```

```text
https://youtube.com/watch?v=xxxx 这是一个电影解说视频，帮我写一份更有深度、更原创的版本，
再做一个动画短片改编。
```

skill 会自动判断输入模式：

| 输入 | 会发生什么 |
|---|---|
| **只给电影名** | Claude 直接研究这部电影（自身知识 + 必要时用网络搜索核实事实），不会去抓取任何视频 |
| **给了视频链接** | `scripts/fetch_content.py` 先抓取参考视频的元数据/转写文案/评论，但只是为了提炼"它用了什么手法"，不会沿用具体措辞 |

两条路径最终都汇入同一套产出流程：论点先行的结构设计 → 完整解说词 → 全新寓言构思（会先查是否和之前用过的重复）→ 完整动画剧本 → 创作手法对照表。

## 项目结构

```
.claude/skills/cine-remix/
├── SKILL.md                          # 工作流程、版权红线、产出硬性要求
├── scripts/
│   └── fetch_content.py              # 参考视频抓取（yt-dlp + 本地语音转写兜底）
├── references/
│   ├── script_format_guide.md        # 分幕格式、钩子设计模式、收尾方式
│   ├── animation_fable_guide.md      # 寓言设计方法论：载体意象、循环结构、
│   │                                   对照角色、语气拿捏
│   ├── used_concepts_log.md          # 已用过的动画核心意象记录（只追加不覆盖）
│   └── output_template.md            # 最终文档拼装模板
└── examples/
    └── ...                           # 一次真实产出，作为质量基准留档
```

## 版权原则

这里的所有产出都是**原创评论 + 原创改编**，不是换个名字的复制品：

- 解说词可以自由讨论剧情、人物、历史（这是影评的常规操作），但不大段引用电影台词或原著文字——只做简短的、明确标注来源的引用。
- 抓取参考视频时，只提炼它的**手法**（钩子类型、节奏、论证结构），不沿用它的具体措辞、段子或论证过程。
- 动画短片是100%虚构的：新世界观、新角色、新情节。判断标准很简单——没看过原电影的人，不应该单看剧本就认出这是哪部电影。
- 真实的传记/历史事实可以自由引用（事实本身不受版权保护），但前提是模型有把握它是准确的——拿不准的细节要么留有余地，要么直接不用，绝不编造。

完整规则见 [`SKILL.md`](.claude/skills/cine-remix/SKILL.md)。

## 依赖

`fetch_content.py` 依赖 [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)，缺失时会在首次使用时自动安装（依次尝试 `brew`、`pipx`、`pip --user`）。本地语音转写 [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) 只在参考视频既没有可用字幕、简介也不够充实时才会作为最后手段触发，且仅在"链接模式"下需要。纯靠电影名字生成时完全不需要额外依赖。

## 项目状态

在一次工作会话里，这套方法论经过多个真实电影案例验证后，从中孵化成了独立仓库——完整的一次真实产出可以看 `examples/` 目录。

## 许可证

[MIT](LICENSE)
