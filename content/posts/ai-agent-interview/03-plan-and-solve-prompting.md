# Plan-and-Solve：先做计划，能减少零样本推理的漏步吗

> 论文笔记：[Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning](https://arxiv.org/abs/2305.04091)，Wang et al.，2023。

## 从 Zero-shot CoT 到显式计划

Zero-shot CoT 用「Let's think step by step」诱导模型展开推理，但复杂问题中仍可能漏掉关键步骤，或者在计算和语义理解上出错。Plan-and-Solve 把触发语句改成两段要求：先理解问题并制定计划，再按计划逐步求解。

PS+ 进一步要求模型提取相关变量及数值、计算中间结果，并关注常识和算术。这些指令看似简单，却把「不要漏信息」和「不要跳过计算」明确写进了任务。

## 它适合什么场景

当任务能被拆成相对稳定的子任务时，显式计划很有帮助，例如多步数学题、结构化分析、数据处理和需要先收集信息再生成结论的 Agent 工作流。它不等于真正的规划器：模型生成的计划仍可能错误，也没有自动验证每一步是否可执行。

## 论文结果给我的启发

论文在十个数学、常识和符号推理数据集上比较了 Zero-shot CoT、PoT、PS/PS+ 与 few-shot 方法。PS+ 在多数算术数据集上明显优于普通 Zero-shot CoT，并接近部分 few-shot CoT 结果。

真正值得复用的不是某一句英文 prompt，而是三件事：

1. 把复杂目标拆成明确的子任务。
2. 要求模型显式保留关键变量与中间结果。
3. 把最终答案抽取与推理过程分开，减少格式干扰。

## 在 Agent 中如何改造

可以把 PS 思路变成结构化计划：

```json
{
  "goal": "完成任务",
  "steps": [
    {"id": 1, "task": "收集事实", "tool": "search", "status": "pending"},
    {"id": 2, "task": "验证事实", "tool": "browser", "status": "pending"},
    {"id": 3, "task": "输出结论", "tool": null, "status": "pending"}
  ]
}
```

执行器逐步验证 schema、工具权限和结果，再决定继续、修改计划还是终止。这样「计划」才真正成为可观测的工程对象，而不是一段无法检查的长文本。

## 面试中如何回答 trade-off

显式计划会增加 token 和延迟，也可能让模型过早锁定错误路径。对简单问题直接回答更便宜；对复杂任务使用短计划、分阶段验证和动态重规划更稳。最终要用任务成功率、漏步率、平均轨迹长度和成本做 A/B，而不是凭感觉判断 prompt 好坏。
