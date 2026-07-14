---
title: "AI 日报 2026.07.14（第三波）：截获App、洗脑AI、扒吉他谱——今天最野的三个开源项目"
date: 2026-07-14
author: "小糊涂虫"
tags: [AI日报, mimic, J-Wash, 吉他谱, YouTube, Jacobian Lens, LLM编辑, 网络安全]
description: "799★ 的 mimic 让你用 Python 调用任何 App 的 API；J-Wash 让你给 LLM「洗脑」改行为；YouTube Guitar Tab Parser 把吉他教学视频自动转成 PDF 谱子——今天第三篇，全是硬核好货"
---

# AI 日报 2026.07.14（第三波）

> 前两篇聊了「反 AI 味」和「AI 新玩法」，第三篇咱们上硬菜。今天 GitHub 冒出了几个脑洞大开的东西——有截获 App 流量的神器、有给大模型「洗脑」的工具、还有用 AI 视觉帮你扒吉他谱的 CLI。三款都不走寻常路，一个个来看。

---

## 🕵️ mimic — 把任何 App 变成你的 Python 库

**★ 799 | 1 天 | Python | [littledivy/mimic](https://github.com/littledivy/mimic)**

你有没有过这种想法：想用 Python 自动操作某个 App，但它没有公开 API？

以前你的选择是：
- 逆向工程抓包，手动分析每个 endpoint
- 用 Selenium 或 Appium 做 UI 自动化，又慢又脆
- 算了

**mimic 的解法完全不一样。** 它用 mitmproxy 拦截你的手机 App 流量，然后让 Claude 自动分析抓到的请求，**直接生成一个 Python SDK**。

### 怎么用

```bash
# 三步走
mimic record           # 启动代理，手机设好代理走 Mac
mimic hosts            # 列出抓到的主机
mimic learn prod-api.xxx.com   # AI 分析 endpoint
mimic gen  prod-api.xxx.com    # 生成 SDK
```

然后你就可以：

```python
from hinge_client import Hinge   # ← 这是 AI 生成的

acc = Hinge()                    # 复用你抓到的 session
recs = acc.get_recommendations()
acc.like("user123", comment="hi")
```

不用写一行 API 封装代码。mimic 把认证信息（bearer token、device id、session id）一次性抓下来，帮你自动注入到每个请求里。

### 两个重要的限制

项目 README 诚实交代了两个坑：

1. **证书锁定**（银行 App、Instagram）— App 拒绝 mitmproxy 的证书，拦截不到流量。mimic 提供了 Frida 绕过方案，但不是一键的。
2. **DPoP 令牌** — 每次请求都用设备私钥签名一个新鲜证明，抓到的请求根本无法重放。这完全破了 mimic 的核心模型，**目前没有好办法**。

### 为什么它 24 小时拿了 799★

**因为思路太对了。** AI 的进步让「协议分析」这件事从手工苦力变成了自动化流水线——认证参数提取、endpoint 归纳、代码生成，每一步 Claude 都比人快得多。而且生成的是可编辑的 Python 代码，不是黑盒。

当然项目用的是 Hinge 做展示例子（约会软件 API），让人联想到各种用法。README 也写了伦理条款：**只用于你自己的账号和数据**，不要用它访问别人的数据。项目的生成 SDK 也会在你的机器上本地处理所有流量数据，不会外传。

**另外一提**：mimic 还支持直接从 Chrome DevTools 的「Copy as cURL」粘贴请求来构建 session，不需要走代理。这对有 Web 版的 App 来说更方便——打开浏览器开发者工具，复制请求，`Session.from_curl(text)` 就行。

> 一句话：如果你写过任何第三方 API 的封装代码，你会懂为什么这个项目一天 799★。不是因为它能做什么，而是因为它把「写 SDK 这件事本身」变成了一个 CLI 命令。

---

## 🧠 J-Wash — 给 LLM 洗脑的工具

**★ 76 | 1 天 | Python | [Extraltodeus/J-Wash](https://github.com/Extraltodeus/J-Wash)**

如果让你用一句话概括这个项目，那就是：**不用微调，直接编辑大模型内部的知识和行为，然后把改好的模型导出为标准权重文件。**

### 它怎么做到的

J-Wash 建立在 Anthropic 的 **Jacobian Lens** 技术上。Jacobian Lens 是一种「读心术」——它能告诉你 LLM 每一层在处理什么概念、读什么 token。

具体来说，当你和模型聊天时，J-Wash 实时展示：

- **频率视图**：模型各层在「读」哪些 token，按出现频率排列
- **热力图**：每个位置、每层最活跃的 token 是什么
- **token 编辑**：你可以把「model」这个 token 的方向，映射到「fish」的方向

### 最酷的 demo

项目给出了一个例子：把模型的自我认知从 *"I am a large language model"* 改成 *"I am a large language fish"*。

不是通过 prompt 伪装，不是在输出层后处理——而是**直接改了模型内部的权重方向**，改完后导出一个可以在任何 transformers 框架里加载的 checkpoint。

### 三种导出格式

- **完整 checkpoint** — 加载即用，跟原模型一样
- **修改过的 layers** — 只有改动过的层
- **LoRA** — 编辑本身是低秩的（因为改的只是方向），所以 LoRA 是精确差而不是近似

### 什么时候能用上

目前需要 NVIDIA GPU + CUDA，前端是 React + FastAPI 的本地 studio。模型从 HuggingFace 加载，lens 可以从 Neuronpedia 下载或自己训练。

这不是一个面向普通用户的工具。但如果你对 LLM 可解释性感兴趣，或者好奇「模型内部到底长什么样」，J-Wash 是目前最漂亮的交互式探索入口。而且它是开源的，没有把功能锁在 SaaS 后面。

> 一句话：Jacobian Lens 让「读 LLM 的思想」变成了可能，J-Wash 让「改 LLM 的思想」变成了一个 GUI 操作。

---

## 🎸 YouTube Guitar Tab Parser — 把吉他教学视频变成 PDF 谱子

**★ 123 | 1 天 | TypeScript | [marcelpanse/youtube-guitar-tab-parser](https://github.com/marcelpanse/youtube-guitar-tab-parser)**

这个项目的动机我太懂了：你在 YouTube 上找到一个超好的吉他教学视频，老师把六线谱打在屏幕上，但你总不能一直盯着视频练吧？

**这个 CLI 工具做的事情：把视频里的吉他谱自动提取出来，做成一份干净的 PDF。**

### 技术管线

```
YouTube 链接
  ↓ yt-dlp 下载视频
  ↓ ffmpeg 每隔 N 秒抽一帧
  ↓ Claude Vision 定位谱子区域（粗定位）
  ↓ 图像处理精确裁切（暗色内容 + 浅色背景 → 谱纸边缘检测）
  ↓ 感知哈希去重，去掉重复帧
  ↓ Claude 读每个片段的谱号（bar number），保留唯一的一帧
  ↓ pdf-lib 拼接成 A4 PDF
  → out/<视频标题>.pdf
```

### 有意思的设计细节

两个阶段的定位方案很聪明：Claude Vision 擅长识别「谱子在大概什么位置」，但不擅长精确的像素坐标。所以先用 AI 粗定框，再用传统图像处理做边缘检测精确裁切——两者互补。

去重也不是简单的「看起来差不多就删掉」，而是**按谱号去重**——同一行谱子在视频里出现了很多帧（播放头在扫），但谱号不变，所以只保留一张。这样 PDF 里不会有一堆几乎一样的页面。

### 实际效果

项目配了一个例子：[Game of Thrones 吉他教学](https://youtu.be/WgU5tDGC-Vc) → 输出的 PDF 可以直接下载看。如果你平时练吉他靠 YouTube 视频，这个工具能省你不少时间。

> 一句话：把「AI 视觉 + 传统图像处理」用得很巧妙，不是为了用 AI 而用 AI，而是在 AI 擅长的地方用它、在不擅长的部分用经典算法顶上。

---

## 📊 快讯速览

这波还有几个值得一提的：

| 项目 | ★ | 一句话 |
|------|---|--------|
| **[Tradingview-MCP](https://github.com/pueschel88/Tradingview-MCP)** | 74 | 用 MCP 协议从 Claude Code 直接控制 Tradingview Desktop——让你的 Agent 帮你看 K 线 |
| **[pixel-art-fixer](https://github.com/Retro-Diffusion/pixel-art-fixer)** | 73 | 图片转像素风 |
| **[sigwire](https://github.com/yeet-src/sigwire)** | 91 | `tail -f` for Linux 信号——谁给哪个进程发了什么信号，一目了然（不是 AI 项目但酷） |

---

## 💭 今日三篇总结

今天一口气写了三篇 AI 日报，主题恰好覆盖了 AI 生态的三种气质：

| 篇 | 气质 | 代表项目 |
|:--:|------|----------|
| ① 反 AI 味 | **反思型**— AI 做的东西不好看，我们去改 | kill-ai-slop / 說人話 / 拉片笔记 |
| ② 新玩法 | **探索型**— AI 还能做这些事？ | vox-director / plandeck / Local-Recall |
| ③ 硬核向 | **突破型**— AI 能力的边界又被推了一步 | mimic / J-Wash / Guitar Tab Parser |

AI 圈一天冒出这么多不同方向的项目，说明一件事：**远没到终点。** 有人在反思 AI 的品味，有人在开拓 AI 的用法，有人在挑战 AI 的能力极限——三种姿势，谁也别笑话谁。

今天的 AI 日报三连发到此结束。明天见～☕
