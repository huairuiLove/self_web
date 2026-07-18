# AI Agent 面试准备：从概念、架构到工程落地

> 一份面向 Agent 岗位的学习路线。重点不是背名词，而是能把问题拆开、讲清 trade-off，并说明如何验证系统真的有效。

## 先建立一张总地图

一个 LLM 调用不等于 Agent。普通调用通常是「输入 → 输出」；Agent 则需要在目标约束下持续完成：

1. 感知任务与环境状态。
2. 规划下一步要做什么。
3. 选择并调用工具。
4. 观察工具结果并更新状态。
5. 判断是否完成，必要时重试或修正计划。

面试中可以把 Agent 概括为一个受约束的决策循环。工程实现往往包含模型、上下文、工具、记忆、执行器和评估器，而不是一个孤立的 prompt。

## 五个核心能力

### 规划

从 Chain-of-Thought、Tree-of-Thoughts、Graph-of-Thoughts，到 Plan-and-Solve，核心问题都是如何降低复杂任务中的遗漏、顺序错误和局部最优。面试时要补充：计划是否允许动态修改，子任务是否可并行，以及失败后由谁决定重试。

### 工具使用

工具是 Agent 连接现实世界的边界。搜索、数据库、代码执行、业务 API 和浏览器操作都应有明确的 schema、权限、超时、重试和审计策略。模型可以提出调用，但最终执行器必须验证参数和权限。

### 记忆

短期记忆解决当前上下文，长期记忆解决跨会话复用。RAG、向量数据库、情节记忆和程序记忆适合不同问题，不要把所有历史对话无差别塞回 prompt。

### 感知与行动

Agent 可能同时处理文本、图像、结构化数据和环境反馈。感知结果要保留来源与置信度，行动要尽量幂等、可撤销、可观测。

### 评估与安全

除了最终答案，还要评估任务成功率、工具调用正确率、轨迹长度、成本、延迟、鲁棒性和安全违规率。生产系统必须把 prompt injection、越权工具调用、敏感数据泄露和无限循环作为一等问题。

## 面试回答模板

遇到「如何设计一个 Agent」时，可以按以下顺序回答：

1. 先定义任务边界、成功标准和不可做的事情。
2. 选择单 Agent、工作流或多 Agent，并解释原因。
3. 描述状态、工具 schema、记忆和执行循环。
4. 说明失败处理、超时、幂等、人工确认和回滚。
5. 给出离线数据集、在线指标和灰度方案。
6. 最后补充成本、延迟、隐私和安全护栏。

## 推荐学习顺序

先读 ReAct 和 Plan-and-Solve 理解推理与行动，再读 Toolformer、RAG、AutoGen、SWE-bench 和 AgentBench，最后补安全与 GUI Agent。每读一篇论文，至少留下三句话：它解决了什么、代价是什么、我会如何在工程中验证它。

## 相关论文

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)
- [A Survey on Large Language Model based Autonomous Agents](https://arxiv.org/abs/2308.11432)
- [The Agent Security Bench](https://arxiv.org/abs/2406.16585)
