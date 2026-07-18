export interface ResearchQuestion {
  index: string
  title: string
  note: string
}

export const activeLearningFocus = {
  title: '主动学习 × 医学人工智能',
  summary: '我现在关注的核心问题，是怎样让模型在标注昂贵、专家时间有限的条件下，主动提出最值得被回答的问题。医学场景把这个问题推到了最实际的位置：一次标注可能不是一个类别，而是一位医生对整套影像、病灶轮廓或临床文本的判断。',
  definition: '从少量已标注数据出发，模型在未标注池中选择下一批样本，请专家给出答案，再带着新增标注重新训练。目标是在固定成本下获得更好的模型，或以更少成本达到同等性能。',
  loop: ['训练当前模型', '计算查询价值', '专家完成标注', '更新并重新评估'],
} as const

export const researchQuestions: ResearchQuestion[] = [
  {
    index: '01',
    title: '查询什么',
    note: '不确定性只是起点。我需要同时考虑代表性、批内多样性、稀有病灶覆盖，以及图像、切片、区域或像素等不同查询粒度。',
  },
  {
    index: '02',
    title: '成本怎么算',
    note: '样本数不是医学标注成本。更可信的预算应包含医生耗时、病例复杂度、复核次数、标注者差异和工具交互成本。',
  },
  {
    index: '03',
    title: '什么时候可信',
    note: '离线数据池上的提升不等于临床可用。我会重点检查患者级划分、模型校准、域偏移、错标鲁棒性、停止条件和真实工作流验证。',
  },
]
