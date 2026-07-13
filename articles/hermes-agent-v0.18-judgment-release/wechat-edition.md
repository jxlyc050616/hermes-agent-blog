# 微信公众号排版版

> 自动生成于 2026-07-14  
> 来源：GitHub [hermes-agent-blog](https://github.com/jxlyc050616/hermes-agent-blog)

---

## 发布指引

### 封面图建议
- **方案 1（推荐）**：Excalidraw 手绘风格 - 多模型协作示意图，三色模型卡片汇聚到中间合成结果
- **方案 2**：深色背景文字封面 - 白色大字标题："Hermes Agent v0.18"，副标题："裁决版本/The Judgment Release"
- **方案 3**：终端截图 - `/model moa/my-council` 命令运行截图

### 标签建议
`#AI Agent` `#Hermes` `#MoA` `#多模型协作` `#开源`

### 排版提醒
- 代码块已添加深色背景和 overflow-x:auto（WeChat 移动端支持有限，建议 PC 端预览确认）
- 表格边框已内联处理，无外层 div 包装
- 已使用 GitHubDaily 风格青绿色 h3 标题
- strong 标签已添加 display:inline 防止 li 内断行

### 发布步骤
1. 将下方 HTML 复制到微信公众号编辑器「源代码」模式
2. 预览确认排版
3. 上传封面图
4. 群发或保存草稿

---

## 文章正文 HTML

```html
<h1 style="font-size:20px;font-weight:700;color:#1a1a1a;margin:24px 0 12px;padding:0 0 8px;border-bottom:2px solid #3866FF;">Hermes Agent v0.18 深度解析：当 AI Agent 学会自我验证、多模型协作和规模化部署</h1>
<h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:20px 0 10px;padding-left:10px;border-left:3px solid #3866FF;">引言</h2>
<p style="margin:1.5em 0;">2026 年 7 月 1 日，Nous Research 发布了 Hermes Agent v0.18.0，代号 <strong style="display:inline;">"The Judgment Release"</strong>（裁决版本）。如果说 v0.16 的惊喜是 Kanban Swarm 多智能体协作，v0.17 的亮点是安全与平台扩展，那么 v0.18 的核心命题只有一个：<strong style="display:inline;">质量</strong>。</p>
<p style="margin:1.5em 0;">过去 12 天，团队和社区几乎把全部精力投入到一个目标——<strong style="display:inline;">清零整个仓库的所有 P0 和 P1 问题</strong>。截至发布日期，<strong style="display:inline;">零个打开的 P0，零个打开的 P1</strong>。~692 个最高优先级事项在 12 天内全部解决，~1,950 个总 Issue 和 PR 被关闭。</p>
<p style="margin:1.5em 0;">但 v0.18 远不止是"大扫除"。它从根本上回答了三个问题：</p>
<ol style="margin:0.8em 0;padding-left:20px;list-style-type:decimal;">
<li style="margin:6px 0;"><strong style="display:inline;">AI Agent 如何判断自己真的做完了？</strong>——自我验证系统和完成契约</li>
<li style="margin:6px 0;"><strong style="display:inline;">如何让多个 AI 模型协作而不是互怼？</strong>——Mixture-of-Agents 成为一等公民</li>
<li style="margin:6px 0;"><strong style="display:inline;">AI Agent 如何在生产环境中可靠运行？</strong>——Scale-to-zero 和 drain 协调</li>
</ol>
<blockquote style="margin:14px 0;padding:12px 16px;background:#f5f7fa;border-left:4px solid #3866FF;color:#555;font-size:14px;border-radius:0 4px 4px 0;">
<p style="margin:1.5em 0;"><strong style="display:inline;">一句话概括</strong>：v0.18 让 Hermes 从一个"能用的 AI Agent"进化为一个"可信赖的 AI 工作平台"——它会证明自己的工作是正确完成的，而非仅仅声称。</p>
</blockquote>
<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
<h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:20px 0 10px;padding-left:10px;border-left:3px solid #3866FF;">一、P0/P1 清零：一场 12 天的闪电战</h2>
<p style="margin:1.5em 0;">在理解新功能之前，先看一组数字：</p>
<table style="border-collapse:collapse;width:100%;font-size:14px;margin:12px 0;">
<thead>
<tr>
<th style="background:#3866FF;color:#fff;padding:8px 10px;border:1px solid #ddd;text-align:left;font-weight:600;">指标</th>
<th style="background:#3866FF;color:#fff;padding:8px 10px;border:1px solid #ddd;text-align:left;font-weight:600;">数字</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">P0（严重）</strong> Issue</td>
<td style="padding:8px 10px;border:1px solid #ddd;">3 个</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">P0 PR</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">8 个</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">P1（高优先级）</strong> Issue</td>
<td style="padding:8px 10px;border:1px solid #ddd;">493 个</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">P1 PR</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">188 个</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">总计解决</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">~692 项</strong></td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">总 Issue/PR 关闭</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">~1,950 项</strong></td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">代码变更</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">~251,000 行新增 / ~41,000 行删除</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">合并 PR</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">998 个</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">贡献者</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">381 人</td>
</tr>
</tbody>
</table>
<p style="margin:1.5em 0;">最后一批关闭的是中断保护的压缩进程 fork bug（issue #56391）及其修复（#56416）——在发布前夜的冲刺中完成。</p>
<p style="margin:1.5em 0;">这不仅仅是一次代码清理。团队建立了 <strong style="display:inline;">P0/P1 保持归零</strong> 的承诺机制。这意味着从 v0.18 开始，Hermes Agent 的质量基线被永久抬高——不会有已知的严重或高优先级问题积压。</p>
<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
<h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:20px 0 10px;padding-left:10px;border-left:3px solid #3866FF;">二、Mixture-of-Agents：多模型协作从"噱头"变"基础设施"</h2>
<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">2.1 MoA 成为一等模型公民</h3>
<p style="margin:1.5em 0;">在 v0.18 之前，MoA 是一个需要手动切换的"模式"。现在每个命名的 MoA 预设都以<strong style="display:inline;">虚拟模型</strong>的形式出现在模型选择器中——和 Claude、GPT、Grok 并列：</p>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code>┌──────────────────────────────────────────────┐
│              Model Picker                     │
│  ┌────────────────────────────────────────┐  │
│  │ anthropic/claude-sonnet-4              │  │
│  │ openai/gpt-5                           │  │
│  │ grok/grok-3                            │  │
│  │ moa/my-council          ← 新！         │  │
│  │ moa/quick-triage        ← 新！         │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
</code></pre></div>

<p style="margin:1.5em 0;">选择 <code style="background:#f0f2f5;color:#d63384;border-radius:3px;padding:2px 6px;font-size:14px;font-family:Menlo,Consolas,monospace;">moa/my-council</code> 就像选择任何其他模型一样——Hermes 自动将你的 prompt 路由到整个专家面板，收集各方意见，合成最佳答案。这条路径在 CLI、TUI、桌面应用和网关上全部可用。</p>
<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">2.2 透明的模型推理过程</h3>
<p style="margin:1.5em 0;">MoA 最令人兴奋的 UX 改进是<strong style="display:inline;">推理可视化</strong>。每个参考模型的输出以带标签的代码块呈现：</p>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code><span class="err">┌─</span><span class="w"> </span><span class="nl">Reference:</span><span class="w"> </span><span class="n">GPT</span><span class="o">-</span><span class="mh">5</span><span class="w"> </span><span class="err">──────────────────────────┐</span>
<span class="err">│</span><span class="w"> </span><span class="err">从代码结构看，问题出在异步竞态条件上</span><span class="p">...</span><span class="w">       </span><span class="err">│</span>
<span class="err">│</span><span class="w"> </span><span class="err">建议在</span><span class="w"> </span><span class="n">dispatch</span><span class="w"> </span><span class="err">层加入分布式锁</span><span class="p">...</span><span class="w">             </span><span class="err">│</span>
<span class="err">└──────────────────────────────────────────────┘</span>

<span class="err">┌─</span><span class="w"> </span><span class="nl">Reference:</span><span class="w"> </span><span class="n">Claude</span><span class="w"> </span><span class="n">Sonnet</span><span class="w"> </span><span class="mh">4</span><span class="w"> </span><span class="err">─────────────────┐</span>
<span class="err">│</span><span class="w"> </span><span class="err">我同意竞态条件是根因，但分布式锁太重了。</span><span class="w">       </span><span class="err">│</span>
<span class="err">│</span><span class="w"> </span><span class="err">用</span><span class="w"> </span><span class="n">SQLite</span><span class="w"> </span><span class="err">的</span><span class="w"> </span><span class="n">WAL</span><span class="w"> </span><span class="err">模式</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="err">乐观锁更合适</span><span class="p">...</span><span class="w">       </span><span class="err">│</span>
<span class="err">└──────────────────────────────────────────────┘</span>

<span class="err">┌─</span><span class="w"> </span><span class="nl">Reference:</span><span class="w"> </span><span class="n">Grok</span><span class="w"> </span><span class="mh">3</span><span class="w"> </span><span class="err">──────────────────────────┐</span>
<span class="err">│</span><span class="w"> </span><span class="err">等等，看堆栈</span><span class="w"> </span><span class="n">trace</span><span class="w"> </span><span class="err">第</span><span class="w"> </span><span class="mh">47</span><span class="w"> </span><span class="err">行——是事件循环的</span><span class="w">     </span><span class="err">│</span>
<span class="err">│</span><span class="w"> </span><span class="err">任务调度顺序问题，不是锁的问题</span><span class="p">...</span><span class="w">             </span><span class="err">│</span>
<span class="err">└──────────────────────────────────────────────┘</span>

<span class="err">┌─</span><span class="w"> </span><span class="n">Aggregator</span><span class="w"> </span><span class="err">─────────────────────────────────┐</span>
<span class="err">│</span><span class="w"> </span><span class="err">综合三方分析：根因是</span><span class="w"> </span><span class="n">asyncio</span><span class="w"> </span><span class="err">任务调度顺序</span><span class="w">      </span><span class="err">│</span>
<span class="err">│</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">WAL</span><span class="w"> </span><span class="err">模式下的写冲突。方案：</span><span class="p">...</span><span class="w">               </span><span class="err">│</span>
<span class="err">└──────────────────────────────────────────────┘</span>
</code></pre></div>

<p style="margin:1.5em 0;">而且聚合器的<strong style="display:inline;">最终答案实时流式输出</strong>——你不会再盯着空白屏幕等待，而是能看到委员会"正在讨论"的过程。</p>
<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">2.3 MoA 架构的可靠性设计</h3>
<p style="margin:1.5em 0;">幕后有几个关键设计决策：</p>
<ul style="margin:0.8em 0;padding-left:20px;list-style-type:disc;">
<li style="margin:6px 0;"><strong style="display:inline;">参考模型和聚合器都通过各自 provider 的真实路由调用</strong>——不做任何取巧的简化</li>
<li style="margin:6px 0;"><strong style="display:inline;">上下文窗口从聚合器解析</strong>（而非默认 256K）——避免窗口溢出</li>
<li style="margin:6px 0;"><strong style="display:inline;">参考模型看到完整工具状态</strong>，在每次用户/工具响应后触发</li>
<li style="margin:6px 0;"><strong style="display:inline;">全轮 trace 持久化到 JSONL</strong>（通过 <code style="background:#f0f2f5;color:#d63384;border-radius:3px;padding:2px 6px;font-size:14px;font-family:Menlo,Consolas,monospace;">moa.save_traces</code> 配置）——用于调试和评估</li>
<li style="margin:6px 0;"><strong style="display:inline;">手改的 preset 配置也能容错</strong>——不会因为格式问题直接崩溃</li>
</ul>
<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
<h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:20px 0 10px;padding-left:10px;border-left:3px solid #3866FF;">三、自我验证系统：AI Agent 终于学会"证明自己是对的"</h2>
<p style="margin:1.5em 0;">这是 v0.18 最具哲学意义的改进。传统 AI Agent 有一个根本问题：<strong style="display:inline;">模型说"完成了" ≠ 真的完成了</strong>。</p>
<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">3.1 完成契约（Completion Contracts）</h3>
<p style="margin:1.5em 0;">v0.18 引入了 <code style="background:#f0f2f5;color:#d63384;border-radius:3px;padding:2px 6px;font-size:14px;font-family:Menlo,Consolas,monospace;">/goal</code> 的<strong style="display:inline;">完成契约</strong>机制。你声明"完成"长什么样，持续目标循环根据证据判断——而不是模型的主观声称：</p>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code><span class="c1"># 声明你的完成契约</span>
/goal<span class="w"> </span><span class="s2">&quot;修复项目中的所有类型错误&quot;</span><span class="w"> </span><span class="se">\</span>
<span class="w">  </span>--contract<span class="w"> </span><span class="s2">&quot;tsc --noEmit 返回零错误 AND 所有测试通过&quot;</span>
</code></pre></div>

<p style="margin:1.5em 0;">Agent 运行后不会说"I think I fixed it"——它会跑 <code style="background:#f0f2f5;color:#d63384;border-radius:3px;padding:2px 6px;font-size:14px;font-family:Menlo,Consolas,monospace;">tsc --noEmit</code>，检查输出，只有实际零错误时才标记完成。</p>
<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">3.2 编码验证证据账本</h3>
<p style="margin:1.5em 0;">一个新的 profile 级别的<strong style="display:inline;">验证证据账本</strong>记录了每次编码任务的标准检查结果：</p>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code><span class="n">coding_verification</span><span class="o">:</span>
<span class="w">  </span><span class="n">project</span><span class="o">:</span><span class="w"> </span><span class="n">my</span><span class="o">-</span><span class="n">app</span>
<span class="w">  </span><span class="n">checks</span><span class="o">:</span>
<span class="w">    </span><span class="o">-</span><span class="w"> </span><span class="n">type</span><span class="o">:</span><span class="w"> </span><span class="n">tsc</span>
<span class="w">      </span><span class="n">status</span><span class="o">:</span><span class="w"> </span><span class="n">passed</span>
<span class="w">      </span><span class="n">evidence</span><span class="o">:</span><span class="w"> </span><span class="s2">&quot;tsc --noEmit: 0 errors&quot;</span>
<span class="w">      </span><span class="n">timestamp</span><span class="o">:</span><span class="w"> </span><span class="mi">2026</span><span class="o">-</span><span class="mi">07</span><span class="o">-</span><span class="mi">14</span><span class="n">T10</span><span class="o">:</span><span class="mi">30</span><span class="o">:</span><span class="mi">00</span><span class="n">Z</span>
<span class="w">    </span><span class="o">-</span><span class="w"> </span><span class="n">type</span><span class="o">:</span><span class="w"> </span><span class="n">test</span>
<span class="w">      </span><span class="n">status</span><span class="o">:</span><span class="w"> </span><span class="n">passed</span>
<span class="w">      </span><span class="n">evidence</span><span class="o">:</span><span class="w"> </span><span class="s2">&quot;vitest run: 142/142 passed&quot;</span>
<span class="w">      </span><span class="n">timestamp</span><span class="o">:</span><span class="w"> </span><span class="mi">2026</span><span class="o">-</span><span class="mi">07</span><span class="o">-</span><span class="mi">14</span><span class="n">T10</span><span class="o">:</span><span class="mi">31</span><span class="o">:</span><span class="mi">00</span><span class="n">Z</span>
</code></pre></div>

<p style="margin:1.5em 0;">网关暴露了验证状态，外部系统也能查询 Agent 的工作到底有没有真的通过检查。</p>
<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">3.3 pre_verify 钩子</h3>
<p style="margin:1.5em 0;">如果你想接入自定义验证逻辑：</p>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code><span class="c1"># 在 coding_context 中</span>
<span class="nt">pre_verify</span><span class="p">:</span>
<span class="w">  </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="s">&quot;security-scan.sh&quot;</span>
<span class="w">    </span><span class="nt">timeout</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">120</span>
<span class="w">  </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="s">&quot;bundle-audit</span><span class="nv"> </span><span class="s">check</span><span class="nv"> </span><span class="s">--update&quot;</span>
<span class="w">    </span><span class="nt">timeout</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">60</span>
</code></pre></div>

<p style="margin:1.5em 0;">验证失败时，Agent 会自动进入修复循环，而非直接报完成。<strong style="display:inline;">"完成"的定义从 Agent 的嘴里转移到了可执行证据上。</strong></p>
<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
<h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:20px 0 10px;padding-left:10px;border-left:3px solid #3866FF;">四、/learn 和 /journey：Agent 的自我进化</h2>
<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">4.1 /learn —— 一句话创建可复用技能</h3>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code>/learn<span class="w"> </span>https://docs.example.com/api-reference
</code></pre></div>

<p style="margin:1.5em 0;">Hermes 自动爬取该 URL，提取关键概念和操作流程，按照你的 CONTRIBUTING.md 中的技能规范，生成一个结构化的 SKILL.md。你指向一个目录、一个 URL 或刚刚走过的交互流程——下一秒它就是一个可复用的技能。</p>
<p style="margin:1.5em 0;">这意味着 Agent <strong style="display:inline;">从今天开始能自己长技能</strong>。你不再需要手动写 SKILL.md 的 YAML frontmatter 和步骤列表。</p>
<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">4.2 /journey —— Agent 记忆的可视化时间线</h3>
<p style="margin:1.5em 0;">CLI 和 TUI 中新增了 <code style="background:#f0f2f5;color:#d63384;border-radius:3px;padding:2px 6px;font-size:14px;font-family:Menlo,Consolas,monospace;">/journey</code> 命令——一条<strong style="display:inline;">可交互的学习时间线</strong>，展示 Hermes 随时间积累的所有记忆和技能。你可以在视图中直接编辑或删除任何条目。</p>
<p style="margin:1.5em 0;">配合桌面版的<strong style="display:inline;">记忆图谱</strong>（一张自上而下、可交互的径向时间线），你终于能直观地看到你的 Agent 知道什么、它在什么时候学会的、有什么是该删掉的。</p>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code>        2026-06 ── 2026-07 ── 2026-07-14
           │           │            │
     [记忆: Ruben    [技能:     [记忆: 微信
      是 COO]       博客流水线]   API 编码坑]
</code></pre></div>

<p style="margin:1.5em 0;">Agent 的记忆再也不是一个黑盒。</p>
<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
<h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:20px 0 10px;padding-left:10px;border-left:3px solid #3866FF;">五、背景并行委派：派遣一支小型 AI 舰队</h2>
<p style="margin:1.5em 0;"><code style="background:#f0f2f5;color:#d63384;border-radius:3px;padding:2px 6px;font-size:14px;font-family:Menlo,Consolas,monospace;">delegate_task</code> 之前是一个<strong style="display:inline;">阻塞调用</strong>——你派出子 Agent，然后等着。现在它支持<strong style="display:inline;">背景并发扇出</strong>：</p>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code><span class="c1"># 一次派遣三个研究员并行工作</span>
delegate_task<span class="w"> </span>research-competitors<span class="w">  </span><span class="c1"># → 后台</span>
delegate_task<span class="w"> </span>audit-security<span class="w">        </span><span class="c1"># → 后台</span>
delegate_task<span class="w"> </span>analyze-performance<span class="w">   </span><span class="c1"># → 后台</span>
<span class="c1"># 你的聊天从未被阻塞！</span>

<span class="c1"># 当所有子 Agent 完成后，一个合并的结果自动回来</span>
</code></pre></div>

<p style="margin:1.5em 0;">CLI 和 TUI 的状态栏会实时显示有多少个后台子 Agent 正在运行。你可以一边审查代码、一边让三个子 Agent 并行研究竞品、审计安全、分析性能——所有结果在完成后一次性汇总。</p>
<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
<h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:20px 0 10px;padding-left:10px;border-left:3px solid #3866FF;">六、桌面应用：从聊天窗口到编程驾驶舱</h2>
<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">6.1 一等公民的编程项目</h3>
<p style="margin:1.5em 0;">桌面应用新增了真正的<strong style="display:inline;">项目系统</strong>——侧边栏显示你的代码库，编程导轨、审查面板、Git worktree 管理，全部建在一个 <code style="background:#f0f2f5;color:#d63384;border-radius:3px;padding:2px 6px;font-size:14px;font-family:Menlo,Consolas,monospace;">project → repo → lane</code> 模型上：</p>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code>┌──────────────────────────────────────────────────────┐
│  📁 Projects                    │  📝 Code Review     │
│  ├── my-app (React/TS)          │  ┌──────────────┐   │
│  ├── api-server (Python)        │  │ spec.ts       │   │
│  └── docs-site (MDX)            │  │ +42 -3 lines  │   │
│                                  │  └──────────────┘   │
│  🔧 Terminal                     │                     │
│  ┌──────────────────────────┐   │  🌳 Git Worktrees   │
│  │ $ npm run dev            │   │  ├── feat/auth      │
│  │ &gt; Ready on :3000         │   │  └── fix/typo       │
│  └──────────────────────────┘   │                     │
└──────────────────────────────────────────────────────┘
</code></pre></div>

<p style="margin:1.5em 0;">散布的聊天会话变成了 Agent 能理解、能操作的有组织项目。</p>
<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">6.2 其他桌面亮点</h3>
<ul style="margin:0.8em 0;padding-left:20px;list-style-type:disc;">
<li style="margin:6px 0;"><strong style="display:inline;">多终端面板</strong>——只读 Agent 终端，跨重启保持终端标签和滚动历史</li>
<li style="margin:6px 0;"><strong style="display:inline;">PR 风格文件 diff</strong>——聊天中的代码变更以 diff 视图呈现</li>
<li style="margin:6px 0;"><strong style="display:inline;">对话时间线导轨</strong>——长对话不再迷失</li>
<li style="margin:6px 0;"><strong style="display:inline;">浮动编辑器</strong>——弹出可拖拽的浮动输入窗口</li>
<li style="margin:6px 0;"><strong style="display:inline;">上下文使用量弹窗</strong>——随时知道上下文用了多少</li>
</ul>
<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
<h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:20px 0 10px;padding-left:10px;border-left:3px solid #3866FF;">七、网关 Scale-to-Zero：AI Agent 的生产级部署</h2>
<p style="margin:1.5em 0;">v0.18 的网关获得了两个关键能力：</p>
<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">7.1 空闲休眠（Dormant on Idle）</h3>
<p style="margin:1.5em 0;">当没有人跟 Hermes 对话时，网关自动进入休眠状态。当有消息进来时，它自动唤醒。对于托管或 relay-only 部署场景，这意味着<strong style="display:inline;">不活跃时零资源消耗</strong>。</p>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code>活跃 ──(60s 无活动)──→ 休眠 ──(新消息到达)──→ 活跃
</code></pre></div>

<h3 style="font-size:16px;font-weight:700;color:rgb(0,181,173);margin:1.2em 0 0.5em;padding:5px 0;">7.2 优雅排空（Drain Coordination）</h3>
<p style="margin:1.5em 0;">在重启、迁移或自动更新之前，网关可以执行<strong style="display:inline;">外部排空协调</strong>——等待所有飞行中的对话完成，将新的对话路由到其他节点，只有在确认安全后才关闭。不会有人在发送消息时被"咔嚓"切断。</p>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code><span class="c1"># 发送排空信号</span>
hermes<span class="w"> </span>gateway<span class="w"> </span>drain<span class="w"> </span>--timeout<span class="w"> </span><span class="m">300</span>
<span class="c1"># → 停止接收新对话</span>
<span class="c1"># → 等待当前对话完成（最多 300 秒）</span>
<span class="c1"># → 安全关闭</span>
</code></pre></div>

<p style="margin:1.5em 0;">这两个能力加在一起，让 Hermes 从"个人开发者的玩具"进化到"能部署给团队的生产级服务"。</p>
<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
<h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:20px 0 10px;padding-left:10px;border-left:3px solid #3866FF;">八、安全与可靠性：多层次加固</h2>
<p style="margin:1.5em 0;">v0.18 的安全轮加固了多个攻击面：</p>
<table style="border-collapse:collapse;width:100%;font-size:14px;margin:12px 0;">
<thead>
<tr>
<th style="background:#3866FF;color:#fff;padding:8px 10px;border:1px solid #ddd;text-align:left;font-weight:600;">加固类型</th>
<th style="background:#3866FF;color:#fff;padding:8px 10px;border:1px solid #ddd;text-align:left;font-weight:600;">内容</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">MCP 配置持久化</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">锁定攻击面，防止 prompt 注入持久化恶意配置</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">Cron credential 防泄漏</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">阻止 <code style="background:#f0f2f5;color:#d63384;border-radius:3px;padding:2px 6px;font-size:14px;font-family:Menlo,Consolas,monospace;">base_url</code> 覆盖窃取 provider 凭证</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">文件读取前缀密钥</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">不可重用的哨兵，防止前缀密钥泄漏</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">Slack token 脱敏</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">新增 <code style="background:#f0f2f5;color:#d63384;border-radius:3px;padding:2px 6px;font-size:14px;font-family:Menlo,Consolas,monospace;">xapp-</code> 级别 token 的脱敏覆盖</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">浏览器元数据分层</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">所有后端强制云元数据底层，重导航后重新检查私有网络守卫</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">Origin 隔离</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;"><code style="background:#f0f2f5;color:#d63384;border-radius:3px;padding:2px 6px;font-size:14px;font-family:Menlo,Consolas,monospace;">/resume</code> 和 <code style="background:#f0f2f5;color:#d63384;border-radius:3px;padding:2px 6px;font-size:14px;font-family:Menlo,Consolas,monospace;">/sessions</code> 限定调用者 origin，防止 IDOR</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">aiohttp CVE</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">惰性消息路径统一提升最低版本 + pin-drift 守卫</td>
</tr>
</tbody>
</table>
<p style="margin:1.5em 0;">新增了 <strong style="display:inline;">Google Vertex AI</strong> 作为一等 provider——通过服务账号 JSON 或应用默认凭证自动签发和刷新短生命周期的 OAuth2 token。如果你所在组织通过 Google Cloud 使用 Gemini，现在只需要指向服务账号文件即可。</p>
<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
<h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:20px 0 10px;padding-left:10px;border-left:3px solid #3866FF;">九、实战：用 v0.18 MoA 做技术决策</h2>
<p style="margin:1.5em 0;">假设你在做一个微服务架构选型，犹豫在 gRPC 和 REST 之间。以前你可能要手动提问多个模型再自己综合。现在：</p>
<div class="codehilite"><pre style="background:#1e1e1e;color:#d4d4d4;padding:14px;font-size:13px;line-height:1.45;white-space:pre;font-family:Menlo,Consolas,Courier,monospace;border-radius:6px;overflow-x:auto;margin:12px 0;"><span></span><code><span class="c1"># 切换到 MoA 预设</span>
/model<span class="w"> </span>moa/my-council

<span class="c1"># 直接问</span>
我需要为一个高吞吐的微服务系统做<span class="w"> </span>API<span class="w"> </span>协议选型。
候选：gRPC、REST<span class="w"> </span>+<span class="w"> </span>Protobuf、GraphQL。
请从性能、可维护性、团队上手成本、生态工具链四个维度分析。

<span class="c1"># 你会看到：</span>
<span class="c1"># Reference 1 (GPT-5): &quot;从性能角度，gRPC 的 HTTP/2 多路复用...&quot;</span>
<span class="c1"># Reference 2 (Claude): &quot;考虑团队经验曲线，REST + Protobuf 是...&quot;</span>
<span class="c1"># Reference 3 (Grok): &quot;如果是内部微服务通信，gRPC 更合适...&quot;</span>
<span class="c1"># Aggregator: &quot;综合三位专家的分析，建议方案是...&quot;</span>
</code></pre></div>

<p style="margin:1.5em 0;">这就是 v0.18 的核心价值：<strong style="display:inline;">不让一个模型替你做重大决策，而是让一个专家小组讨论后再作答。</strong></p>
<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
<h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:20px 0 10px;padding-left:10px;border-left:3px solid #3866FF;">总结</h2>
<p style="margin:1.5em 0;">v0.18 "The Judgment Release" 的四个关键词：</p>
<table style="border-collapse:collapse;width:100%;font-size:14px;margin:12px 0;">
<thead>
<tr>
<th style="background:#3866FF;color:#fff;padding:8px 10px;border:1px solid #ddd;text-align:left;font-weight:600;">关键词</th>
<th style="background:#3866FF;color:#fff;padding:8px 10px;border:1px solid #ddd;text-align:left;font-weight:600;">含义</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">清零</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">P0/P1 归零，质量基线永久抬高</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">协作</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">MoA 成为一等模型公民，多模型专家小组</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">验证</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">Agent 用证据证明完成，而非自我声称</td>
</tr>
<tr>
<td style="padding:8px 10px;border:1px solid #ddd;"><strong style="display:inline;">规模化</strong></td>
<td style="padding:8px 10px;border:1px solid #ddd;">Scale-to-zero + drain，拥抱生产部署</td>
</tr>
</tbody>
</table>
<p style="margin:1.5em 0;">从 v0.16 的 Kanban Swarm 多智能体协作，到 v0.18 的自我验证、多模型融合和规模化部署——Hermes Agent 正在从"一个很酷的 AI 工具"变成"一个可信赖的 AI 工作平台"。</p>
<p style="margin:1.5em 0;">而 381 位贡献者、998 个合并 PR、~1,950 个关闭的 Issue/PR——这些数字背后是一个社区在说同一句话：<strong style="display:inline;">AI Agent 不只是玩具，它已经准备好了。</strong></p>
<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
<p style="margin:1.5em 0;"><em>下一篇预告：我们将深入实战，展示如何用 v0.18 的 MoA + 自我验证系统，搭建一个零幻觉的自动化代码审查流水线。</em></p>
```

## 原文链接

GitHub 全文：https://github.com/jxlyc050616/hermes-agent-blog/blob/main/articles/hermes-agent-v0.18-judgment-release/index.md
