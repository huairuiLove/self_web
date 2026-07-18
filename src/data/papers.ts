export type PaperCategory =
  | '综述与入门'
  | '架构与推理'
  | '工具使用'
  | '记忆与 RAG'
  | '多 Agent'
  | '代码生成'
  | 'GUI Agent'
  | '评估与安全'
  | '前沿实践'

export interface AgentPaper {
  id: string
  slug: string
  title: string
  authors?: string
  year: string
  category: PaperCategory
  contribution: string
  arxivId?: string
  externalUrl?: string
}

const arxiv = (id: string) => `https://arxiv.org/abs/${id}`

export const papers: AgentPaper[] = [
  { id: '1', slug: 'autonomous-agents-survey', title: 'A Survey on Large Language Model based Autonomous Agents', authors: 'Wang et al.', year: '2023', category: '综述与入门', contribution: '系统梳理 Agent 的架构、能力、应用与评估。', arxivId: '2308.11432' },
  { id: '2', slug: 'rise-of-llm-agents', title: 'The Rise and Potential of Large Language Model Based Agents: A Survey', authors: 'Xi et al.', year: '2023', category: '综述与入门', contribution: '从社会与系统视角讨论 LLM Agent 的发展潜力。', arxivId: '2309.07864' },
  { id: '3', slug: 'agent-ai-multimodal-interaction', title: 'Agent AI: Surveying the Horizons of Multimodal Interaction', year: '2024', category: '综述与入门', contribution: '总结多模态 Agent 的感知、推理和行动能力。', arxivId: '2401.03568' },
  { id: '4', slug: 'react', title: 'ReAct: Synergizing Reasoning and Acting in Language Models', authors: 'Yao et al.', year: '2022', category: '架构与推理', contribution: '提出交替推理与行动的 Agent 基础范式。', arxivId: '2210.03629' },
  { id: '5', slug: 'chain-of-thought', title: 'Chain-of-Thought Prompting Elicits Reasoning in Large Language Models', authors: 'Wei et al.', year: '2022', category: '架构与推理', contribution: '展示示例推理链如何激发大模型多步推理。', arxivId: '2201.11903' },
  { id: '6', slug: 'tree-of-thoughts', title: 'Tree of Thoughts: Deliberate Problem Solving with Large Language Models', authors: 'Yao et al.', year: '2023', category: '架构与推理', contribution: '用树状搜索探索多条推理路径并选择更优解。', arxivId: '2305.10601' },
  { id: '7', slug: 'graph-of-thoughts', title: 'Graph of Thoughts: Solving Elaborate Problems with Large Language Models', authors: 'Besta et al.', year: '2023', category: '架构与推理', contribution: '将推理表示为可合并、分叉与回溯的有向图。', arxivId: '2308.09687' },
  { id: '8', slug: 'plan-and-solve', title: 'Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning', authors: 'Wang et al.', year: '2023', category: '架构与推理', contribution: '先制定计划再逐步求解，减少漏步与计算错误。', arxivId: '2305.04091' },
  { id: '9', slug: 'reflexion', title: 'Reflexion: Language Agents with Verbal Reinforcement Learning', authors: 'Shinn et al.', year: '2023', category: '架构与推理', contribution: '通过语言化反思把失败经验反馈给后续尝试。', arxivId: '2303.11366' },
  { id: '10', slug: 'self-refine', title: 'Self-Refine: Iterative Refinement with Self-Feedback', authors: 'Madaan et al.', year: '2023', category: '架构与推理', contribution: '让模型通过自我反馈迭代改进初始输出。', arxivId: '2303.17651' },
  { id: '11', slug: 'toolformer', title: 'Toolformer: Language Models Can Teach Themselves to Use Tools', authors: 'Schick et al.', year: '2023', category: '工具使用', contribution: '探索让语言模型自主学习何时、如何调用工具。', arxivId: '2302.04761' },
  { id: '12', slug: 'gorilla', title: 'Gorilla: Large Language Model Connected with Massive APIs', year: '2023', category: '工具使用', contribution: '面向大规模 API 调用，降低工具选择与参数幻觉。', arxivId: '2305.15334' },
  { id: '13', slug: 'toollm', title: 'ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs', authors: 'Qin et al.', year: '2023', category: '工具使用', contribution: '用大规模真实 API 数据训练工具调用能力。', arxivId: '2307.16789' },
  { id: '14', slug: 'mm-react', title: 'MM-REACT: Prompting ChatGPT for Multimodal Reasoning and Action', authors: 'Yang et al.', year: '2023', category: '工具使用', contribution: '将视觉输入和外部工具整合进多模态推理。', arxivId: '2303.11381' },
  { id: '15', slug: 'api-bank', title: 'API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs', year: '2023', category: '工具使用', contribution: '提供工具增强 LLM 的训练与评估基准。', arxivId: '2304.08244' },
  { id: '16', slug: 'rag', title: 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks', authors: 'Lewis et al.', year: '2020', category: '记忆与 RAG', contribution: '奠定检索增强生成的经典架构。', arxivId: '2005.11401' },
  { id: '17', slug: 'memgpt', title: 'MemGPT: Towards LLMs as Operating Systems', authors: 'Packer et al.', year: '2023', category: '记忆与 RAG', contribution: '用主存与外存分层管理超出上下文窗口的记忆。', arxivId: '2310.08560' },
  { id: '18', slug: 'generative-agents', title: 'Generative Agents: Interactive Simulacra of Human Behavior', authors: 'Park et al.', year: '2023', category: '记忆与 RAG', contribution: '结合记忆流、反思和规划模拟长期行为。', arxivId: '2304.03442' },
  { id: '19', slug: 'autogen', title: 'AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation', authors: 'Wu et al.', year: '2023', category: '多 Agent', contribution: '用可对话 Agent 组织复杂任务协作。', arxivId: '2308.08155' },
  { id: '20', slug: 'metagpt', title: 'MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework', authors: 'Hong et al.', year: '2023', category: '多 Agent', contribution: '模拟软件公司的角色分工与协作流程。', arxivId: '2308.00352' },
  { id: '21', slug: 'chatdev', title: 'ChatDev: Communicative Agents for Software Development', authors: 'Qian et al.', year: '2023', category: '多 Agent', contribution: '用多角色对话完成软件开发流水线。', arxivId: '2307.07924' },
  { id: '22', slug: 'camel', title: 'CAMEL: Communicative Agents for Mind Exploration', authors: 'Li et al.', year: '2023', category: '多 Agent', contribution: '通过角色扮演和任务指令促进 Agent 协作。', arxivId: '2303.17760' },
  { id: '23', slug: 'multiagent-debate', title: 'Improving Factuality and Reasoning in Language Models through Multiagent Debate', authors: 'Du et al.', year: '2023', category: '多 Agent', contribution: '用多 Agent 辩论提升事实性与推理质量。', arxivId: '2305.14325' },
  { id: '24', slug: 'swe-agent', title: 'SWE-Agent: Agent-Computer Interfaces Enable Automated Software Engineering', authors: 'Yang et al.', year: '2024', category: '代码生成', contribution: '研究面向软件工程 Agent 的计算机接口设计。', arxivId: '2405.15793' },
  { id: '25', slug: 'swe-bench', title: 'SWE-bench: Can Language Models Resolve Real-World GitHub Issues?', authors: 'Jimenez et al.', year: '2023', category: '代码生成', contribution: '用真实 GitHub Issue 评估代码修复 Agent。', arxivId: '2310.06770' },
  { id: '26', slug: 'opendevin', title: 'OpenDevin: An Open Platform for AI Software Developers as Generalist Agents', year: '2024', category: '代码生成', contribution: '提供开放的通用软件工程 Agent 平台。', arxivId: '2407.16741' },
  { id: '27', slug: 'devin', title: 'Devin: The AI Software Engineer', year: '2024', category: '代码生成', contribution: '商业软件工程 Agent 的产品化案例。', externalUrl: 'https://www.cognition.ai/blog/introducing-devin' },
  { id: '28', slug: 'os-copilot', title: 'OS-Copilot: Towards Generalist Computer Agents with Self-Improvement', authors: 'Wu et al.', year: '2024', category: 'GUI Agent', contribution: '探索具备自我改进能力的通用计算机操作 Agent。', arxivId: '2402.07456' },
  { id: '29', slug: 'ufo', title: 'UFO: A UI-Focused Agent for Windows OS Interaction', authors: 'Zhang et al.', year: '2024', category: 'GUI Agent', contribution: '面向 Windows UI 交互的视觉操作 Agent。', arxivId: '2402.07939' },
  { id: '30', slug: 'webarena', title: 'WebArena: A Realistic Web Environment for Building Autonomous Agents', authors: 'Zhou et al.', year: '2023', category: 'GUI Agent', contribution: '提供真实 Web 任务环境评估自主 Agent。', arxivId: '2307.13854' },
  { id: '31', slug: 'gaia', title: 'GAIA: A Benchmark for General AI Assistants', authors: 'Mialon et al.', year: '2023', category: '评估与安全', contribution: '评估通用 AI 助手在真实问题上的综合能力。', arxivId: '2311.12983' },
  { id: '32', slug: 'agentbench', title: 'AgentBench: Evaluating LLMs as Agents', authors: 'Liu et al.', year: '2023', category: '评估与安全', contribution: '从多个环境系统评估 LLM Agent 能力。', arxivId: '2308.03688' },
  { id: '33', slug: 'tau-bench', title: 'τ-Bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains', year: '2024', category: '评估与安全', contribution: '评估真实领域中的工具、Agent 与用户交互。', arxivId: '2406.12045' },
  { id: '34', slug: 'agent-security-bench', title: 'The Agent Security Bench (ASB)', year: '2024', category: '评估与安全', contribution: '面向 Agent 攻击面与防护能力的安全基准。', arxivId: '2406.16585' },
  { id: '35', slug: 'mint', title: 'MINT: Evaluating LLMs in Multi-Turn Interaction with Tools', year: '2023', category: '评估与安全', contribution: '评估多轮对话中 Agent 的工具交互能力。', arxivId: '2309.10691' },
  { id: '36', slug: 'voyager', title: 'Voyager: An Open-Ended Embodied Agent with Large Language Models', authors: 'Wang et al.', year: '2023', category: '前沿实践', contribution: '在 Minecraft 中持续学习并构建可复用技能库。', arxivId: '2305.16291' },
  { id: '37', slug: 'deps', title: 'Describe, Explain, Plan and Select (DEPS)', authors: 'Wang et al.', year: '2023', category: '前沿实践', contribution: '面向开放世界游戏的分解式规划 Agent。', arxivId: '2302.01560' },
  { id: '38', slug: 'hugginggpt', title: 'HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face', authors: 'Shen et al.', year: '2023', category: '前沿实践', contribution: '让 LLM 编排 Hugging Face 上的多个专用模型。', arxivId: '2303.17580' },
  { id: '39', slug: 'taskweaver', title: 'TaskWeaver: A Code-First Agent Framework', authors: 'Qiao et al.', year: '2023', category: '前沿实践', contribution: '以代码作为中间表示构建可组合 Agent 工作流。', arxivId: '2311.17541' },
  { id: '40', slug: 'autowebglm', title: 'AutoWebGLM: A Large Language Model-based Web Navigating Agent', year: '2024', category: '前沿实践', contribution: '研究基于 LLM 的 Web 导航与操作 Agent。', arxivId: '2404.03648' },
]

export function getPaperBySlug(slug: string): AgentPaper | undefined {
  return papers.find((paper) => paper.slug === slug)
}

export function getPaperUrl(paper: AgentPaper): string {
  return paper.arxivId ? arxiv(paper.arxivId) : paper.externalUrl ?? '#'
}

export function getPaperPdfUrl(paper: AgentPaper): string | undefined {
  return paper.arxivId ? `https://arxiv.org/pdf/${paper.arxivId}.pdf` : undefined
}
