<div align="center">

# 🎬 Cine Remix Forge

**有深度的电影解说词，全新的原创动画短片剧本——是重新创作，不是复制粘贴。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AGENTS.md](https://img.shields.io/badge/AGENTS.md-%E5%B7%A5%E5%85%B7%E4%B8%AD%E7%AB%8B-6b5b95)](AGENTS.md)
[![Python 3](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://www.python.org/)

[English](README.md)&nbsp;·&nbsp;简体中文

</div>

---

## 项目简介

给一个电影解说视频链接，或者直接给一个电影名字——不需要别的输入——**Cine Remix Forge** 就能产出一份完整的创作文档：

1. **深度解说词** —— 8-16分钟，分幕+时间轴结构，有开篇钩子，有经得起核实的历史/评论背景，至少一处跨作品对照。不是"剧情复述+感想"的拼接。
2. **原创动画短片剧本** —— 每次生成都是全新的寓言世界，主题上呼应原电影，但人物、设定、情节完全原创，不是换个媒介的翻拍。
3. **创作手法对照表** —— 把两份成稿里用到的手法（钩子、论点、对照角色、首尾呼应）拆开对应列出，让这套方法论本身可以被复用，而不只是拿到两篇成品。

整套工作流只在 [`AGENTS.md`](AGENTS.md) 里定义了一份，**不绑定任何一个具体的 AI 工具**。只要一个 agent 能读 markdown 文件、能跑 Python 脚本，就能执行这套流程。

## 支持哪些工具

| 工具 | 怎么接入 |
|---|---|
| **Claude Code** | 安装为 skill（放到 `~/.claude/skills/cine-remix/`，或者直接把仓库克隆下来打开）——`.claude/skills/cine-remix/SKILL.md` 会自动触发，内容指向 `AGENTS.md`。根目录的 `CLAUDE.md` 覆盖"没装成 skill、直接打开仓库"这种情况。也可以不依赖自动触发，直接用 `/cine-remix <请求>` 显式调用。 |
| **Codex CLI** 及其他支持 [agents.md](https://agents.md) 约定的工具 | 原生读取根目录的 `AGENTS.md`，不需要额外适配。 |
| **Cursor** | `.cursor/rules/cine-remix.mdc` 在匹配的请求上触发，内容指向 `AGENTS.md`。 |
| **GitHub Copilot** | `.github/copilot-instructions.md` 指向 `AGENTS.md`。 |
| **DeepSeek、GLM 等纯对话模型** | 这些是模型，不是有自己项目文件约定的工具——没有"安装"这一步。直接把 `AGENTS.md`（以及需要用到的 `references/*.md`）内容粘贴进对话即可；如果你是通过 Cline / Continue / opencode 这类已经支持 `AGENTS.md` 规则的通用 agent 工具去接入这些模型，那自动就能读到。 |

`AGENTS.md` 和 `references/` 里的内容都不依赖任何具体工具。上面这些针对各工具的文件，作用只是让每个工具"找到并遵循"这份workflow——真正的流程、版权规则、格式要求只在一个地方维护，不会在不同工具之间跑偏。

## 为什么做这个

大多数"视频拆解"类工具，最终停留在"把原内容换个说法重新说一遍"。这个项目押的是相反的方向：真正的价值在于拆出"它为什么有效"，再在这份理解之上造出全新的东西——而不是把已有内容重新包装一遍。仓库里的每一条约束（见下方[版权原则](#版权原则)）都是为了兑现这个方向而存在的。

## 快速开始

在上面任意一个工具里，指向这个仓库之后，直接说：

```text
帮我写一份《XXX》的深度解说词，再配一个原创动画短片剧本。
```

```text
https://youtube.com/watch?v=xxxx 这是一个电影解说视频，帮我写一份更有深度、更原创的版本，
再做一个动画短片改编。
```

在 Claude Code 里，也可以不依赖自动触发，直接指名调用：

```text
/cine-remix 帮我写一份《XXX》的深度解说词，再配一个原创动画短片剧本。
```

（`/skill名称` 这个语法是 Claude Code 特有的——上面列的其他工具都是靠描述匹配自动触发，没有统一的手动调用前缀。）

工作流会自动判断输入模式：

| 输入 | 会发生什么 |
|---|---|
| **只给电影名** | 模型直接研究这部电影（自身知识 + 必要时用网络搜索核实事实），不会去抓取任何视频 |
| **给了视频链接** | `scripts/fetch_content.py` 先抓取参考视频的元数据/转写文案/评论，但只是为了提炼"它用了什么手法"，不会沿用具体措辞 |

两条路径最终都汇入同一套产出流程：论点先行的结构设计 → 完整解说词 → 全新寓言构思（会先查是否和之前用过的重复）→ 完整动画剧本 → 创作手法对照表。

## 项目结构

```
AGENTS.md                             # 唯一权威来源：工作流、版权规则、产出格式要求
CLAUDE.md                             # 指向 AGENTS.md，覆盖"Claude Code 直接打开本仓库"的情况
scripts/
└── fetch_content.py                  # 参考视频抓取（yt-dlp + 本地语音转写兜底）
references/
├── script_format_guide.md            # 分幕格式、钩子设计模式、收尾方式
├── animation_fable_guide.md          # 寓言设计方法论：载体意象、循环结构、
│                                        对照角色、语气拿捏
├── used_concepts_log.md              # 已用过的动画核心意象记录（只追加不覆盖）
└── output_template.md                # 最终文档拼装模板
examples/
└── ...                                # 一次真实产出，作为质量基准留档
.claude/skills/cine-remix/SKILL.md    # Claude Code 适配入口 → 指向 AGENTS.md
.cursor/rules/cine-remix.mdc          # Cursor 适配入口 → 指向 AGENTS.md
.github/copilot-instructions.md       # Copilot 适配入口 → 指向 AGENTS.md
```

## 版权原则

这里的所有产出都是**原创评论 + 原创改编**，不是换个名字的复制品：

- 解说词可以自由讨论剧情、人物、历史（这是影评的常规操作），但不大段引用电影台词或原著文字——只做简短的、明确标注来源的引用。
- 抓取参考视频时，只提炼它的**手法**（钩子类型、节奏、论证结构），不沿用它的具体措辞、段子或论证过程。
- 动画短片是100%虚构的：新世界观、新角色、新情节。判断标准很简单——没看过原电影的人，不应该单看剧本就认出这是哪部电影。
- 真实的传记/历史事实可以自由引用（事实本身不受版权保护），但前提是模型有把握它是准确的——拿不准的细节要么留有余地，要么直接不用，绝不编造。

完整规则见 [`AGENTS.md`](AGENTS.md)。

## 依赖

`fetch_content.py` 依赖 [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)，缺失时会在首次使用时自动安装（依次尝试 `brew`、`pipx`、`pip --user`）。本地语音转写 [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) 只在参考视频既没有可用字幕、简介也不够充实时才会作为最后手段触发，且仅在"链接模式"下需要。纯靠电影名字生成时完全不需要额外依赖。

## 项目状态

在一次工作会话里，这套方法论经过多个真实电影案例验证后，从中孵化成了独立仓库——完整的一次真实产出可以看 `examples/` 目录。

## 许可证

[MIT](LICENSE)
