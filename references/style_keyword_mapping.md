# 视觉风格关键词 → story-to-handdrawn-video 画风映射表

`scripts/screenplay_to_prose.py` 用这张表，把动画剧本"项目信息 → 形式（视觉风格关键词）"里的描述，对照到 `story-to-handdrawn-video` 内置的20种画风上，**推荐3-5个候选**，不直接锁定一个——具体选哪个交给用户确认。

## 内置20种画风（id / 中文名）

1. `colored-pencil-diary` 彩铅日记漫画（锁定默认，什么都匹配不上时兜底用这个）
2. `minimal-line-explainer` 极简黑白线条讲解
3. `kid-crayon` 五岁儿童蜡笔坏画
4. `rawkid-crayon` 潦草家庭投稿蜡笔
5. `bean-doodle-infographic` 小豆人涂鸦信息图
6. `ms-paint-bad-doodle` 鼠标烂涂鸦
7. `ballpoint-scribble` 圆珠笔缠绕线速写
8. `real-crayon-paper` 真实蜡笔纸实拍
9. `ink-wash` 水墨写意
10. `emotional-watercolor-sketch` 情绪叙事淡彩速写
11. `retro-gouache-concept` 中古动画水粉概念稿
12. `sunlit-storybook` 暖光童画绘本
13. `nordic-gouache-storybook` 北欧低饱和水粉绘本
14. `inked-storybook` 墨线淡彩绘本
15. `warm-flat-storybook` 暖色几何扁平绘本
16. `naive-marker-notes` 稚拙马克笔笔记
17. `zine-riso-collage` Zine 孔版拼贴
18. `organic-contour-doodle` 有机轮廓品牌涂鸦
19. `whiteboard-explainer` 白板讲解动画
20. `linocut-editorial` 粗粝木刻社论插画

## 关键词聚类 → 候选画风

匹配逻辑：在剧本的"视觉风格关键词"字段里查这些聚类词（同义词、近义词都算），命中哪一类就把对应的候选画风加进推荐列表；命中多类就取并集，按下表顺序去重，只保留前5个。一个都没命中就只推荐 `colored-pencil-diary`。

| 关键词聚类（剧本里常出现的描述） | 候选画风（按契合度排序） |
|---|---|
| 剪影 / 皮影 / 木偶 / 提线 / 偶动画 | `linocut-editorial`, `ink-wash`, `organic-contour-doodle` |
| 寓言 / 绘本 / 治愈 / 温情 | `sunlit-storybook`, `warm-flat-storybook`, `nordic-gouache-storybook` |
| 沉重 / 严肃 / 历史感 / 年代感 / 做旧 | `retro-gouache-concept`, `inked-storybook`, `emotional-watercolor-sketch` |
| 荒诞 / 戏谑 / 黑色幽默 / 反讽喜剧 | `ms-paint-bad-doodle`, `bean-doodle-infographic`, `rawkid-crayon` |
| 官僚 / 讽刺 / 社论感 / 批判性 | `linocut-editorial`, `whiteboard-explainer`, `zine-riso-collage` |
| 儿童视角 / 天真 / 反差萌 | `kid-crayon`, `rawkid-crayon`, `real-crayon-paper` |
| 水墨 / 东方 / 古典意境 | `ink-wash`, `retro-gouache-concept` |
| 极简 / 概念先行 / 说明性 / 图解 | `minimal-line-explainer`, `whiteboard-explainer`, `bean-doodle-infographic` |
| 复古 / 怀旧 / 褪色 / 中古 | `retro-gouache-concept`, `nordic-gouache-storybook`, `real-crayon-paper` |
| 拼贴 / 独立杂志感 / 版画质感 | `zine-riso-collage`, `naive-marker-notes` |
| 日记体 / 私人化 / 手记感 | `colored-pencil-diary`, `emotional-watercolor-sketch`, `naive-marker-notes` |

## 推荐话术模板

脚本给出候选时，按这个格式打印，让用户确认或改选：

```
根据剧本风格关键词"<原文>"，推荐以下画风（按契合度排序），回复编号或名称确认，或直接说你想用的画风：
1. linocut-editorial（粗粝木刻社论插画）
2. ink-wash（水墨写意）
3. organic-contour-doodle（有机轮廓品牌涂鸦）
不确定的话，默认会用 colored-pencil-diary（彩铅日记漫画）。
```
