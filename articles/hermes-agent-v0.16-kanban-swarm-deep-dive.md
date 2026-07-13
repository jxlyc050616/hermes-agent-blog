---
title: "Hermes Agent v0.16 Kanban Swarm 深度解析：当 AI Agent 有了自己的协作流水线"
date: 2026-07-13
author: "小糊涂虫"
tags: [Hermes Agent, Kanban, Swarm, Multi-Agent, v0.16]
description: "深入解析 Hermes Agent v0.16 的 Kanban Swarm 多智能体协作系统——从架构设计到实战工作流，看 AI Agent 如何编排 AI Agent"
---

# Hermes Agent v0.16 Kanban Swarm 深度解析：当 AI Agent 有了自己的协作流水线

## 引言

2026年6月5日，Nous Research 发布了 Hermes Agent v0.16.0（代号"The Surface Release"）。这个版本的核心惊喜并不在标题中的桌面应用和仪表盘——那些只是改变了你与 Agent 交互的"表面"。真正值得 AI 开发者关注的，是一个在 v0.15.0 诞生、在 v0.16.0 进一步打磨的底层能力：**Kanban Swarm——多智能体协作工作流引擎**。

如果你还在手动编排多个 AI Agent，或者在 `delegate_task` 的树形调用链里头疼，那么 Kanban Swarm 可能会彻底改变你组织 AI 工作流的方式。

> **一句话概括**：Kanban Swarm 是一个基于 SQLite 的持久化任务看板，让多个 AI Agent（不同 Profile）像工厂流水线一样协作——任务状态持久化、断点续传、人工介入、审计追溯，所有 Agent 之间通过看板行通信，不再依赖脆弱的进程内调用链。

---

## 一、架构全景：从 `delegate_task` 到 Kanban

在理解 Kanban Swarm 之前，先要理解它解决的是什么问题。

### 1.1 `delegate_task` 的局限

Hermes 的 `delegate_task` 是一个强大的 RPC 式子代理机制：主 Agent fork 出一个子 Agent 执行任务，等它完成后拿到结果，继续往下走。但它的设计本质决定了几个难以逾越的局限：

| 维度 | `delegate_task` | Kanban Swarm |
|------|----------------|--------------|
| **形态** | RPC 调用（fork → join） | 持久化消息队列 + 状态机 |
| **父进程** | 阻塞等待子进程返回 | fire-and-forget，创建后立即返回 |
| **子进程标识** | 匿名子 Agent | 具名 Profile，带持久化记忆 |
| **断点续传** | 不支持——失败即失败 | 阻塞 → 解阻塞 → 重试；崩溃 → 回收 |
| **人工介入** | 不支持 | 随时评论和解阻塞 |
| **审计追溯** | 上下文压缩后丢失 | SQLite 中永久保留 |
| **协调模式** | 层级式（调用者 → 被调用者） | 对等——任何 Profile 可读写任何任务 |

**一句话区分**：`delegate_task` 是**函数调用**，Kanban 是**工作队列**——每一次交接都是一行记录，任何 Agent（或人）都能看到并编辑。

### 1.2 Kanban Swarm 的核心架构

```
┌─────────────────────────────────────────────────────────┐
│                    Hermes Gateway                        │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Dispatcher (调度器)                   │   │
│  │  - 每 60 秒扫描一次                               │   │
│  │  - 回收僵死任务、提升 ready 队列                    │   │
│  │  - 自动分配任务到指定 Profile                       │   │
│  └──────────────────────────────────────────────────┘   │
│                         │                                │
└─────────────────────────┼────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              │    kanban.db (SQLite)  │
              │   ┌─────────────────┐  │
              │   │ tasks 表        │  │
              │   │ task_links 表   │  │
              │   │ comments 表     │  │
              │   │ boards 表       │  │
              │   └─────────────────┘  │
              └───────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   researcher         writer            reviewer
   (Profile)          (Profile)          (Profile)
        │                 │                 │
    kanban_show      kanban_show       kanban_show
    kanban_complete   kanban_complete   kanban_complete
    kanban_block      kanban_comment    kanban_heartbeat
```

**关键设计决策**：

1. **SQLite 作持久化层**——零依赖、无需额外部署、每个任务记录永久保留
2. **State Machine 状态机**——任务在 `triage → todo → ready → running → blocked → done → archived` 之间流转
3. **Worker 是完整 OS 进程**——每个工作 Agent 是一个独立的 Hermes 进程实例，拥有自己的 Profile、记忆、工具集
4. **Dispatcher 常驻网关**——默认运行在 Hermes Gateway 内部，每 60 秒一个 tick

---

## 二、Kanban Swarm v1：一键生成 Swarm 拓扑

在 v0.15.0 中，Hermes 引入了一个极具想象力的命令：`hermes kanban swarm`。

### 2.1 Swarm 拓扑结构

执行一条命令，就能生成一个完整的 Swarm v1 协作图：

```bash
hermes kanban swarm "撰写一篇关于 Hermes Agent 的深度技术文章"
```

这个命令会自动分解出：

```
                    ┌──────────────┐
                    │  Root Task   │
                    │  撰写技术文章 │
                    └──────┬───────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
     ┌──────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
     │  Worker 1   │ │  Worker 2  │ │  Worker 3  │
     │  调研资料    │ │  撰写内容  │ │  代码验证   │
     └──────┬──────┘ └─────┬──────┘ └─────┬──────┘
            │              │              │
            └──────────────┼──────────────┘
                           │
                    ┌──────▼──────┐
                    │  Verifier   │
                    │  四维审核   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Synthesizer │
                    │  整合发布   │
                    └─────────────┘
```

这个拓扑包含四个核心组件：

1. **Root Task（根任务）**——Swarm 的入口点，包含完整任务描述和目标
2. **Parallel Workers（并行工作者）**——可并行执行的子任务，各自分配给不同的 Profile
3. **Gated Verifier（门控验证器）**——等待所有 Worker 完成后，执行质量审核
4. **Gated Synthesizer（门控合成器）**——通过验证后，生成最终交付物

### 2.2 协作流程详解

每个 Worker 的工作流：

```
任务创建 (triage)
  ↓  Dispatcher 扫描并分配
任务就绪 → 分配 (ready → running)
  ↓  Worker 进程启动
Worker 读取任务详情 + 历史评论
  ↓
执行工作 (调用工具、读写文件)
  ↓  kanban_heartbeat 每 15 秒报告存活
完成或阻塞
  ↓
kanban_complete → done
  OR
kanban_block → blocked (等待人工介入)
```

**关键的 Heartbeat 机制**：Worker 在运行期间会定期发送心跳（`kanban_heartbeat`）。如果 Dispatcher 发现某个任务的 PID 已消失但 TTL 未过期，它会自动回收这个任务并重新分配。这意味着即使 Worker 进程崩溃，任务也不会永远卡在 `running` 状态。

### 2.3 任务状态流转图

```
                     ┌──────────┐
                     │  triage   │
                     └────┬─────┘
                          │ 人工或自动分解
                     ┌────▼─────┐
                     │   todo   │
                     └────┬─────┘
                          │ 所有前置依赖完成
                     ┌────▼─────┐
                     │  ready   │
                     └────┬─────┘
                          │ Dispatcher 分配
              ┌───────────┼───────────┐
              │           │           │
         ┌────▼────┐ ┌───▼────┐  ┌───▼──────┐
         │ running │ │blocked │  │ archived  │
         └────┬────┘ └───┬────┘  └──────────┘
              │           │
              │      ┌────▼────┐
              │      │  done   │  ← 解阻塞后 → ready
              │      └────┬────┘
              │           │
              └───────────┘
```

---

## 三、v0.16.0 对 Kanban 的增强

v0.16.0 不是 Kanban 的初始版本，但它带来的改进对生产级使用至关重要：

### 3.1 goal_mode 循环执行

```yaml
# 任务配置
goal_mode: true
goal_prompt: "持续监控日志目录，发现 ERROR 立即报告"
```

当 `goal_mode` 开启时，Worker 会进入 `/goal` 循环模式——不是一次执行就结束，而是保持活跃、持续执行目标，直到手动终结或目标达成。

**适用场景**：

- 日志监控与告警
- 定时数据采集与汇总
- 持续代码审查

### 3.2 文件附件与视觉能力

- 任务可以附带文件附件（代码、文档、图片）
- 如果任务 body 中引用了图片 URL，Worker 启动时会自动加载到视觉模型中
- 这意味着：你可以创建一个 "帮我审查这张 UI 设计图" 的任务，Worker 拿到后真的会用多模态模型看图分析

### 3.3 Per-Profile 并发控制

```yaml
# 在 Profile 配置中
kanban:
  concurrency: 2  # 该 Profile 最多同时运行 2 个任务
```

在 v0.16.0 之前，所有任务争抢同一 Profile 的进程。现在可以为每个 Profile 设置并发上限，防止一个 Profile 被塞满任务导致所有其他任务排队。同时 `default_assignee` 回退机制确保无人认领的任务不会死在那里。

### 3.4 远程终结端点

新增 `POST /runs/{run_id}/terminate` 端点，允许通过 API 直接中止正在运行的任务——自动化流水线可以自助管理任务生命周期，不再需要手动介入。

---

## 四、实战案例：用 Kanban Swarm 搭建博客流水线

这是我实际用 Kanban Swarm 搭建的一个博客生产流水线，也是这篇文章本身的诞生方式：

### 4.1 流水线架构

```
📱 微信收到主题
    │
    ▼
🔀 orchestrator（任务拆解）
  - 接收用户主题
  - 自动分解为：调研 + 撰写 + 审核 + 发布
  - 创建依赖链：调研→撰写→审核→发布
    │
    ▼
🔬 researcher（小糊研究员）
  - 模型：deepseek/deepseek-chat（低成本）
  - 工具：搜索 + 终端 + 文件
  - 输出：结构化研究报告
    │
    ▼
✍️ writer（小糊撰稿人）
  - 模型：deepseek-v4-flash（高质量）
  - 推理：high
  - 约束：字数 ≥ 2000
  - 输出：完整 Markdown 文章
    │
    ▼
✅ reviewer（四维审核员）
  - 模型：deepseek-v4-flash
  - 检查：技术准确性 / 逻辑完整性 / 信息时效性 / 可读性
  - 输出：checklist 格式审核报告
    │
    ▼
🚀 publisher（发布员）
  - git commit → push → GitHub
  - 微信公众号排版与发布
```

### 4.2 核心设计要点

**1. Profile 即角色**
每个 Profile 是一个有明确身份和能力的 Agent。`researcher` 用低成本模型（搜资料不需要大模型），`writer` 用高质量模型（创作需要深度推理）。这在 Kanban Swarm 中天然支持——每个任务可以指定 `model_override`，不同子任务用不同模型和推理级别，成本最优化：

```bash
hermes kanban create "调研主题" --assignee researcher --model deepseek/deepseek-chat
hermes kanban create "撰写文章" --assignee writer --model deepseek-v4-flash --reasoning high
```

**2. 依赖链即 Pipeline**
通过 `--link` 或 `--parent` 参数创建父子依赖，Dispatcher 会自动按顺序推进：

```bash
# 创建依赖链
hermes kanban create "撰写文章" --parent "$RESEARCH_TASK_ID"
hermes kanban create "审核文章" --parent "$WRITE_TASK_ID"
hermes kanban create "发布文章" --parent "$REVIEW_TASK_ID"
```

**3. 工作空间隔离**
每个任务支持三种工作空间类型：

| 类型 | 说明 | 生命周期 |
|------|------|---------|
| `scratch`（默认） | 临时目录 | 任务完成后删除，artifacts 保留 |
| `dir:/path` | 已有目录 | 永久保留 |
| `worktree:/project` | Git worktree | 永久保留，适合编码任务 |

审核任务完成后，`dir:` 目录中的最终 Markdown 直接由 Publisher 推送到 GitHub。

**4. 人工在环（Human-in-the-Loop）**
Kanban 最强大的特性之一：任何人可以在任何时间点通过 `kanban_comment` 或 CLI 的 `hermes kanban comment` 在任务上留言。如果 Worker 发现需要人工决策，它可以直接 `kanban_block` 并附带问题，等待人工回复后再 `kanban_unblock` 继续执行。

---

## 五、Kanban Swarm vs 其他多 Agent 方案

理解 Kanban Swarm 的最好方式，是与当前主流的几种多 Agent 协作方案对比：

| 方案 | 协作模式 | 持久化 | 人工介入 | 适用场景 |
|------|---------|--------|---------|---------|
| **Hermes Kanban** | 对等看板 | ✅ SQLite | ✅ 原生支持 | 生产级工作流、跨日任务 |
| **OpenAI Swarm** | 函数调用链 | ❌ 无 | ❌ 无 | 实验性原型 |
| **AutoGen** | 对话式 | ❌ 无 | ✅ 手动 | 研究、对话式协作 |
| **CrewAI** | 层级流程 | ❌ 无 | ❌ 无 | 简单顺序任务 |
| **LangGraph** | 图状态机 | ❌ 内存中 | ❌ 无 | 需要精细控制的状态流 |

Kanban 的核心差异在于：**它不是一个"框架"而是一个"基础设施"**。它不定义 Agent 之间的通信协议（那是 LLM 自己搞定的），它只提供一个可靠的持久化工作队列——任何语言、任何框架、任何 Agent 只要会读写 SQLite 就能参与。

---

## 六、最佳实践与陷阱

### ✅ 推荐做法

1. **为每种角色创建独立 Profile**——不同 Profile 拥有不同的模型、记忆和工具集，这是 Kanban Swarm 的设计初衷
2. **善用 `model_override`**——搜索类任务用便宜的模型，创作和决策类任务用好模型，优化 Token 消耗
3. **设置合理的 TTL**——根据任务复杂度调整 `claim_ttl`，太短会导致 Worker 被过早回收，太长会导致崩溃任务长期不释放
4. **使用 `dir:` 工作空间**——当任务处理的数据需要长期保留时，用 `dir:/path` 替代默认的 `scratch`，避免数据丢失
5. **拥抱人工在环**——不要试图让流水线完全自动化。复杂决策节点设置 `kanban_block` 等待人工确认，是保证质量的关键

### ❌ 常见误区

1. **用 Kanban 做实时交互**——Dispatcer 默认 60 秒扫描间隔，不适合需要秒级响应的场景。实时交互请用 `delegate_task`
2. **所有任务都用同一个 Profile**——身份模糊的 Agent 做不好任何事。给不同角色不同的 Profile
3. **忽略 Heartbeat**——长时间运行的任务应该调用 `kanban_heartbeat`，否则被 Dispatcher 误回收会前功尽弃
4. **单个 Board 塞太多无关任务**——不同项目应该用不同的 Board，而不是一个 Board 里塞满杂项。`hermes kanban board create project-name` 即可

---

## 七、未来展望

从 v0.15.0 到 v0.16.0，Kanban 系统经历了 104+ PR 的重塑。从我的观察来看，Kanban Swarm 正在从"一个实验性功能"进化为"Hermes 多 Agent 编排的默认范式"。

几个值得关注的演进方向：

- **跨主机 Board**——目前 Kanban 是单机设计，未来可能支持分布式 Board，让不同机器上的 Agent 协作
- **动态拓扑重配置**——v1 的 Swarm 拓扑是静态生成的，未来的 Dispatcher 可能能在运行时根据任务进度动态调整拓扑
- **RAG 增强的任务分解**——Orchestrator 可以结合知识库，将用户需求更精确地分解为可执行的子任务

---

## 结语

Kanban Swarm 是一个简单但不简陋的设计。它没有引入复杂的新协议，没有要求你学习新的编排语言，没有强迫你改变 Agent 的写作方式——它只是在所有 Agent 之间放了一个 SQLite 数据库，然后说："你们看完留言板上写下你的结果，下一个自然有人接上。"

这种"薄层编排"的设计哲学——用最少的约束实现最大的灵活性——正是 Hermes Agent 一直以来的风格。它不是告诉你"应该怎么用 AI Agent"，而是给你一个工具箱，让你自己决定"我的 AI Agent 应该怎么协作"。

而对于像我这样需要同时管理多个 AI Agent 的开发者来说，Kanban Swarm 最珍贵的不是那个 Swarm 拓扑生成器，也不是那个 Dispatcher 自动回收机制——而是它让我可以晚上睡觉前创建一个任务，第二天醒来时看到它已经经过了调研、撰写、审核、发布四个节点，整齐地排在我的 GitHub 上。

**这就是 AI Agent 基础设施该有的样子：它不在你面前晃悠，但你的活儿干完了。**

---

*本文由 Hermes Agent Kanban Swarm 流水线自动生成：researcher 调研 → writer 撰写 → reviewer 审核 → publisher 发布。*

*源码仓库：https://github.com/jxlyc050616/hermes-agent-blog*
