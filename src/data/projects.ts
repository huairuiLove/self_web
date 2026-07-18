import type { Project } from '../types/content'

export const projects: Project[] = [
  {
    id: 'portfolio',
    title: '个人主页',
    summary: '用 Vue 3 搭建的静态个人站，集中展示项目与经验贴。',
    description:
      '基于 Vite + Vue Router 的单页应用，组件化布局，深色主题与响应式排版。后续可接入 CMS 或 Markdown 构建流程。',
    tags: ['Vue 3', 'TypeScript', 'Vite'],
    repo: 'https://github.com/huairuiLove',
    year: '2026',
    featured: true,
    gradient: 'linear-gradient(135deg, #2d4a3e 0%, #1a2332 50%, #3d2f4a 100%)',
  },
  {
    id: 'toolkit',
    title: '开发工具箱',
    summary: '日常脚本与小工具的集合，解决重复性工作流。',
    description: '包含环境同步、批量处理、日志分析等脚本，按场景分类，附带使用说明。',
    tags: ['Python', 'CLI', '自动化'],
    link: 'https://github.com/fengjin0625',
    year: '2025',
    featured: true,
    gradient: 'linear-gradient(135deg, #3a2f1f 0%, #1f2a3a 100%)',
  },
  {
    id: 'experiment',
    title: '创赛设计-“纫兰逢锦”AI试衣',
    summary: '快速验证想法的原型仓库，从 UI 到接口联调。',
    description: '用于尝试新框架、新 API 或交互方案，生命周期短但沉淀可复用的模式与踩坑记录。',
    tags: ['原型', '全栈'],
    repo: 'https://github.com/huairuiLove',
    year: '2025',
    featured: false,
    gradient: 'linear-gradient(135deg, #1f3a2f 0%, #2a1f3a 100%)',
  },
]

export function getProjectById(id: string): Project | undefined {
  return projects.find((p) => p.id === id)
}
