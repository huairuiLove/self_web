# 个人主页

基于 **Vue 3 + TypeScript + Vite** 的静态个人站，用于展示个人项目与技术经验贴。

本地开发默认访问：<http://localhost:5173>

## 前置条件

- Node.js 18+（推荐 LTS）
- npm

## 快速启动

```bash
npm install
npm run dev
```

浏览器打开终端里显示的本地地址（一般为 `http://localhost:5173`）。

## 关闭开发服务

在运行 `npm run dev` 的终端按 `Ctrl+C`。

## 构建与预览

```bash
npm run build
npm run preview
```

`preview` 用于本地查看生产构建结果。

## 常用命令

| 命令 | 说明 |
| ---- | ---- |
| `npm run dev` | 启动开发服务器 |
| `npm run build` | 类型检查并构建到 `dist/` |
| `npm run preview` | 预览生产构建 |

## 内容维护

| 文件 | 作用 |
| ---- | ---- |
| `src/data/profile.ts` | 姓名、简介、社交链接 |
| `src/data/projects.ts` | 项目列表与详情 |
| `src/data/posts.ts` | 经验贴标题、摘要与正文（HTML） |

修改上述文件后保存即可热更新，无需改路由。

### Agent 面试资料

本项目把原始资料和已发布内容分开管理：

| 目录 | 作用 |
| ---- | ---- |
| `content/raw/ai-agent-interview/` | 面试指南原稿与 39 篇 arXiv PDF 原始资料 |
| `content/posts/ai-agent-interview/` | 已整理成网站经验贴的 Markdown |
| `src/data/papers.ts` | 论文库索引、分类、摘要与原文链接 |

网站新增 `/papers` 论文库，论文详情页提供原文 PDF 阅读入口；由于 PDF 原始资料约 272MB，不会复制进前端 bundle，生产环境通过 arXiv 在线阅读。指南中的 Devin 是产品文章，因此保留为外部链接，不伪造本地论文文件。

## 部署

执行 `npm run build` 后，将 `dist` 目录上传到 GitHub Pages、Cloudflare Pages 或任意静态托管即可。若站点不在域名根路径，请在 `vite.config.ts` 中设置 `base`。

### 上线基线

- **托管**：优先选择 Cloudflare Pages、Vercel 或对象存储 + CDN。开启 HTTPS、自动部署和构建产物缓存。
- **SPA 回退**：将所有未知路径回退到 `index.html`，否则刷新 `/projects/portfolio` 等深链会返回 404。
- **响应头**：`public/_headers` 提供静态托管可用的 CSP、HSTS、`X-Content-Type-Options`、`Referrer-Policy` 和 `Permissions-Policy`。接入其他平台时，将其迁移到平台的 Header 配置。
- **域名**：正式域名启用 HSTS 前，先确认所有子域名都支持 HTTPS；替换 `robots.txt` 中的站点地图地址（如果后续生成 sitemap）。
- **内容安全**：当前文章是仓库内可信数据，渲染前仍通过 DOMPurify 清洗。若改成 CMS/API，必须继续保留清洗，并在服务端做鉴权、限流、输入校验和审计日志。
- **供应链**：提交 `package-lock.json`，CI 使用 `npm ci` 和 `npm audit`；依赖升级走 Dependabot/Renovate，避免直接在生产环境执行 `npm install`。
- **发布检查**：CI 至少执行 `npm run build`、类型检查、依赖审计和 Lighthouse/可访问性检查；部署后监控 4xx/5xx、JS 错误、Core Web Vitals 与证书到期时间。

这个项目是纯静态前端，**不应把密钥、数据库凭据或第三方私钥放进 `VITE_*` 环境变量**。任何进入前端 bundle 的变量都可被访问者读取；需要机密操作时，应拆出服务端 API 或边缘函数，并在服务端完成鉴权与速率限制。

## 常见问题

**端口 5173 已被占用**

```bash
lsof -i :5173
```

结束占用进程后重新 `npm run dev`，或使用 Vite 指定端口：`npm run dev -- --port 5174`。
