---
title: "AI 日报 2026.07.14（第二波）：造视频、管Agent、守隐私——这三款新工具各有一手"
date: 2026-07-14
author: "小糊涂虫"
tags: [AI日报, vox-director, plandeck, Local-Recall, AI视频, Agent看板, 本地化AI, 隐私]
description: "从 Vox 风格视频自动生成到 AI Agent 可视化看板，再到本地化的 Windows Recall 替代——今天第二篇日报带你看看三款在新赛道上各显神通的开源项目"
---

# AI 日报 2026.07.14（第二波）

> 第一篇聊了「反 AI 味」的三个项目，这篇换个口味——看看那些 **让 AI 做不一样的事** 的新工具。从自动化视频创作到 Agent 的可视化计划看板，再到拿回隐私权的本地屏幕记忆，三个方向，三种思路，都挺有意思。话不多说，直接开看！

---

## 🎬 Vox Director — 输入一个主题，输出一条 Vox 风格科普视频

**★ 98 | 4 天 | Python | [Alisa0808/vox-director](https://github.com/Alisa0808/vox-director)**

还记得 Vox 的那种剪报风格科普视频吗？拼贴纸片、撕纸边缘、黑白网点、醒目的大字标题配上旁白和音乐——一眼就能认出来的视觉语言。

**Vox Director** 是一个 Agent Skill，你丢给它一个主题，它帮你走完从脚本到成片的全部管线：

```
主题：墨西哥街头小吃
  ↓
① 设计叙事弧线 → 分镜头脚本 (你审)
  ↓
② 风格对决 → 按 3-4 种视觉风格生成预览 (你选)
  ↓
③ 逐帧生成 → 每个镜头一张拼贴海报
  ↓
④ 动画化 → 海报动起来，配上运镜
  ↓
⑤ 配音 + 字幕 + 背景音乐
  ↓
✅ 一条完成的 MP4！
```

项目配了三个带视频的 demo 可以参考：
- **"Mexican street food"** — 60 秒横屏
- **"The evolution of Chinese civilization"** — 30 秒横屏
- **"A brief history of money"** — 60 秒竖屏

### 值得关注的几点

**不是一键无脑生成。** 管线里有两个「关卡」（Gate）：第一步的叙事弧线要你点头才往下走，第二步的风格对决让你肉眼挑色调——这是对的，自动化的上限由人的判断力封顶。

**依赖 Atlas Cloud 做图像生成。** 底层用 Atlas Cloud 的 API + 本地 ffmpeg 渲染。这意味着你需要一个 Atlas Cloud 账号和 API Key，不是完全免费的，但相较于用专业团队做一条同质量的科普视频，成本已经不是一个量级了。

**Agent Skill 的形态。** 它是以 Agent Skill 发布的——给你的 Claude Code / Codex 装一个，然后在编辑器里说「做一个关于黑洞的 Vox 视频」，它就开始跑工作了。

> 一句话：如果你做内容运营、科普自媒体或者品牌传播，这个工具值得留意。目前还只是 R1 版本，想法本身比实现更有价值——「把一种成熟的视频风格自动化」这件事，才刚刚开始。生成一条 60 秒视频的成本从几万元的制作费降到了 AI API 的几分钱。

---

## 📋 Plandeck — 让你的 AI Agent 有个看得见的计划看板

**★ 20 | 2 天 | JavaScript | [OthmanAdi/plandeck](https://github.com/OthmanAdi/plandeck)**

这个项目的 README 第一句就把痛点说得明明白白：

> **"没人想读 Markdown 计划，也没人想盯着一堆原始 HTML 看 Agent 跑一个小时。"**

说的就是你吧。让 Agent 执行一个长任务，它列了一堆 TODO，但：

- 上下文压缩一次，掉一半进度
- 分不清哪个任务在等什么
- 它自己猜下一步做什么，经常猜错

**Plandeck 的解法：把 Agent 的计划变成一个交互式看板。**

不是花里胡哨的 SaaS 页面，而是一个**纯文件**方案——计划存在磁盘上的一个文件里，Agent 自己读、自己更新。看板会自动处理依赖关系：

```
C001 → 阻塞 → C002 → 阻塞 → C003
                     ↓
                  就绪  ← C004 在这里等着
```

- 依赖解锁后自动变成 Ready
- 关键路径高亮显示（金色）
- 永远只有一个「下一步」是明确的
- 不怕 `/clear`——文件在硬盘上，Agent 重启后还能接上

**实现方式**：零依赖，就是一个 Agent Skill + CLI。装到 Claude Code 后用它创建计划，看板自动生成，Agent 根据看板状态决定下一步做什么。团队协作的时候就提交那个计划文件到 git，谁都能看到进度。

### 为什么它值得关注

这其实解决了一个 Agent 领域的大问题：**规划的执行追踪**。现在大多数 Agent 要么列个 Markdown checklist，要么做一个超长思考把整个计划塞进上下文，前者不靠谱，后者浪费 token。Plandeck 用文件当持久层，用看板当接口，思路很对。

还有一个很聪明的设计细节：**计划的文件格式是标准化的 JSON**，不是私有的二进制格式。这意味着你可以把计划文件提交到 git，做 Code Review，甚至写脚本批量分析和改进 Agent 的计划——一个以前没人想到的「Agent 开发运维」的新维度。

当然只有 20 个 Star 说明还在很早期，但想法的成熟度超越了很多有几百 Star 的工具。

> 一句话：如果你经常让 Agent 跑长时间的任务（自动化测试、代码重构、调研报告），Plandeck 能让你看清楚它到底在干什么，而不是对着终端干等。

---

## 💾 Local Recall — 把微软 Recall 拿过来，全部跑在本地

**★ 14 | 1 天 | Python | [anshupriyan/Local-Recall](https://github.com/anshupriyan/Local-Recall)**

微软去年推出的 Recall 功能闹得沸沸扬扬——AI 定时截屏、存下来让你搜索回看，想法很棒，但隐私问题让人不放心（截图加密后还是上传云端了）。

**Local Recall 要做的事：同款功能，全部本地跑。**

### 架构管线

```
每 5 秒截屏
  ↓ 感知哈希去重（相同画面跳过）
  ↓
WinRT OCR 提取文字
  ↓
sentence-transformers 生成 384 维向量
  ↓
SQLite + sqlite-vec 存向量（子 50ms 语义搜索）
  ↓
对接本地 LM Studio（Qwen 2.5-7B）
  → 自然语言对话式查询你的屏幕历史
```

**关键区别**：一切在本地完成，零云端通信。OCR 不用云 API（用 Windows 内置的 WinRT OCR），向量存 SQLite，LLM 靠 LM Studio 本地跑。

### 目前状态

⚠️ **早期原型**，1 天前才发到 GitHub。只有 Windows 版（依赖 WinRT OCR），Linux 吃不上。项目结构清晰但是要走的路还长——

- 需要更好的存储管理（截屏久了吃空间）
- 目前只支持 LM Studio 做 RAG 查询
- 去重算法还是最简单的哈希对比

但方向非常对：**AI 功能不一定要上云。** 有些东西——特别是涉及你屏幕上的所有操作——天然应该留在本地。这个项目现在是唯一一个认真在做这件事的开源项目。如果它能解决存储效率和跨平台的问题，Windows Recall 的隐私争议可能就会促成一个更健康的替代方案。

> 一句话：如果你对微软 Recall 的功能心动但对隐私担忧，关注这个项目。它现在还跑不起来（你装了依赖也得折腾一会儿），但如果持续开发下去，会是 privacy-first AI 的一个重要方向。

---

## 📊 快讯速览

这波还有几个有趣的：

| 项目 | ★ | 一句话 |
|------|---|--------|
| **[morphe-ai](https://github.com/Paresh-Maheshwari/morphe-ai)** | 86 | AI 驱动的 Android APK 修改工作流——反编译→分析→改→重打包全自动 |
| **[Zer0Fit](https://github.com/porespellar/Zer0Fit)** | 18 | 用 MCP 协议接入 Google TimesFM 2.5，丢个 CSV 就能做零样本时间序列预测 |
| **[zabt-ai](https://github.com/afeef/zabt-ai)** | 14 | 自托管会议智能——转录（faster-whisper）+ 说话人分离 + LLM 摘要，Otter.ai 的开源替代 |
| **[awesome-gemini-cli-subagents](https://github.com/JosephHampton/awesome-gemini-cli-subagents)** | 37 | Gemini CLI 的 51 个生产级子 Agent 合集 |

---

## 💭 一点总结

今天两篇文章加起来，刚好看到 AI 生态的几个不同切面：

- **第一篇**：AI 用太多了，该去 AI 味了（kill-ai-slop / 說人話）
- **第二篇**：AI 还在长出新玩法（vox-director 做视频 / plandeck 管计划 / Local-Recall 守隐私）

AI 远没有「卷到头」。大家都还在试新的事情——问题不是 AI 能不能做，而是**怎么做才顺眼、才靠谱、才让人放心放下戒备去用**。

今天的日报到此为止。两篇加起来，基本覆盖了这周 GitHub 上最有意思的 AI 新面孔。明天见～☕
