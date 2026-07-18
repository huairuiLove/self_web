# ReAct：为什么 Agent 要把推理和行动交替起来

> 论文笔记：[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)，Yao et al.，ICLR 2023。

## 它解决了什么问题

纯推理容易产生幻觉和错误传播，纯行动又缺少对当前状态的解释与计划。ReAct 的核心做法是让模型交替生成 reasoning trace 和 action，再把外部 observation 放回下一轮上下文。

```text
Thought -> Action -> Observation -> Thought -> ... -> Finish
```

Thought 用来拆任务、更新计划和处理异常；Action 负责调用搜索、知识库或环境接口；Observation 是来自工具的事实，而不是模型自己的猜测。

## 为什么比单独 CoT 或单独工具调用更实用

CoT 只在模型内部推理，无法主动获取缺失事实；只调用工具则容易在错误的搜索路径上持续执行。ReAct 把二者放进同一条轨迹，模型可以先判断需要什么信息，再调用工具，拿到结果后修正下一步。

论文在 HotpotQA、FEVER、ALFWorld 和 WebShop 等任务上验证了这一点：外部信息可以减少事实性错误，交替轨迹也更容易被人检查和调试。

## 工程实现时不能照搬的地方

论文中的 action space 很简单，生产系统需要额外加入：

- 工具参数 JSON Schema 与服务端二次校验。
- 每个工具的权限、超时、重试和速率限制。
- 对写操作增加用户确认、幂等键和审计日志。
- 对轨迹长度、token 消耗和重复调用设置预算。
- 把 observation 标记为外部数据，防止工具返回内容直接劫持后续 prompt。

## 面试中如何讲

一句话版本：ReAct 让模型在「思考下一步」与「执行并观察结果」之间循环，从而把内部推理和外部事实连接起来；它提升了可解释性与适应异常的能力，但需要执行器负责权限、安全和预算控制。

## 我的落地清单

先用一个只读搜索工具实现最小闭环，再加入结构化 observation、失败重试和轨迹评估。等成功率稳定后，才开放写入型工具，并为每类副作用设计人工确认点。
