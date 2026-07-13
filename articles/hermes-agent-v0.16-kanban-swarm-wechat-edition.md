# Hermes Agent v0.16 Kanban Swarm 深度解析：当 AI Agent 有了自己的协作流水线

> 本文由 Hermes Agent Kanban Swarm 流水线自动生成

---

## 引言

2026 年 6 月 5 日，Nous Research 发布了 Hermes Agent v0.16.0。真正值得 AI 开发者关注的，是一个在 v0.15.0 诞生、在 v0.16.0 进一步打磨的底层能力：**Kanban Swarm——多智能体协作工作流引擎**。

如果你还在手动编排多个 AI Agent，Kanban Swarm 可能会彻底改变你组织 AI 工作流的方式。

**一句话概括**：Kanban Swarm 是一个基于 SQLite 的持久化任务看板，让多个 AI Agent 像工厂流水线一样协作——任务状态持久化、断点续传、人工介入、审计追溯，所有 Agent 之间通过看板行通信。

---

## 一、从 delegate_task 到 Kanban

Hermes 的 `delegate_task` 是一个强大的 RPC 式子代理机制，但有几个本质局限：

- **形态**：RPC 调用 vs 持久化消息队列
- **子进程**：匿名子 Agent vs 具名 Profile
- **断点续传**：不支持 vs 阻塞/解阻塞
- **人工介入**：不支持 vs 随时评论
- **审计**：上下文压缩丢失 vs SQLite 永久保留

**一句话**：delegate_task 是函数调用，Kanban 是工作队列。

### 核心架构

```
┌───────────┐   ┌───────────┐   ┌───────────┐
│researcher  │   │  writer   │   │  reviewer │
│ (Profile)  │   │ (Profile) │   │ (Profile) │
└─────┬─────┘   └─────┬─────┘   └─────┬─────┘
      │               │               │
      └───────┬───────┴───────┬───────┘
              │               │
        ┌─────▼─────┐   ┌────▼──────┐
        │kanban.db  │   │Dispatcher │
        │  (SQLite) │   │ (每60s)   │
        └───────────┘   └───────────┘
```

关键决策：SQLite 持久化、Worker 是完整 OS 进程、Dispatcher 默认运行在 Gateway 内部。

---

## 二、Kanban Swarm v1：一键生成 Swarm 拓扑

执行一条命令就能生成完整的协作图：

```bash
hermes kanban swarm "撰写一篇技术文章"
```

这会自动分解为：Root Task → Parallel Workers → Gated Verifier → Gated Synthesizer

四个核心组件：
1. **Root Task** — 入口点
2. **Parallel Workers** — 并行子任务
3. **Gated Verifier** — 质量审核
4. **Gated Synthesizer** — 整合发布

### 任务状态流转

`triage → todo → ready → running → blocked → done → archived`

Worker 通过 `kanban_heartbeat` 定期报告存活。如果进程崩溃，Dispatcher 自动回收重新分配。

---

## 三、v0.16 增强

- **goal_mode 循环** — 持续执行目标，直到手动终结
- **文件附件 + 视觉** — 任务可带图片，Worker 自动加载到视觉模型
- **并发控制** — 每个 Profile 设 max_concurrent
- **远程终结** — `POST /runs/{run_id}/terminate`

---

## 四、实战：博客流水线

这篇文章本身就是用 Kanban Swarm 生产的：

1. **🔀 orchestrator** — 接收主题，自动分解任务链
2. **🔬 researcher** — deepseek/deepseek-chat 低成本搜索
3. **✍️ writer** — deepseek-v4-flash 写 2000+ 字
4. **✅ reviewer** — 四维审核（技术/逻辑/时效/可读）
5. **🚀 publisher** — git push GitHub

核心设计：
- **Profile 即角色** — 不同模型成本最优化
- **依赖链即 Pipeline** — `--parent` 自动顺序执行
- **工作空间隔离** — scratch/dir/worktree 三种模式
- **人工在环** — `kanban_block` 等待人工确认

---

## 五、对比其他方案

| 方案 | 持久化 | 人工介入 | 适用场景 |
|------|--------|---------|---------|
| Hermes Kanban | ✅ SQLite | ✅ | 生产级工作流 |
| OpenAI Swarm | ❌ | ❌ | 原型实验 |
| AutoGen | ❌ | ✅ | 对话式协作 |
| CrewAI | ❌ | ❌ | 简单顺序任务 |

Kanban 的核心差异：它不是"框架"而是"基础设施"——任何 Agent 只要会读写 SQLite 就能参与。

---

## 六、最佳实践

✅ **推荐**
- 为每种角色创建独立 Profile
- 善用 model_override 优化 Token
- 设置合理的 claim_ttl
- 长任务用 dir: 工作空间

❌ **避免**
- 实时交互用 Kanban（用 delegate_task）
- 所有任务同一个 Profile
- 忽略 Heartbeat

---

## 结语

Kanban Swarm 的设计哲学是"薄层编排"——用最少的约束实现最大的灵活性。它不是告诉你"应该怎么用 AI Agent"，而是给你一个工具箱，让你自己决定"我的 AI Agent 应该怎么协作"。

**这就是 AI Agent 基础设施该有的样子：它不在你面前晃悠，但你的活儿干完了。**

---

### 📋 微信公众号发布指南

**标题建议**: Hermes Agent v0.16 Kanban Swarm 深度解析

**封面图建议**: 
- 方案1：用 Excalidraw 生成一张 Kanban Swarm 架构手绘风格图
- 方案2：截取 GitHub 上 Kanban 命令的终端运行截图
- 方案3：纯文字封面图（深色背景 + 白色大标题）

**排版建议**:
- 正文使用默认字号（16px）
- 代码块正确使用 Markdown 代码格式
- 表格用微信编辑器中的"表格"组件
- 重点加粗部分已标注

**发布步骤**:
1. 复制本 Markdown 内容
2. 粘贴到微信公众平台编辑器
3. 添加封面图
4. 设置标签：AI Agent, Hermes, 多智能体
5. 预览确认排版
6. 发布

> 📍 文章已推送到 GitHub: https://github.com/jxlyc050616/hermes-agent-blog
