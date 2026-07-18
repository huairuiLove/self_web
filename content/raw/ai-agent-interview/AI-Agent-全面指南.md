# AI Agent 全面指南 —— 概念、架构与必读论文

> 面向 Agent 岗位面试准备的系统性知识整理

---

## 目录

1. [什么是 AI Agent](#1-什么是-ai-agent)
2. [Agent 的核心能力](#2-agent-的核心能力)
3. [Agent 架构范式](#3-agent-架构范式)
4. [关键概念详解](#4-关键概念详解)
5. [Agent 评估](#5-agent-评估)
6. [必读论文清单（按主题分类）](#6-必读论文清单按主题分类)
7. [面试常见问题](#7-面试常见问题)

---

## 1. 什么是 AI Agent

### 1.1 定义

**AI Agent（智能体）** 是一个能够感知环境、自主决策、执行动作以实现目标的系统。在 LLM 时代，Agent 通常指：

> 以 **大语言模型（LLM）为"大脑"**，具备 **规划、记忆、工具使用** 能力，能够自主完成复杂任务的智能系统。

### 1.2 Agent 与普通 LLM 调用的区别

| 维度 | 普通 LLM 调用 | AI Agent |
|------|-------------|----------|
| 交互模式 | 单轮/多轮对话 | 自主循环执行 |
| 外部交互 | 无 | 调用工具、API、代码 |
| 记忆 | 仅上下文窗口 | 短期+长期记忆 |
| 决策 | 一次生成 | 规划→执行→观察→反思 |
| 任务复杂度 | 简单问答 | 多步骤复杂任务 |

### 1.3 Agent 的数学定义（经典 RL 视角）

Agent 可以被形式化为一个 **POMDP（部分可观测马尔可夫决策过程）**：

- **S**: 环境状态空间
- **A**: 动作空间
- **O**: 观测空间
- **T(s'|s, a)**: 状态转移函数
- **R(s, a)**: 奖励函数
- **π(a|o)**: 策略（Agent 的核心——给定观测选择动作）

---

## 2. Agent 的核心能力

### 2.1 🧠 规划（Planning）

Agent 需要将复杂目标分解为可执行的子任务序列。

#### 关键方法

**a) 思维链（Chain-of-Thought, CoT）**
- 在推理时生成中间推理步骤
- 代表性论文: Wei et al., 2022

**b) 思维树（Tree-of-Thoughts, ToT）**
- 同时探索多条推理路径，用 BFS/DFS 搜索
- 代表性论文: Yao et al., 2023

**c) 思维图（Graph-of-Thoughts, GoT）**
- 将推理建模为有向图，允许合并/分叉/循环
- 代表性论文: Besta et al., 2023

**d) 分解式规划（Decomposed Planning）**
- ReAct: 交替进行 Reasoning 和 Action
- Plan-and-Solve: 先制定计划再逐步执行
- DEPS: 面向开放世界游戏的分解式规划

**e) 自我反思（Self-Reflection）**
- Reflexion: 从失败中学习，维护反思记忆
- Self-Refine: 迭代优化输出

---

### 2.2 🔧 工具使用（Tool Use）

Agent 需要调用外部工具来突破 LLM 的固有限制（知识截止日期、计算能力、多模态感知）。

#### 工具类型

| 工具类别 | 示例 | 解决的问题 |
|---------|------|-----------|
| **搜索/检索** | Google Search, Bing, 向量数据库 | 知识截止、幻觉 |
| **代码执行** | Python REPL, Shell | 精确计算、数据处理 |
| **API 调用** | 日历、邮件、支付 | 与现实世界交互 |
| **多模态** | 图像生成、语音识别 | 感知能力扩展 |
| **数据库** | SQL, 图数据库 | 结构化知识查询 |
| **专用模型** | 翻译模型、OCR | 领域深度能力 |

#### 工具学习范式

1. **零样本工具使用**: 通过 prompt 描述工具，LLM 直接生成调用
2. **少样本工具学习**: 提供工具使用示例
3. **微调工具使用**: 在工具调用数据上微调模型（如 Gorilla, Toolformer）

#### 关键概念：Function Calling

现代 LLM（GPT-4, Claude）原生支持 Function Calling —— 模型输出结构化的函数调用参数而非自由文本。

```json
// LLM 输出的 Function Call
{
  "name": "get_weather",
  "arguments": {
    "location": "Beijing",
    "unit": "celsius"
  }
}
```

---

### 2.3 🗂️ 记忆（Memory）

Agent 的记忆系统模仿人类记忆结构：

#### 记忆层次

```
┌─────────────────────────────────────────┐
│            Agent 记忆系统                 │
├─────────────────────────────────────────┤
│  🧠 感觉记忆 (Sensory)                    │
│  └─ 当前交互的原始输入（嵌入表示）          │
│                                          │
│  💭 短期记忆 (Short-term / Working)       │
│  └─ 对话上下文窗口                        │
│  └─ Scratchpad（中间推理结果）             │
│                                          │
│  📚 长期记忆 (Long-term)                  │
│  ├─ 情节记忆 (Episodic): 过去交互经验      │
│  ├─ 语义记忆 (Semantic): 外部知识库        │
│  └─ 程序记忆 (Procedural): 工作流程/技能   │
└─────────────────────────────────────────┘
```

#### 关键实现技术

**a) RAG（检索增强生成）**
- 将外部知识编码为向量存入数据库
- 查询时检索相关片段注入上下文
- 代表性工作: RAG (Lewis et al., 2020)

**b) MemGPT / Letta**
- 操作系统式内存管理
- 主内存（上下文窗口）+ 外存（向量数据库）的分层设计
- 支持内存分页和上下文交换

**c) Reflexion 记忆**
- 存储"失败→反思→改进"的经验元组
- 作为长期记忆指导未来行动

**d) 向量数据库方案**
- Chroma, Pinecone, Weaviate, Milvus, Qdrant
- 基于语义相似度的记忆检索

---

### 2.4 👁️ 感知（Perception）

Agent 需要理解多种形式的输入：

- **文本**: 自然语言指令、API 文档
- **视觉**: 截图、UI 界面、图表（多模态模型实现）
- **结构化数据**: JSON, 表格, 代码
- **环境反馈**: 错误信息、执行结果

---

### 2.5 🎬 行动（Action）

Agent 的动作空间：

| 动作类型 | 粒度 | 示例 |
|---------|------|------|
| 语言生成 | 粗 | 回复用户、写报告 |
| 工具调用 | 中 | 查天气、搜网页 |
| 代码执行 | 中 | 运行 Python、SQL |
| 环境操作 | 细 | 点击按钮、输入文本（GUI Agent） |
| 物理动作 | 细 | 机器人控制（Embodied Agent） |

---

## 3. Agent 架构范式

### 3.1 ReAct 范式（Reasoning + Acting）

最经典的单 Agent 范式，交替进行推理和行动。

```
循环:
  1. Thought: 分析当前状态，决定下一步
  2. Action: 执行选定的工具/动作
  3. Observation: 观察执行结果
  4. 判断是否完成目标，否则回到步骤 1
```

```
示例:
  Thought: 我需要知道今天北京的温度来判断穿什么
  Action: get_weather("Beijing")
  Observation: 北京今天 35°C，晴天
  Thought: 35°C 很热，建议穿短袖。任务完成。
  Final Answer: 今天北京 35°C，建议穿短袖和防晒。
```

**代表性论文**: ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022)

---

### 3.2 Plan-then-Execute 范式

先完整规划，再逐步执行。

```
阶段1 - 规划:
  LLM 生成完整的步骤计划:
  Step 1: 读取 CSV 文件
  Step 2: 计算每列的均值
  Step 3: 生成可视化图表
  Step 4: 撰写分析报告

阶段2 - 执行:
  依次执行每个步骤，中途可调整
```

**代表性论文**: Plan-and-Solve (Wang et al., 2023)

---

### 3.3 Multi-Agent 范式

多个 Agent 协作完成复杂任务。

#### 常见的多 Agent 拓扑

```
a) 层级式 (Hierarchical)
     Manager Agent
       /    |    \
   Worker1 Worker2 Worker3

b) 流水线式 (Pipeline)
   Agent1 → Agent2 → Agent3 → Output

c) 辩论式 (Debate)
   Agent1 ↔ Agent2  (反复辩论直到达成一致)

d) 动态团队 (Dynamic Teaming)
   根据任务自动组建和调整团队结构
```

#### 关键概念

- **角色分配**: 每个 Agent 有特定的角色和职责（如"程序员"、"测试员"、"项目经理"）
- **通信协议**: Agent 之间如何交换信息（自然语言、结构化消息）
- **共识机制**: 如何从多个 Agent 的输出中得出最终决策
- **记忆共享**: 共享记忆池 vs 独立记忆

**代表性工作**: AutoGen (Microsoft), CrewAI, MetaGPT, ChatDev

---

### 3.4 Reflexion / Self-Improvement 范式

Agent 从自己的错误中学习。

```
循环:
  1. Actor: 根据当前策略执行动作
  2. Evaluator: 评估执行结果（成功/失败/部分成功）
  3. Self-Reflection: 如果失败，生成反思（为什么失败？如何改进？）
  4. Memory: 将反思存入长期记忆
  5. 用更新后的记忆重新尝试
```

**代表性论文**: Reflexion (Shinn et al., 2023)

---

### 3.5 Code-Generation Agent 范式

Agent 通过生成和执行代码来完成任务（代码作为中间表示更精确、更易验证）。

```
循环:
  1. 分析任务需求
  2. 生成代码（Python/Shell/SQL）
  3. 在沙箱中执行代码
  4. 分析执行结果（输出/错误）
  5. 如果失败，根据错误信息修复代码；否则完成任务
```

**代表性工作**: CodeAct, SWE-Agent, OpenDevin

---

### 3.6 Computer Use / GUI Agent 范式

Agent 像人一样操作计算机界面。

```
感知: 截图 → 多模态模型理解屏幕内容
行动: 鼠标点击(x,y)、键盘输入、滚动
```

**代表性工作**: Claude Computer Use, OS-Copilot, UFO, SeeClick

---

## 4. 关键概念详解

### 4.1 Token 与上下文窗口

- **Token**: LLM 处理文本的最小单位（≈0.75 英文单词，≈1.5 中文字）
- **上下文窗口**: 模型一次能"看到"的最大 token 数
  - GPT-4 Turbo: 128K
  - Claude 4 Opus: 200K
  - Gemini 2.5 Pro: 1M+
- **对 Agent 的影响**: 上下文窗口就是 Agent 的"工作记忆"容量
- **长上下文的问题**:
  - 注意力稀释（"Lost in the Middle"）
  - 成本增加（按 token 计费）
  - 延迟增加

### 4.2 Tool Definition & Function Calling

**工具定义**是描述工具能力的结构化 schema：

```json
{
  "name": "search_database",
  "description": "在知识库中搜索相关文档",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "搜索查询关键词"
      },
      "top_k": {
        "type": "integer",
        "description": "返回的最相关文档数量",
        "default": 5
      }
    },
    "required": ["query"]
  }
}
```

**关键挑战**:
- 工具选择（太多了选哪个？）
- 参数填充（如何从对话中提取参数？）
- 并行调用 vs 串行调用
- 错误处理（工具调用失败后怎么办？）

### 4.3 Agent Loop（Agent 控制循环）

Agent 的核心是控制循环（Agent Loop），也称为 Agentic Loop：

```
while not task_complete and steps < max_steps:
    1. 构建上下文（系统提示词 + 历史 + 工具定义 + 最新观测）
    2. LLM 推理 → 输出 (Thought, Action/Function Call)
    3. 如果是工具调用 → 执行工具 → 获得 Observation
    4. 如果是最终答案 → 结束
    5. 更新历史（追加 Thought/Action/Observation）
```

### 4.4 上下文工程（Context Engineering）

为 Agent 构建有效上下文的艺术：

- **System Prompt 设计**: Agent 的角色、能力边界、行为规范
- **工具描述优化**: 清晰、准确、带示例的工具文档
- **Few-shot 示例**: 在提示中加入成功的 Agent 交互示例
- **上下文压缩**: 当历史过长时进行摘要/压缩
- **结构化输出**: 要求 Agent 按特定格式输出（JSON, XML, Markdown）

### 4.5 Guardrails & Safety（安全护栏）

- **输入护栏**: 检测恶意/不当输入
- **输出护栏**: 验证输出格式和内容安全性
- **工具护栏**: 限制工具调用权限（如不允许 rm -rf）
- **人工审核（Human-in-the-Loop）**: 关键操作前请求人类确认
- **Token 预算**: 限制单次任务的最大 token 消耗
- **超时机制**: 防止 Agent 陷入死循环

### 4.6 Grounding（扎根/对齐）

确保 Agent 的输出与事实和工具返回结果一致（减少幻觉）：

- **工具返回优先**: 始终以工具返回的实际结果为准
- **引用溯源**: 输出的每个事实都要能追溯到具体来源
- **不确定性表达**: 不确定时说"不确定"，不要编造

### 4.7 Routing & Intent Classification（路由与意图分类）

在多 Agent 系统中，需要将用户请求路由到正确的 Agent：

```
用户请求 → 意图分类器 → 路由到对应 Agent
         ├─ 编程任务 → Coding Agent
         ├─ 数据分析 → Data Agent
         ├─ 客服问答 → Support Agent
         └─ 通用对话 → General Agent
```

---

## 5. Agent 评估

### 5.1 评估维度

| 维度 | 描述 | 指标 |
|------|------|------|
| **任务成功率** | 是否完成了用户指定的目标 | Pass@1, Success Rate |
| **效率** | 完成任务的代价 | Token 消耗、步数、时间 |
| **工具使用准确率** | 是否正确选择了工具和参数 | Tool Selection Accuracy |
| **鲁棒性** | 面对错误/意外情况的恢复能力 | Recovery Rate |
| **安全性** | 是否产生有害/不安全的行为 | Harmfulness Score |
| **泛化能力** | 在新任务/新工具上的表现 | Cross-task Performance |

### 5.2 主流 Benchmark

| Benchmark | 领域 | 描述 |
|-----------|------|------|
| **SWE-Bench** | 软件工程 | 真实 GitHub Issue 修复 |
| **WebArena** | Web 导航 | 模拟网站上的交互任务 |
| **GAIA** | 通用推理 | 多步骤推理 + 工具使用 |
| **AgentBench** | 多维评估 | 8 个环境（OS、DB、KG 等）|
| **ToolBench** | 工具使用 | 大规模工具调用评估 |
| **τ-Bench** | 真实场景 | 客服、旅行预订等真实任务 |
| **OSWorld** | OS 操作 | 真实操作系统环境中的任务 |
| **MINT** | 多轮交互 | 通过多轮对话完成任务 |

---

## 6. 必读论文清单（按主题分类）

### 🌟 综述/入门（必读）

| # | 论文 | 年份 | 关键贡献 | 阅读优先级 |
|---|------|------|---------|-----------|
| 1 | **[A Survey on Large Language Model based Autonomous Agents](https://arxiv.org/abs/2308.11432)** (Wang et al.) | 2023 | 最全面的 LLM Agent 综述，覆盖架构、应用、评估 | ⭐⭐⭐⭐⭐ |
| 2 | **[The Rise and Potential of Large Language Model Based Agents: A Survey](https://arxiv.org/abs/2309.07864)** (Xi et al.) | 2023 | 从社会学视角审视 AI Agent | ⭐⭐⭐⭐⭐ |
| 3 | **[Agent AI: Surveying the Horizons of Multimodal Interaction](https://arxiv.org/abs/2401.03568)** | 2024 | 多模态 Agent 的综合综述 | ⭐⭐⭐⭐ |

### 🏗️ Agent 架构与推理范式

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|---------|
| 4 | **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** (Yao et al.) | 2022 | 提出 ReAct 范式：交替推理与行动。**Agent 领域基石论文** |
| 5 | **[Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)** (Wei et al.) | 2022 | 思维链激发 LLM 推理能力 |
| 6 | **[Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)** (Yao et al.) | 2023 | 树状搜索多条推理路径 |
| 7 | **[Graph of Thoughts: Solving Elaborate Problems with Large Language Models](https://arxiv.org/abs/2308.09687)** (Besta et al.) | 2023 | 将推理建模为有向图，支持合并和回溯 |
| 8 | **[Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning](https://arxiv.org/abs/2305.04091)** (Wang et al.) | 2023 | 先规划再求解的推理策略 |
| 9 | **[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)** (Shinn et al.) | 2023 | 自我反思机制：从错误中学习 |
| 10 | **[Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)** (Madaan et al.) | 2023 | 通过自我反馈迭代优化输出 |

### 🛠️ 工具使用与 Function Calling

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|---------|
| 11 | **[Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)** (Schick et al.) | 2023 | 让 LLM 自主学会使用工具的里程碑工作 |
| 12 | **[Gorilla: Large Language Model Connected with Massive APIs](https://arxiv.org/abs/2305.15334)** | 2023 | 连接海量 API 的 LLM，减少幻觉 |
| 13 | **[ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs](https://arxiv.org/abs/2307.16789)** (Qin et al.) | 2023 | 大规模工具学习的指令调优方法 |
| 14 | **[MM-REACT: Prompting ChatGPT for Multimodal Reasoning and Action](https://arxiv.org/abs/2303.11381)** (Yang et al.) | 2023 | 多模态工具使用的先驱工作 |
| 15 | **[API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs](https://arxiv.org/abs/2304.08244)** | 2023 | 工具使用能力的全面评估基准 |

### 🧠 记忆与 RAG

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|---------|
| 16 | **[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** (Lewis et al.) | 2020 | RAG 原始论文，检索增强生成的奠基工作 |
| 17 | **[MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)** (Packer et al.) | 2023 | 操作系统式内存管理，主存+外存分层设计 |
| 18 | **[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)** (Park et al.) | 2023 | 记忆流+反思+规划的记忆架构，Stanford AI Town |

### 👥 多 Agent 系统

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|---------|
| 19 | **[AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155)** (Wu et al.) | 2023 | Microsoft 的多 Agent 对话框架 |
| 20 | **[MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352)** (Hong et al.) | 2023 | 模拟软件公司的多 Agent 框架（PM+架构师+工程师） |
| 21 | **[ChatDev: Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924)** (Qian et al.) | 2023 | 多 Agent 协作软件开发 |
| 22 | **[CAMEL: Communicative Agents for "Mind" Exploration](https://arxiv.org/abs/2303.17760)** (Li et al.) | 2023 | 角色扮演式 Agent 通信框架 |
| 23 | **[Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325)** (Du et al.) | 2023 | 多 Agent 辩论提高事实性和推理质量 |

### 💻 代码生成 Agent（软件工程方向）

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|---------|
| 24 | **[SWE-Agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793)** (Yang et al.) | 2024 | Agent-Computer Interface 设计，SWE-Bench 高性能 Agent |
| 25 | **[SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770)** (Jimenez et al.) | 2023 | 真实 GitHub Issue 修复的评估基准 |
| 26 | **[OpenDevin: An Open Platform for AI Software Developers as Generalist Agents](https://arxiv.org/abs/2407.16741)** | 2024 | 开源通用软件工程 Agent 平台 |
| 27 | **[Devin: The AI Software Engineer](https://www.cognition.ai/blog/introducing-devin)** | 2024 | Cognition AI 的商业化软件工程 Agent |

### 🖥️ GUI/Computer Use Agent

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|---------|
| 28 | **[OS-Copilot: Towards Generalist Computer Agents with Self-Improvement](https://arxiv.org/abs/2402.07456)** (Wu et al.) | 2024 | 通用计算机操作 Agent，自我改进 |
| 29 | **[UFO: A UI-Focused Agent for Windows OS Interaction](https://arxiv.org/abs/2402.07939)** (Zhang et al.) | 2024 | Windows 操作系统的 UI 交互 Agent |
| 30 | **[WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854)** (Zhou et al.) | 2023 | 真实 Web 环境中的 Agent 评估 |

### 🎯 Agent 评估与安全

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|---------|
| 31 | **[GAIA: A Benchmark for General AI Assistants](https://arxiv.org/abs/2311.12983)** (Mialon et al.) | 2023 | Meta 的通用 AI 助手评估基准 |
| 32 | **[AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688)** (Liu et al.) | 2023 | 首个系统性的 Agent 多维评估基准 |
| 33 | **[τ-Bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045)** | 2024 | 真实世界领域的工具-Agent-用户交互评估 |
| 34 | **[The Agent Security Bench (ASB)](https://arxiv.org/abs/2406.16585)** | 2024 | Agent 安全基准测试 |
| 35 | **[MINT: Evaluating LLMs in Multi-Turn Interaction with Tools](https://arxiv.org/abs/2309.10691)** | 2023 | 多轮工具交互评估 |

### 🔬 前沿/进阶

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|---------|
| 36 | **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** (Wang et al.) | 2023 | Minecraft 中的终身学习 Agent，自动技能库构建 |
| 37 | **[Describe, Explain, Plan and Select (DEPS)](https://arxiv.org/abs/2302.01560)** (Wang et al.) | 2023 | 面向开放世界游戏的分解式规划 |
| 38 | **[HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face](https://arxiv.org/abs/2303.17580)** (Shen et al.) | 2023 | 用 LLM 编排 HuggingFace 上多个 AI 模型 |
| 39 | **[TaskWeaver: A Code-First Agent Framework](https://arxiv.org/abs/2311.17541)** (Qiao et al.) | 2023 | 代码优先的 Agent 框架 |
| 40 | **[AutoWebGLM: A Large Language Model-based Web Navigating Agent](https://arxiv.org/abs/2404.03648)** | 2024 | 基于 LLM 的 Web 导航 Agent |

---

## 7. 面试常见问题

### 基础概念

1. **什么是 AI Agent？它和传统的 Chatbot 有什么区别？**
2. **Agent 需要哪些核心能力？**
3. **什么是 ReAct 范式？画一下它的流程图。**
4. **Agent 记忆系统如何设计？短期记忆和长期记忆的区别？**
5. **什么是 Function Calling？它的实现原理是什么？**

### 架构设计

6. **如何设计一个可扩展的 Multi-Agent 系统？**
7. **Agent 之间如何通信和协作？有哪些常见的通信拓扑？**
8. **如何处理 Agent 的工具调用错误？设计一个重试/回退策略。**
9. **上下文窗口有限，如何处理长任务？**
10. **如何在 Agent 系统中实现 Human-in-the-Loop？**

### 工程实践

11. **你如何评估一个 Agent 系统的好坏？**
12. **Agent 陷入死循环怎么办？有哪些防护措施？**
13. **如何降低 Agent 的 Token 消耗和延迟？**
14. **如何在 Agent 中实现流式输出（Streaming）？**
15. **你设计 Agent 时会考虑哪些安全问题？**

### 深度思考

16. **Agent 的幻觉问题比普通 LLM 更严重还是更轻微？为什么？**
17. **你认为 Agent 的下一步突破会在哪个方向？**
18. **Autonomous Agent vs Assistive Agent 的边界在哪里？**
19. **如何平衡 Agent 的自主性和可控性？**
20. **Agent 的 scaling law 是什么？更大模型 vs 更好架构，哪个更重要？**

---

## 推荐学习路径

```
Week 1-2: 基础概念
  ├─ 读综述 #1, #2
  ├─ 读 ReAct (#4) + CoT (#5)
  └─ 动手: 用 LangChain/AutoGen 搭一个简单 Agent

Week 3-4: 工具使用与记忆
  ├─ 读 Toolformer (#11) + MemGPT (#17)
  ├─ 读 RAG (#16)
  └─ 动手: 给你的 Agent 加工具调用 + 向量记忆

Week 5-6: 多 Agent 系统
  ├─ 读 AutoGen (#19) + MetaGPT (#20) + CAMEL (#22)
  ├─ 读 Reflexion (#9)
  └─ 动手: 搭一个多 Agent 协作系统

Week 7-8: 专项 + 评估
  ├─ 读 SWE-Agent (#24) + SWE-Bench (#25)
  ├─ 读 GAIA (#31) + AgentBench (#32)
  └─ 动手: 在 SWE-Bench Lite 上跑一个 Agent
```

---

> 💡 **面试提示**: 面试官不仅关心你读过什么论文，更关心你能否**解释清楚核心概念**、**说出各方法的 trade-off**、以及**展示实际的工程经验**。建议精读 5-8 篇核心论文（标记 ⭐⭐⭐⭐⭐ 的），对其余的能说出"做什么的"和"解决了什么问题"即可。
