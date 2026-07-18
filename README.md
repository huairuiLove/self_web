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
| `content/raw/active-learning/` | 主动学习阅读顺序与 22 篇本地 PDF |
| `content/posts/ai-agent-interview/` | 已整理成网站经验贴的 Markdown |
| `src/data/papers.ts` | 论文库索引、分类、摘要与原文链接 |

### PyTorch 方法字典

`function_search/` 是桌面版 API 查询工具，网站通过 `/function-search` 提供同一份站内查询入口。目前导出了 6,164 个 PyTorch API，以及 Python 常用、后端和扩展条目，共 6,235 条；索引文件位于 `public/function-search.json`，按页面访问时才加载，不影响首页首屏。更新桌面版索引后，可以重新导出：

```bash
cd function_search
PYTHONPATH=src ./.venv/bin/python -m function_search.build_index \
  --output /tmp/function-search.db \
  --export-json ../public/function-search.json
```

网站新增 `/papers` 论文库，论文详情页内置 PDF 阅读、缩放和划词翻译。Agent 与主动学习两组共 61 篇 PDF 保存在原始资料目录，Vite 构建时自动复制到 `dist/papers/` 并通过同源 `/papers/{文件名}` 提供，不会再触发浏览器跨域请求；没有本地 PDF 的产品文章或出版物仍保留外部入口。

### PDF 选区翻译

论文库的 PDF 详情页内置阅读翻译模块。先在 LM Studio 中加载模型并启动 Local Server（默认 `http://localhost:1234`），再填写模型名称并测试接口。当前默认模型为 `qwen/qwen3-4b-2507`，请求关闭 thinking，适合短词即时查译；开发环境对默认本地地址使用 Vite 同源代理，避免 LM Studio 不处理 `OPTIONS` 预检导致请求失败；生产环境直连本地 LM Studio 时，需要在 Local Server 设置中开启 CORS，或部署自己的服务端代理。阅读器使用 PDF.js 官方 Viewer 渲染连续页面、缩放和文字层，保持 PDF 原生排版清晰度；在论文详情页像 Edge/Safari 一样拖选文字，松开鼠标后会自动调用本地模型并显示中文译文，无需画框或手动触发 OCR。PDF 只在浏览器内处理；接口配置保存在当前浏览器的 localStorage。

论文详情页的“智能划词阅读”直接加载同源本地 PDF；如果部署时没有上传 `dist/papers/`，页面会提示通过“打开 PDF”载入本地文件。自动翻译依赖 PDF 自带的文字层，扫描版 PDF 没有可选择文本时需要先执行 OCR。若浏览器无法连接 LM Studio，检查 Local Server 是否启动、端口是否正确，以及 LM Studio 的 CORS 是否允许当前网站地址。

成功译文会写入浏览器本地查词历史，按模型和翻译模式去重，最多保留 60 条；重复选择相同内容会直接命中缓存。历史记录不会被拼接进模型消息。每次 LM Studio 请求都是独立的 `system + 当前选中文字`，因此上下文不会随阅读时间持续增长，也不依赖模型自动压缩上下文。

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
