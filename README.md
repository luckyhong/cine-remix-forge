# Cine Remix Forge

给一个电影解说视频链接，或者直接给一个电影/剧集的名字，产出一份完整的深度创作文档：

1. **深度电影解说词**——8-16分钟、分幕+时间轴格式、有开篇钩子、有真实历史锚点、有跨作品对照、有自己的论点，不是剧情复述
2. **原创动画短片剧本**——主题上呼应这部电影，但世界观、人物、情节完全原创的寓言故事，每次生成都会换一个新的核心意象，不会重复
3. **创作手法对照表**——把两份成稿里用到的手法拆开列出来，方便自己复用这套方法论

这是一个 [Claude Code](https://claude.com/product/claude-code) skill 项目，核心逻辑都在 `.claude/skills/cine-remix/` 下。

## 怎么用

在装有 Claude Code、且已启用这个 skill 的环境里，直接给一个电影名字或者一条解说视频链接：

```
帮我写一份《XXX》的深度解说词，再配一个原创动画短片剧本
```

```
https://youtube.com/xxx 这个解说视频，帮我写一份更有深度的版本，再做个动画短片
```

skill 会自动判断输入类型（有链接就先抓取参考视频做轻量拆解，没链接就直接研究这部电影本身），然后按固定格式产出完整文档。

## 目录结构

```
.claude/skills/cine-remix/
├── SKILL.md                          # 核心工作流程和版权红线
├── scripts/
│   └── fetch_content.py              # 抓取参考解说视频的元数据/文案/评论（yt-dlp + 本地语音转写兜底）
├── references/
│   ├── script_format_guide.md        # 解说词格式规范 + 钩子设计方法论
│   ├── animation_fable_guide.md      # 原创动画寓言设计方法论
│   ├── used_concepts_log.md          # 已用过的动画载体意象记录，避免重复
│   └── output_template.md            # 最终文档拼装模板
└── examples/
    └── 我这一辈子_深度解说词与动画短片.md   # 一次真实产出，用作质量/格式校准参照
```

## 版权原则

这个 skill 的所有产出都必须是**原创评论 + 原创改编**，不是复制粘贴：

- 解说词可以自由讨论剧情和历史背景，但不大段逐字引用电影台词或原著文字
- 如果参考了别人的解说视频，只提炼"这类内容为什么有效"的方法论，不沿用具体论证和措辞
- 动画短片是完全虚构的新故事，只在主题上呼应原电影，人物、情节、世界观都是原创的

具体规则见 [`.claude/skills/cine-remix/SKILL.md`](.claude/skills/cine-remix/SKILL.md) 里的"版权红线"章节。

## 依赖

`fetch_content.py` 依赖 [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)，缺失时会自动尝试安装（优先 `brew`，其次 `pipx`，最后 `pip --user`）。只有在给了参考视频链接、且平台字幕/简介都拿不到有效文案时，才会触发本地语音转写兜底（[`faster-whisper`](https://github.com/SYSTRAN/faster-whisper)，同样按需自动安装），纯靠电影名字生成时不需要这套依赖。

## 项目状态

从 [ideas-exploration](https://github.com/) 项目里孵化出来的独立项目，核心方法论已经过几轮真实案例验证。
