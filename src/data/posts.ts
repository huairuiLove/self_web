import type { Post } from '../types/content'
import { marked } from 'marked'
import interviewRoadmap from '../../content/posts/ai-agent-interview/01-ai-agent-interview-roadmap.md?raw'
import reactNotes from '../../content/posts/ai-agent-interview/02-react-reasoning-and-acting.md?raw'
import planAndSolveNotes from '../../content/posts/ai-agent-interview/03-plan-and-solve-prompting.md?raw'
import interviewExperience from '../../content/posts/ai-agent-interview/04-ai-agent-interview-experience.md?raw'

export const posts: Post[] = [
  {
    id: '1',
    slug: 'vite-vue-personal-site',
    title: '用 Vite + Vue 3 搭个人站：从 0 到可部署',
    excerpt:
      '选型、目录结构、路由与内容组织的一页纸清单，适合作为个人主页的起点模板。',
    content: `
<h2>为什么选 Vite + Vue</h2>
<p>构建快、生态成熟，Composition API 让页面逻辑更易拆分。个人站以展示为主，静态构建 + 任意静态托管即可。</p>
<h2>推荐目录</h2>
<ul>
<li><code>src/data/</code> — 项目与文章数据（后期可换 Markdown）</li>
<li><code>src/views/</code> — 路由页面</li>
<li><code>src/components/</code> — 按功能分子目录</li>
</ul>
<h2>部署</h2>
<p>执行 <code>npm run build</code>，将 <code>dist</code> 上传到 GitHub Pages、Cloudflare Pages 或对象存储即可。</p>
`,
    tags: ['Vue', 'Vite', '前端'],
    publishedAt: '2026-07-10',
    readMinutes: 6,
  },
  {
    id: '2',
    slug: 'write-good-tech-notes',
    title: '技术经验贴怎么写才真的有用',
    excerpt:
      '背景、问题、方案、结果、可复用结论——五段式结构，让读者和你未来的自己都能快速检索。',
    content: `
<h2>先写「问题」再写「方案」</h2>
<p>读者最关心的是：在什么约束下、遇到了什么现象、你如何验证根因。避免一上来堆代码。</p>
<h2>留下可检索的关键词</h2>
<p>标题和摘要里带上框架名、错误信息、版本号，方便搜索与书签。</p>
<h2>结论要可行动</h2>
<p>最后一节用 bullet 列出「下次直接这样做」，比长篇感想更有价值。</p>
`,
    tags: ['写作', '方法论'],
    publishedAt: '2026-06-28',
    readMinutes: 4,
  },
  {
    id: '3',
    slug: 'local-dev-env-checklist',
    title: '本地开发环境自检清单',
    excerpt: '换机器或帮同事排错时，按顺序检查 Node、包管理器、代理与常见端口冲突。',
    content: `
<h2>版本</h2>
<p>锁定 Node LTS，项目根目录提供 <code>.nvmrc</code> 或文档说明。</p>
<h2>依赖</h2>
<p>优先使用 lockfile；CI 与本地用同一包管理器。</p>
<h2>网络</h2>
<p>公司代理、镜像源、<code>SSL</code> 证书问题单独记一篇，能省大量重复沟通。</p>
`,
    tags: ['环境', 'DevOps'],
    publishedAt: '2026-05-15',
    readMinutes: 5,
  },
  {
    id: '4',
    slug: 'ai-agent-interview-roadmap',
    title: 'AI Agent 面试准备：从概念、架构到工程落地',
    excerpt: '把 Agent 岗位面试拆成规划、工具、记忆、评估和安全五条主线，形成一套可复用的学习与回答框架。',
    content: marked.parse(interviewRoadmap, { async: false }),
    tags: ['AI Agent', '面试', '学习路线'],
    publishedAt: '2026-07-17',
    readMinutes: 12,
  },
  {
    id: '5',
    slug: 'react-reasoning-and-acting',
    title: 'ReAct：为什么 Agent 要把推理和行动交替起来',
    excerpt: '从 ReAct 论文理解 Thought、Action、Observation 闭环，并整理成生产 Agent 的工具安全清单。',
    content: marked.parse(reactNotes, { async: false }),
    tags: ['ReAct', 'Agent', '论文笔记'],
    publishedAt: '2026-07-17',
    readMinutes: 9,
  },
  {
    id: '6',
    slug: 'plan-and-solve-prompting',
    title: 'Plan-and-Solve：先做计划，能减少零样本推理的漏步吗',
    excerpt: '从 PS/PS+ 看显式计划、变量提取和中间结果校验，思考它们如何进入真实 Agent 工作流。',
    content: marked.parse(planAndSolveNotes, { async: false }),
    tags: ['Prompting', '推理', '论文笔记'],
    publishedAt: '2026-07-17',
    readMinutes: 8,
  },
  {
    id: '7',
    slug: 'ai-agent-interview-experience',
    title: '人力资源面试经验：把校园经历讲成真实的工作能力',
    excerpt: '我把人力资源规划、招聘模拟、社团管理和项目经历重新梳理了一遍，聊聊怎样在面试中真实、清楚地介绍自己的能力。',
    content: marked.parse(interviewExperience, { async: false }),
    tags: ['人力资源', '面试经验', '校园实践'],
    publishedAt: '2026-07-18',
    readMinutes: 10,
  },
]

export function getPostBySlug(slug: string): Post | undefined {
  return posts.find((p) => p.slug === slug)
}
