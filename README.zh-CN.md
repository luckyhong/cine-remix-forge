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

文档一定会存成真正的 `.md` 文件——存哪会问你（见[产出与存放位置](#产出与存放位置)）；动画短片还可以再往前一步，做成真正的视频（见[可选功能：把动画短片渲染成视频](#可选功能把动画短片渲染成视频)）。

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

## 叙述人设

解说词不是只有一种腔调。写钩子之前，工作流会先定一个**叙述人设**——不同人设会用不同的方式写开篇钩子、幕间转折句、结尾收尾。论点层层反转的深度产出方法、幕结构、版权规则在所有人设下都保持一致——变的只是"声音"。每个人设的完整措辞规则见 [`references/narration_style_library.md`](references/narration_style_library.md)。

| # | 人设 | 声音特点 |
|---|---|---|
| 1 | **严肃反转型**（默认） | 有分量的论点反转——加粗判断句、克制的直接称呼 |
| 2 | 学术严谨型 | 冷静克制、重证据——读起来像一篇讲究的影评 |
| 3 | 犀利吐槽型 | 辛辣敢损——但笑点绝不落在情感高潮上 |
| 4 | 温情人文型 | 贴近角色、情感真挚——收尾更像一封信 |
| 5 | 悬疑节奏型 | 短句、留白——每一幕结尾都是一个钩子 |

如果你的请求里已经带了语气信号（比如"写个吐槽向的""再悬疑一点"），会直接匹配对应人设，不用追问。没有信号的话，会照下面[存放位置提问](#产出与存放位置)一样的模式（编号选项 + 写明默认值）问你一次；没人回答或非交互场景默认用人设1，不主动选就不会有任何变化。

## 产出与存放位置

组装好的文档一定会存成真正的 `.md` 文件——绝不会只留在聊天记录里。写好之后会问你存哪：

```text
《XXX》的深度解说词和动画短片剧本都写好了，存到哪？
A) 当前目录（...）
B) 当前目录下的 works/（...，如果不存在会新建）
C) 你自己指定一个路径
```

如果没人回答（比如非交互式/无人值守的运行场景），会回退到一个合理的默认值——当前目录下如果有 `works/` 这类文件夹就用它，没有就用当前目录——保证不管有没有人回复，文件都一定会生成。

## 可选功能：把动画短片渲染成视频

下面这些都是**可选的**——两份文字成稿才是默认产出，除非你明确提出要求，不会自动触发渲染，因为渲染更慢，有时候还有真实的生成成本。

| 路线 | 需要什么 | 能得到什么 |
|---|---|---|
| **路线一——手绘风 Remotion 视频** | 一个单独安装好的 `story-to-handdrawn-video` Claude Code skill（不属于这个仓库——是另一个项目，你的机器上要提前装好） | `scripts/screenplay_to_prose.py` 把剧本转成那个工具要的散文格式（自动生成它需要的 `--character-lock` 和 `--visual-plan`，并对照 `references/style_keyword_mapping.md` 从它内置的20种画风里推荐3-5个候选），产出一份**静音**、**竖屏3:4** 的 MP4。渲染范围每次都会先问你——`teaser`（约1场）、`highlight`（约4场，推荐）、`full`（全部场次，会明确提醒很慢）——可以先跑 `--scope preview` 看真实的场次选择和镜头数再决定。 |
| **路线二——更丰富的AI视频生成提示词** | 不需要任何依赖，纯文本产出 | `scripts/screenplay_to_video_prompts.py` 给每一场戏生成一段可以直接粘贴使用的提示词，供你手动放进即梦、Seedance或类似的文生视频工具。没有接API、没有浏览器自动化、没有凭证——这台机器目前还没接上这些，所以这一步就设计成手动操作（`references/video_render_routes.md` 里记录了后续自动化的路线图，还没实现）。 |

两个脚本共用同一个版权安全解析器（`scripts/_screenplay_parser.py`）：只读取组装文档里动画短片那一段，绝不读取讨论真实电影的解说词部分。

## 项目结构

```
AGENTS.md                             # 唯一权威来源：工作流、版权规则、产出格式要求
CLAUDE.md                             # 指向 AGENTS.md，覆盖"Claude Code 直接打开本仓库"的情况
scripts/
├── fetch_content.py                  # 参考视频抓取（yt-dlp + 本地语音转写兜底）
├── _screenplay_parser.py             # 路线一/二共用的版权安全剧本解析器
├── screenplay_to_prose.py            # 路线一：剧本 → story-to-handdrawn-video 输入格式
└── screenplay_to_video_prompts.py    # 路线二：剧本 → 即梦/Seedance 可粘贴提示词
references/
├── script_format_guide.md            # 分幕格式、钩子设计模式、收尾方式
├── narration_style_library.md        # 解说人设风格库：各人设的钩子/转折句/收尾措辞变体
├── animation_fable_guide.md          # 寓言设计方法论：载体意象、循环结构、
│                                        对照角色、语气拿捏
├── used_concepts_log.md              # 已用过的动画核心意象记录（只追加不覆盖）
├── output_template.md                # 最终文档拼装模板
├── video_render_routes.md            # 路线一/二具体机制、渲染范围分档、路线图
└── style_keyword_mapping.md          # 剧本风格关键词 → story-to-handdrawn-video 画风id映射表
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
- 这条边界延伸到视频渲染环节：两个转换脚本都只读取组装文档里动画短片那一段，绝不读取解说词部分。

完整规则见 [`AGENTS.md`](AGENTS.md)。

## 依赖

`fetch_content.py` 依赖 [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)，缺失时会在首次使用时自动安装（依次尝试 `brew`、`pipx`、`pip --user`）。本地语音转写 [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) 只在参考视频既没有可用字幕、简介也不够充实时才会作为最后手段触发，且仅在"链接模式"下需要。纯靠电影名字生成时完全不需要额外依赖。

`screenplay_to_video_prompts.py`（路线二）除了 Python 3 之外不需要任何依赖——它只产出文本。`screenplay_to_prose.py`（路线一）本身也只需要 Python 3，但它产出的内容要真正渲染成视频，需要另外单独搭建好 `story-to-handdrawn-video` 这个项目/skill（Node 20+、ffmpeg，以及一个出图后端）——这部分不在本仓库范围内。

## 项目状态

在一次工作会话里，这套方法论经过多个真实电影案例验证后，从中孵化成了独立仓库——完整的一次真实产出可以看 `examples/` 目录。

## 路线图

后续想法（选题差异化校验、对应原片真实时间戳辅助剪辑、多语言产出、多智能体事实核查等）都记录在 [`ROADMAP.md`](ROADMAP.md) 里——是持续累积的清单，不是承诺的开发计划。

## 许可证

[MIT](LICENSE)
