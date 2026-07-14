---
title: "LLM Agent 工具调用机制深度解析：从 Function Calling 到 MCP 协议的架构演进"
date: 2026-07-14
author: "小糊涂虫"
tags:
  - LLM
  - Agent
  - Function Calling
  - MCP
  - 工具调用
  - AI架构
  - 多智能体
description: "全面解析 LLM Agent 工具调用机制，从 OpenAI Function Calling 到 Anthropic MCP 协议的架构演进与工程实践"
---

# LLM Agent 工具调用机制深度解析：从 Function Calling 到 MCP 协议的架构演进

> 让大语言模型不再只是"纸上谈兵"——工具调用是 Agent 通往真实世界的桥梁。

## 摘要

2023 年 OpenAI 推出 Function Calling 功能，标志着大语言模型（LLM）从"对话生成"迈入"行动执行"的关键转折。此后一年半，Anthropic 的 Tool Use、Google 的 Function Declaration、以及最新的 Model Context Protocol（MCP）协议相继问世，工具调用的架构从**封闭的 API 调用**演进为**开放的标准协议**。本文将深入解析这些机制的核心原理、架构设计、代码实现与工程化最佳实践，并通过完整的对比分析，帮助读者构建对 LLM 工具调用体系的系统性认知。

---

## 一、为什么需要工具调用？

大语言模型本质上是一个**概率生成器**——基于海量训练数据学习到的模式来预测下一个 token。它有几大天然局限：

1. **知识截止**：模型的知识停留在训练数据截止日期，无法获取最新信息
2. **计算能力弱**：无法精确执行数学运算，更无法运行代码
3. **无状态访问**：无法访问数据库、文件系统、API 等外部资源
4. **无法执行操作**：不能发送邮件、创建工单、修改配置等

**工具调用（Tool Calling/Function Calling）** 正是为了解决这些局限而设计的架构模式：LLM 生成结构化的"工具调用请求"，由宿主环境（Agent 框架/应用）执行实际调用，再将结果反馈给 LLM 进行下一步推理。

用一句大白话概括：**LLM 负责 "思考"，工具负责 "执行"。**

---

## 二、架构演进全景

### 2.1 第一代：Prompt 工程时代（2022-2023）

最早的方案是在系统提示词中描述可用的工具，让模型自然语言输出调用指令：

```
你是一个智能助手。当你需要查询天气时，请输出：
[call_tool: get_weather(location="北京")]
```

**痛点**：不可靠。模型输出格式不固定，解析困难，几乎没有错误处理能力。

### 2.2 第二代：OpenAI Function Calling（2023.06）

2023 年 6 月，OpenAI 在 `gpt-3.5-turbo-0613` 和 `gpt-4-0613` 中正式推出 Function Calling，成为**第一个原生支持工具调用的商业 LLM API**。

核心原理：在 API 请求中通过 `functions` 或 `tools` 参数声明可调用的工具，模型返回结构化 JSON，而非自然语言。

```json
// API 请求中的工具声明
{
  "model": "gpt-4",
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "获取指定城市的当前天气",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "城市名，如 北京、上海"
            },
            "unit": {
              "type": "string",
              "enum": ["celsius", "fahrenheit"]
            }
          },
          "required": ["location"]
        }
      }
    }
  ],
  "messages": [
    {"role": "user", "content": "北京今天天气怎么样？"}
  ]
}
```

模型返回的响应中会包含 `tool_calls` 字段：

```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": null,
      "tool_calls": [{
        "id": "call_xxx",
        "type": "function",
        "function": {
          "name": "get_weather",
          "arguments": "{\"location\":\"北京\"}"
        }
      }]
    }
  }]
}
```

**关键设计决策**：OpenAI 在模型内部通过**注意力机制**将 JSON Schema 与对话上下文进行联合编码，使模型能够：
- 理解参数的语义约束（枚举、格式、必填）
- 在需要时选择调用（而非强制每次都调用）
- 支持并行调用（Parallel Function Calling，2023.11 发布）

这就是经典的 **ReAct（Reasoning + Acting）循环**：Think → Call → Observe → Repeat。

```python
# 简化的 Function Calling 循环
def agent_loop(user_query: str):
    messages = [{"role": "user", "content": user_query}]
    
    while True:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        messages.append(message)
        
        if not message.tool_calls:
            # 模型已给出最终回答
            return message.content
        
        # 执行每个工具调用
        for tool_call in message.tool_calls:
            result = execute_tool(tool_call.function.name, 
                                  json.loads(tool_call.function.arguments))
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })
```

### 2.3 第三代：多模型时代的百花齐放

2024 年，各大模型厂商纷纷跟进：

| 厂商 | 功能名 | 推出时间 | 特色 |
|------|--------|----------|------|
| OpenAI | Function Calling / Tool Calling | 2023.06 | 首创，支持并行调用 |
| Anthropic | Tool Use | 2024.03 | 支持多轮工具调用链 |
| Google Gemini | Function Declaration | 2024.04 | 原生支持 Python 代码执行 |
| Mistral | Function Calling | 2024.05 | 开源模型，可自部署 |
| Meta Llama 3 | Tool Calling | 2024.07 | 社区生态丰富 |

以 Anthropic 的 Tool Use 为例，其在架构上的独特设计是**工具结果自动注入**——模型内部自动将工具结果拼接回推理上下文，开发者无需手动管理 `role: tool` 消息：

```python
# Anthropic Tool Use 示例
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[
        {
            "name": "search_database",
            "description": "搜索数据库中的用户信息",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["query"]
            }
        }
    ],
    messages=[{"role": "user", "content": "查找最近注册的用户"}]
)

# Claude 会返回 tool_use 类型的 content block
for content in response.content:
    if content.type == "tool_use":
        result = execute_tool(content.name, content.input)
        # 将结果附加回对话
        messages.append({
            "role": "user", 
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": content.id,
                    "content": str(result)
                }
            ]
        })
```

> **架构洞察**：Function Calling 的技术本质是**约束解码**——模型在生成过程中，一旦检测到需要调用工具，其 token 生成空间会被限制为合法的 JSON 语法。这是一项需要专门训练的能力，并非简单的 prompt 工程。

---

## 三、MCP 协议：标准化工具调用

### 3.1 背景：碎片化之痛

随着工具调用的普及，行业面临一个尴尬局面：每接入一个工具，开发者就需要：
1. 编写 JSON Schema 声明
2. 实现 API 调用逻辑
3. 处理认证、重试、错误
4. 适配不同 LLM 厂商的格式差异

**这种"点对点集成"在工具数量增长时迅速失控。**

### 3.2 MCP 是什么？

2024 年 11 月，Anthropic 发布了 **Model Context Protocol（MCP）**，旨在成为 LLM 工具调用的"HTTP 协议"——一个开放、统一的标准化协议。

MCP 的核心架构采用**客户端-服务器**模型：

```
┌─────────────────────────────────────────┐
│             AI 应用 (MCP Client)         │
│  ┌─────────────────────────────────┐    │
│  │    Hermes / Claude Desktop      │    │
│  │    / Cursor / 自定义 Agent      │    │
│  └──────────┬──────────────────────┘    │
│             │ MCP Protocol              │
│  ┌──────────▼──────────────────────┐    │
│  │    Transport Layer              │    │
│  │  (stdio / SSE / WebSocket)      │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    ▼                   ▼
┌──────────┐     ┌──────────┐
│ MCP Server │     │ MCP Server │
│ (文件系统)  │     │ (数据库)   │
│ 工具:      │     │ 工具:      │
│  - read    │     │  - query   │
│  - write   │     │  - insert  │
│  - search  │     │  - update  │
└──────────┘     └──────────┘
```

### 3.3 MCP 的核心概念

**Resources（资源）**：暴露给 LLM 的数据来源，类似 RESTful API 的资源概念。通过 URI 定位，支持动态更新的订阅机制。

**Tools（工具）**：LLM 可以调用的可执行动作。每个工具有名称、描述和 JSON Schema 参数定义。

**Prompts（提示模板）**：预定义的对话模板，LLM 可以"使用"特定工具时自动注入上下文。

**Transport（传输层）**：MCP 支持多种传输方式：
- **stdio**：通过子进程的标准输入/输出通信，适合本地工具
- **SSE（Server-Sent Events）**：通过 HTTP 长连接通信，适合远程服务
- **WebSocket**：双向通信，适合实时交互（预览特性）

### 3.4 MCP 协议的核心流程

```json
// Client → Server: 初始化
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": { "tools": {} },
    "clientInfo": { "name": "hermes-agent", "version": "1.0.0" }
  }
}

// Server → Client: 返回可用工具列表
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}

// 响应
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "read_file",
        "description": "读取文件内容",
        "inputSchema": {
          "type": "object",
          "properties": {
            "path": { "type": "string" }
          },
          "required": ["path"]
        }
      }
    ]
  }
}

// Client → Server: 调用工具
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": { "path": "/tmp/test.txt" }
  }
}
```

### 3.5 实现一个简单的 MCP Server

```python
# mcp_server.py — 一个最小化的 MCP Server
import json
import sys

class MCPServer:
    def __init__(self):
        self.tools = {
            "calculator": {
                "name": "calculator",
                "description": "执行数学运算",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "expr": {"type": "string", "description": "数学表达式"}
                    },
                    "required": ["expr"]
                }
            }
        }
    
    def handle_message(self, message: dict) -> dict:
        method = message.get("method")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": message["id"],
                "result": {
                    "protocolVersion": "2025-03-26",
                    "serverInfo": {"name": "calc-server", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": message["id"],
                "result": {"tools": list(self.tools.values())}
            }
        
        elif method == "tools/call":
            name = message["params"]["name"]
            args = message["params"]["arguments"]
            result = self.execute_tool(name, args)
            return {
                "jsonrpc": "2.0",
                "id": message["id"],
                "result": {"content": [{"type": "text", "text": str(result)}]}
            }
    
    def execute_tool(self, name: str, args: dict):
        if name == "calculator":
            expr = args.get("expr", "")
            try:
                return eval(expr, {"__builtins__": {}}, {"abs": abs, "round": round})
            except Exception as e:
                return f"计算错误: {e}"
    
    def run(self):
        """通过 stdio 运行 MCP Server"""
        for line in sys.stdin:
            try:
                message = json.loads(line.strip())
                response = self.handle_message(message)
                print(json.dumps(response), flush=True)
            except Exception as e:
                error = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": str(e)}
                }
                print(json.dumps(error), flush=True)

if __name__ == "__main__":
    MCPServer().run()
```

### 3.6 MCP 的生态与前景

截至 2026 年 7 月，MCP 生态已相当丰富：

- **官方实现**：Anthropic 提供 Python、TypeScript、Java 和 Kotlin SDK
- **客户端支持**：Claude Desktop、Cursor、VS Code（通过 Copilot）、JetBrains IDE、Hermes Agent
- **预置服务器**：文件系统、数据库（PostgreSQL/MySQL/SQLite）、浏览器（Playwright/Puppeteer）、Git、Slack、Notion、飞书
- **工具链**：MCP Inspector（调试工具）、MCP Proxy（网关）、MCP Registry（服务目录）

MCP 的出现标志着 LLM 工具调用从**私有 API 时代**迈入**开放协议时代**，这类似于 HTTP 对 Web 的意义——统一的标准催生了繁荣的生态。

---

## 四、Agent 框架中的工具编排

### 4.1 从单工具到多工具编排

单一工具调用并不复杂，真正的挑战在于**多工具编排**——Agent 需要自主决定调用哪些工具、以什么顺序调用、如何处理中间结果。

Agent 框架中的编排模式主要有三种：

| 模式 | 描述 | 适用场景 | 代表框架 |
|------|------|----------|----------|
| **线性链** | 按顺序依次调用工具 | 固定流程（如：搜索→总结→报告） | LangChain Chain |
| **DAG 执行** | 有向无环图，依赖并行 | 复杂多步骤任务 | LlamaIndex |
| **ReAct 循环** | 动态推理→行动→观察循环 | 开放探索型任务 | AutoGPT, Hermes Agent |
| **Plan-and-Solve** | 先规划再逐步执行 | 需全局规划的长任务 | HuggingGPT, BabyAGI |

### 4.2 工具调用的核心挑战

**1. 幻觉控制**

工具调用结果中，最危险的错误并非"调用失败"，而是**"模型幻觉出工具调用"**——模型编造了一个不存在的调用并"假装"成功。解决方案：

- 严格校验工具名称和参数 Schema
- 在训练阶段加入负样本（不应调用工具的场景）
- 使用 `tool_choice: "required"` 强制关键流程必须调用

**2. 上下文窗口管理**

工具返回值可能非常庞大。以文件读取为例，一次 `read_file` 可能返回 10 万行日志。高效管理：

```python
# 工具结果截断策略
def truncate_tool_result(result: str, max_tokens: int = 2000) -> str:
    tokens = len(result) // 2  # 粗略估算
    if tokens <= max_tokens:
        return result
    
    # 截取头部 + 尾部 + 中间省略
    head_len = max_tokens // 2
    tail_len = max_tokens // 4
    return (
        result[:head_len * 2] +
        f"\n\n... [中间省略 {tokens - head_len - tail_len} tokens] ...\n\n" +
        result[-tail_len * 2:]
    )
```

**3. 错误重试与回退**

工具调用的失败模式多样：超时、认证过期、限流、数据格式变更。成熟的 Agent 框架应有以下策略：

```python
class ToolRetryStrategy:
    def __init__(self, max_retries=3, backoff=1.0):
        self.max_retries = max_retries
        self.backoff = backoff
    
    async def execute_with_retry(self, tool_call_func, fallback=None):
        last_error = None
        for attempt in range(self.max_retries):
            try:
                return await tool_call_func()
            except RateLimitError:
                wait = self.backoff * (2 ** attempt)
                await asyncio.sleep(wait)
            except AuthError:
                await self.refresh_auth()
            except ToolNotFoundError:
                if fallback:
                    return await fallback()
                raise
        raise last_error or RuntimeError("所有重试均失败")
```

### 4.3 Hermes Agent 的工具调用设计

作为 Nous Research 出品的 Agent 框架，Hermes Agent 在工具调用方面做出了独特的设计选择：

**1. 统一的 Tool Executor 抽象**

所有工具通过统一的 `ToolExecutor` 接口注册和执行，支持 MCP 协议的标准工具和自定义 Python 函数：

```python
class ToolExecutor:
    def __init__(self):
        self._tools: dict[str, Tool] = {}
        self._mcp_clients: list[MCPClient] = []
    
    def register_tool(self, tool: Tool):
        self._tools[tool.name] = tool
    
    def register_mcp_server(self, server_config: dict):
        client = MCPClient(server_config)
        self._mcp_clients.append(client)
    
    def list_tools(self) -> list[dict]:
        tools = []
        for t in self._tools.values():
            tools.append(t.to_schema())
        for client in self._mcp_clients:
            tools.extend(client.get_tools())
        return tools
    
    async def execute(self, name: str, args: dict):
        if name in self._tools:
            return await self._tools[name].execute(**args)
        for client in self._mcp_clients:
            if name in client.tool_names:
                return await client.call_tool(name, args)
        raise ToolNotFoundError(name)
```

**2. 并行工具调用优化**

支持同时调用多个不相关的工具，极大提升效率：

```
用户："对比一下北京和上海今天的天气，顺便查一下明天的股票走势"
                          │
                    ┌─────┴─────┐
                    │  LLM 推理  │
                    └─────┬─────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        get_weather  get_weather  get_stock
        (北京)       (上海)       (市场指数)
              │           │           │
              └───────────┼───────────┘
                          ▼
                    综合结果回复
```

---

## 五、性能对比与选型指南

### 5.1 不同工具调用方案的对比

| 维度 | Native Function Calling | MCP 协议 | ReAct Prompt |
|------|------------------------|----------|-------------|
| **协议开放性** | 私有 API | 开放标准 | 无协议 |
| **跨模型兼容** | 仅同厂商 | 所有 MCP 客户端 | 理论上通用 |
| **部署复杂度** | 低（API 内置） | 中（需搭建 Server） | 极低 |
| **工具复用** | 需重复声明 | 一次声明到处用 | 需重复声明 |
| **错误处理** | API 内置 | 协议层定义 | 完全靠 prompt |
| **流式支持** | ✅ | ✅ | ❌ |
| **并行调用** | ✅ | ✅ | ❌ |
| **安全认证** | 应用层实现 | 协议层支持 | 无 |
| **工具发现** | 静态声明 | 动态发现 | 静态描述 |

### 5.2 选型建议

| 场景 | 推荐方案 | 理由 |
|------|----------|------|
| 快速原型验证 | Native Function Calling | 零配置，开箱即用 |
| 多模型迁移 | MCP 协议 | 一次开发，多模型适配 |
| 企业级安全要求 | MCP + SSE | 协议层认证与审计 |
| 本地文件处理 | MCP FileSystem Server | 开箱即用，权限可控 |
| 云端微服务 | MCP + Lambda Server | 弹性伸缩，低延迟 |
| 开源模型部署 | MCP + Llama 3 | 独立于 API 供应商 |

---

## 六、未来展望

### 6.1 工具调用的技术趋势

1. **多模态工具调用**：LLM 不仅能调用 API，还能直接操作 GUI（Computer Use）、控制浏览器、调用图像生成工具等

2. **工具调用安全**：引入"工具防火墙"——在 LLM 和工具之间加入策略引擎，防止注入攻击和权限滥用

3. **工具链的自动化组合**：不再需要手动编排，LLM 自治地将多个工具组合成复杂工作流

4. **Agent-to-Agent 协议**：一个 Agent 的工具调用结果可以被另一个 Agent 作为输入，MCP 可能演进为 Agent 间的通信协议

### 6.2 对开发者的建议

- **拥抱标准**：尽量基于 MCP 协议开发工具，而非绑定单一供应商的私有格式
- **关注可靠性**：工具调用是"Action"层面，失败的影响远大于"对话"层面——做好容错、记录审计日志
- **控制成本**：每次工具调用都意味着额外的 API 调用和 token 消耗，设计缓存策略和结果复用机制
- **安全第一**：永远不要将 LLM 的决策直接映射为系统操作，需要经过权限校验和人工确认的"安全闸门"

---

## 参考资料

1. OpenAI Function Calling 文档 - https://platform.openai.com/docs/guides/function-calling
2. Anthropic Tool Use 文档 - https://docs.anthropic.com/en/docs/build-with-claude/tool-use
3. Model Context Protocol 规范 - https://modelcontextprotocol.io/
4. Hermes Agent 文档 - https://hermes-agent.nousresearch.com/docs
5. ReAct: Synergizing Reasoning and Acting in Language Models - https://arxiv.org/abs/2210.03629
6. Toolformer: Language Models Can Teach Themselves to Use Tools - https://arxiv.org/abs/2302.04761

---

*本文由小糊涂虫原创于 2026-07-14。转载请注明出处。*
