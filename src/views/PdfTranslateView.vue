<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, reactive, shallowRef, useTemplateRef } from 'vue'
import * as pdfjsLib from 'pdfjs-dist'
import pdfWorkerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url'
import 'pdfjs-dist/web/pdf_viewer.css'
import { EventBus, PDFLinkService, PDFViewer } from 'pdfjs-dist/web/pdf_viewer.mjs'
import { useLmStudio } from '../composables/useLmStudio'
import { useTranslationHistory, type TranslationHistoryEntry } from '../composables/useTranslationHistory'
import { getPaperPdfUrl, type ResearchPaper } from '../data/papers'

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorkerUrl

const props = defineProps<{
  embedded?: boolean
  paper?: ResearchPaper
}>()

const fileInput = useTemplateRef<HTMLInputElement>('fileInput')
const pdfContainer = useTemplateRef<HTMLDivElement>('pdfContainer')
const pdfViewerElement = useTemplateRef<HTMLDivElement>('pdfViewerElement')
const pdfDocument = shallowRef<pdfjsLib.PDFDocumentProxy | null>(null)
let eventBus: EventBus | null = null
let linkService: PDFLinkService | null = null
let pdfViewer: PDFViewer | null = null
let pagesInitHandler: (() => void) | null = null
let pageChangingHandler: ((event: { pageNumber: number }) => void) | null = null
const fileName = shallowRef('')
const pageNumber = shallowRef(1)
const pageCount = shallowRef(0)
const isLoading = shallowRef(false)
const isTranslating = shallowRef(false)
const sidebarOpen = shallowRef(false)
const sidebarTab = shallowRef<'translation' | 'history'>('translation')
const selectedText = shallowRef('')
const translatedText = shallowRef('')
const selectionMode = shallowRef<'term' | 'academic'>('term')
const popover = reactive({ visible: false, x: 0, y: 0 })
const toolError = shallowRef('')
const activeRequest = shallowRef(0)
const { config, status, error: lmError, testConnection, translate } = useLmStudio()
const { history, findTranslation, addTranslation, removeTranslation, clearHistory } = useTranslationHistory()

function openFilePicker() {
  fileInput.value?.click()
}

async function handleFile(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  toolError.value = ''
  isLoading.value = true
  try {
    const data = await file.arrayBuffer()
    await loadPdfData(data, file.name)
  } catch (cause) {
    toolError.value = cause instanceof Error ? cause.message : '无法打开 PDF 文件'
  } finally {
    isLoading.value = false
    input.value = ''
  }
}

async function loadPdfData(data: ArrayBuffer, name: string) {
  pdfViewer?.setDocument(null as unknown as pdfjsLib.PDFDocumentProxy)
  linkService?.setDocument(null)
  const previousDocument = pdfDocument.value
  pdfDocument.value = null
  if (previousDocument) {
    const destroyDocument = (previousDocument as unknown as { destroy?: () => Promise<void> }).destroy
    if (destroyDocument) void destroyDocument.call(previousDocument)
  }
  const loadingTask = pdfjsLib.getDocument({ data })
  pdfDocument.value = await loadingTask.promise
  fileName.value = name
  pageCount.value = pdfDocument.value.numPages
  pageNumber.value = 1
  clearTranslation()
  await nextTick()
  if (!pdfViewer) setupPdfViewer()
  pdfViewer?.setDocument(pdfDocument.value)
  linkService?.setDocument(pdfDocument.value)
}

async function loadPaperFromLibrary() {
  const paper = props.paper
  const pdfUrl = paper ? getPaperPdfUrl(paper) : undefined
  if (!paper || !pdfUrl) return
  isLoading.value = true
  toolError.value = ''
  try {
    const response = await fetch(pdfUrl)
    if (!response.ok) throw new Error(`论文 PDF 下载失败（${response.status}）`)
    await loadPdfData(await response.arrayBuffer(), `${paper.title}.pdf`)
  } catch (cause) {
    toolError.value = cause instanceof TypeError && cause.message === 'Failed to fetch'
      ? '无法读取本地论文 PDF，请确认构建产物包含 dist/papers；也可以用“打开 PDF”临时载入。'
      : cause instanceof Error ? cause.message : '无法加载论文 PDF，请改用本地上传。'
  } finally {
    isLoading.value = false
  }
}

function setupPdfViewer() {
  if (!pdfContainer.value || !pdfViewerElement.value) return
  eventBus = new EventBus()
  linkService = new PDFLinkService({ eventBus })
  pdfViewer = new PDFViewer({
    container: pdfContainer.value,
    viewer: pdfViewerElement.value,
    eventBus,
    linkService,
    textLayerMode: 1,
    removePageBorders: false,
    enableDetailCanvas: true,
    enableSelectionRendering: true,
    maxCanvasPixels: 16_777_216,
  })
  linkService.setViewer(pdfViewer)
  pagesInitHandler = () => {
    if (!pdfViewer) return
    pdfViewer.currentScaleValue = 'page-width'
    pageNumber.value = pdfViewer.currentPageNumber
    isLoading.value = false
  }
  pageChangingHandler = ({ pageNumber: currentPage }) => {
    pageNumber.value = currentPage
  }
  eventBus.on('pagesinit', pagesInitHandler)
  eventBus.on('pagechanging', pageChangingHandler)
}

function destroyPdfViewer() {
  if (eventBus && pagesInitHandler) eventBus.off('pagesinit', pagesInitHandler)
  if (eventBus && pageChangingHandler) eventBus.off('pagechanging', pageChangingHandler)
  pdfViewer?.setDocument(null as unknown as pdfjsLib.PDFDocumentProxy)
  linkService?.setDocument(null)
  const destroyDocument = (pdfDocument.value as unknown as { destroy?: () => Promise<void> } | null)?.destroy
  if (destroyDocument) void destroyDocument.call(pdfDocument.value)
  eventBus = null
  linkService = null
  pdfViewer = null
  pagesInitHandler = null
  pageChangingHandler = null
}

function changePage(step: number) {
  const nextPage = pageNumber.value + step
  if (!pdfDocument.value || nextPage < 1 || nextPage > pageCount.value) return
  pageNumber.value = nextPage
  clearTranslation()
  if (pdfViewer) pdfViewer.currentPageNumber = nextPage
}

function zoom(step: number) {
  if (!pdfViewer) return
  pdfViewer.currentScale = Math.max(0.5, Math.min(3, pdfViewer.currentScale + step))
}

function normalizeSelectedText(text: string) {
  return text
    .replace(/-\s*\n\s*(?=[a-z])/g, '')
    .replace(/\s*\n\s*/g, ' ')
    .replace(/[ \t]+/g, ' ')
    .trim()
}

function isTermSelection(text: string) {
  const wordCount = text.split(/\s+/).filter(Boolean).length
  return text.length <= 160 && wordCount <= 12
}

function positionPopover(rect: DOMRect) {
  const popoverWidth = 320
  const estimatedHeight = 150
  popover.x = Math.min(Math.max(12, rect.left), window.innerWidth - popoverWidth - 12)
  popover.y = rect.bottom + 10
  if (popover.y + estimatedHeight > window.innerHeight) {
    popover.y = Math.max(12, rect.top - estimatedHeight - 10)
  }
}

async function handleTextSelection() {
  const selection = window.getSelection()
  if (!selection || selection.isCollapsed || !pdfViewerElement.value) return
  const range = selection.rangeCount ? selection.getRangeAt(0) : null
  if (!range || !pdfViewerElement.value.contains(range.commonAncestorContainer)) return
  const selectionAnchor = selection.anchorNode?.parentElement?.closest('.textLayer')
  if (!selectionAnchor) return

  const text = normalizeSelectedText(selection.toString())
  if (text.length < 2 || text === selectedText.value) return
  if (text.length > 12_000) {
    toolError.value = '选中文字过长，请缩小到 12,000 字符以内。'
    return
  }

  const termMode = isTermSelection(text)
  selectionMode.value = termMode ? 'term' : 'academic'
  selectedText.value = text
  translatedText.value = ''
  if (termMode) {
    positionPopover(range.getBoundingClientRect())
    popover.visible = true
  } else {
    popover.visible = false
    sidebarOpen.value = true
  }
  await translateSelectedText()
}

async function translateSelectedText() {
  if (!selectedText.value) return
  const mode = selectionMode.value
  const sourceText = selectedText.value
  const requestId = activeRequest.value + 1
  activeRequest.value = requestId
  isTranslating.value = true
  toolError.value = ''
  try {
    if (status.value !== 'ready') {
      const connected = await testConnection()
      if (!connected) throw new Error(lmError.value || '无法连接 LM Studio')
    }
    const model = config.model.trim()
    const cached = findTranslation(sourceText, mode, model)
    if (cached) {
      translatedText.value = cached.translation
      return
    }
    const result = await translate(sourceText, { mode })
    if (requestId === activeRequest.value) {
      translatedText.value = result
      addTranslation({ source: sourceText, translation: result, mode, model })
    }
  } catch (cause) {
    if (requestId === activeRequest.value) {
      toolError.value = cause instanceof Error ? cause.message : '翻译失败'
    }
  } finally {
    if (requestId === activeRequest.value) isTranslating.value = false
  }
}

function clearTranslation() {
  activeRequest.value += 1
  selectedText.value = ''
  translatedText.value = ''
  popover.visible = false
  isTranslating.value = false
  toolError.value = ''
  window.getSelection()?.removeAllRanges()
}

function openResultInSidebar() {
  sidebarOpen.value = true
  sidebarTab.value = 'translation'
  popover.visible = false
}

function selectHistoryEntry(entry: TranslationHistoryEntry) {
  selectedText.value = entry.source
  translatedText.value = entry.translation
  selectionMode.value = entry.mode
  sidebarTab.value = 'translation'
  sidebarOpen.value = true
  popover.visible = false
  toolError.value = ''
}

function formatHistoryTime(iso: string) {
  return new Intl.DateTimeFormat('zh-CN', {
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(iso))
}

async function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
  await nextTick()
  if (pdfViewer) pdfViewer.currentScaleValue = 'page-width'
}

onBeforeUnmount(() => {
  destroyPdfViewer()
})

onMounted(() => {
  setupPdfViewer()
  void loadPaperFromLibrary()
})
</script>

<template>
  <div class="translator-page" :class="{ 'translator-page--embedded': embedded }">
    <header v-if="!embedded" class="page-header">
      <div>
        <p class="page-kicker">LOCAL AI READER / 04</p>
        <h1 class="page-title">PDF 阅读翻译</h1>
        <p class="page-lead">选中单词或短语后就地显示中文释义；长段落自动进入右侧翻译栏。PDF 文件只在当前浏览器中打开。</p>
      </div>
      <button type="button" class="sidebar-toggle" :aria-pressed="sidebarOpen" @click="toggleSidebar">
        {{ sidebarOpen ? '关闭翻译栏' : '打开翻译栏' }}
      </button>
    </header>

    <details class="config-panel">
      <summary>
        <span><strong>LM Studio</strong> · {{ config.model }}</span>
        <span class="status" :class="`status--${status}`">{{ status === 'ready' ? '已连接' : status === 'checking' ? '连接中' : status === 'error' ? '连接失败' : '接口设置' }}</span>
      </summary>
      <div class="config-grid">
        <label class="field"><span>接口地址</span><input v-model="config.baseUrl" type="url" placeholder="http://localhost:1234" /></label>
        <label class="field"><span>模型名称</span><input v-model="config.model" type="text" placeholder="qwen/qwen3-4b-2507" /></label>
        <label class="field"><span>API Key（可选）</span><input v-model="config.apiKey" type="password" placeholder="LM Studio 默认可留空" /></label>
        <button type="button" class="outline-button" :disabled="status === 'checking'" @click="testConnection">测试接口</button>
      </div>
      <p class="panel-hint">启动 LM Studio Local Server 并开启 CORS。Qwen3 已关闭思考模式，短词优先走快速查译，长段落保留学术翻译提示。</p>
      <p v-if="lmError" class="error-message">{{ lmError }}</p>
    </details>

    <div class="reader-layout" :class="{ 'reader-layout--sidebar': sidebarOpen }">
      <main class="document-panel">
        <div class="reader-toolbar">
          <input ref="fileInput" type="file" accept="application/pdf" hidden @change="handleFile" />
          <button type="button" class="primary-button file-button" @click="openFilePicker">{{ fileName || '打开 PDF' }}</button>
          <button v-if="embedded" type="button" class="sidebar-toggle sidebar-toggle--compact" :aria-pressed="sidebarOpen" @click="toggleSidebar">
            {{ sidebarOpen ? '关闭翻译栏' : '打开翻译栏' }}
          </button>
          <template v-if="pdfDocument">
            <button type="button" class="square-button" :disabled="pageNumber <= 1" aria-label="上一页" @click="changePage(-1)">←</button>
            <span class="page-count">{{ pageNumber }} / {{ pageCount }}</span>
            <button type="button" class="square-button" :disabled="pageNumber >= pageCount" aria-label="下一页" @click="changePage(1)">→</button>
            <span class="toolbar-divider" aria-hidden="true"></span>
            <button type="button" class="square-button" aria-label="缩小" @click="zoom(-0.1)">−</button>
            <button type="button" class="square-button" aria-label="放大" @click="zoom(0.1)">＋</button>
          </template>
          <span v-if="isLoading" class="loading-label">正在渲染...</span>
        </div>

        <div ref="pdfContainer" class="pdf-viewport" v-show="pdfDocument" @mouseup="handleTextSelection" @keyup="handleTextSelection">
          <div ref="pdfViewerElement" class="pdfViewer" />
        </div>
        <div v-if="!pdfDocument" class="empty-document">
          <span class="empty-mark" aria-hidden="true">PDF</span>
          <strong>打开论文开始阅读</strong>
          <span>选中文字后会自动翻译，无需画框或点击识别</span>
          <p v-if="toolError" class="reader-error">{{ toolError }}</p>
        </div>
      </main>

      <aside v-if="sidebarOpen" class="translation-sidebar" aria-label="PDF 翻译结果">
        <div class="sidebar-heading">
          <div>
            <p class="panel-kicker">LOCAL TRANSLATION</p>
            <h2>{{ sidebarTab === 'translation' ? '中文翻译' : '查词历史' }}</h2>
          </div>
          <div class="sidebar-actions">
            <button v-if="sidebarTab === 'translation' && selectedText" type="button" class="clear-button" @click="clearTranslation">清除</button>
            <button v-else-if="sidebarTab === 'history' && history.length" type="button" class="clear-button" @click="clearHistory">清空</button>
            <button type="button" class="sidebar-close" aria-label="关闭翻译栏" title="关闭翻译栏" @click="sidebarOpen = false">×</button>
          </div>
        </div>

        <div class="sidebar-tabs" role="tablist" aria-label="翻译栏视图">
          <button type="button" role="tab" :aria-selected="sidebarTab === 'translation'" :class="{ active: sidebarTab === 'translation' }" @click="sidebarTab = 'translation'">当前翻译</button>
          <button type="button" role="tab" :aria-selected="sidebarTab === 'history'" :class="{ active: sidebarTab === 'history' }" @click="sidebarTab = 'history'">历史 {{ history.length }}</button>
        </div>

        <template v-if="sidebarTab === 'translation'">
          <div v-if="selectedText" class="translation-content">
            <section class="source-section">
              <span class="section-label">选中原文</span>
              <p>{{ selectedText }}</p>
            </section>
            <section class="target-section">
              <div class="target-heading">
                <span class="section-label">简体中文</span>
                <span v-if="isTranslating" class="translating-state">{{ config.model }} 正在翻译...</span>
              </div>
              <p :class="{ placeholder: !translatedText }">{{ translatedText || (isTranslating ? '正在生成译文' : '选择另一段文字即可重新翻译') }}</p>
            </section>
            <button v-if="toolError" type="button" class="retry-button" @click="translateSelectedText">重新翻译</button>
          </div>
          <div v-else class="sidebar-empty">
            <span class="selection-icon" aria-hidden="true">Aa</span>
            <strong>选择一段 PDF 文字</strong>
            <p>松开鼠标后会自动调用本地模型，译文显示在这里。</p>
          </div>
          <p v-if="toolError" class="error-message sidebar-error">{{ toolError }}</p>
        </template>

        <div v-else class="history-list">
          <article v-for="entry in history" :key="entry.id" class="history-item">
            <button type="button" class="history-main" @click="selectHistoryEntry(entry)">
              <strong>{{ entry.source }}</strong>
              <span>{{ entry.translation }}</span>
              <small>{{ entry.mode === 'term' ? '划词' : '段落' }} · {{ formatHistoryTime(entry.createdAt) }}</small>
            </button>
            <button type="button" class="history-remove" :aria-label="`删除 ${entry.source}`" @click="removeTranslation(entry.id)">×</button>
          </article>
          <div v-if="!history.length" class="history-empty">
            <strong>还没有查词记录</strong>
            <p>成功翻译的内容会保存在当前浏览器，最多保留 60 条。</p>
          </div>
        </div>
      </aside>
    </div>

    <div
      v-if="popover.visible && selectedText"
      class="term-popover"
      :style="{ left: `${popover.x}px`, top: `${popover.y}px` }"
      role="status"
      @mousedown.stop
    >
      <div class="term-popover-heading">
        <strong>{{ selectedText }}</strong>
        <button type="button" aria-label="关闭划词翻译" @click="popover.visible = false">×</button>
      </div>
      <p :class="{ placeholder: !translatedText }">
        {{ translatedText || (isTranslating ? '正在查询本地模型...' : '暂时没有译文') }}
      </p>
      <div class="term-popover-footer">
        <span>{{ config.model }}</span>
        <button type="button" @click="openResultInSidebar">在侧栏查看</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.translator-page { max-width: 1180px; }
.translator-page--embedded { width: calc(100vw - 2rem); max-width: none; margin-left: calc((100% - 100vw + 2rem) / 2); }
.page-header { display: flex; align-items: flex-end; justify-content: space-between; gap: 2rem; margin-bottom: 1.25rem; }
.page-header > div { max-width: 48rem; }
.page-kicker, .panel-kicker { margin: 0 0 0.5rem; color: var(--accent-pink); font-size: 0.68rem; font-weight: 800; letter-spacing: 0.14em; }
.page-title { margin: 0 0 0.55rem; font-family: var(--font-display); font-size: clamp(2rem, 4vw, 2.8rem); }
.page-lead { margin: 0; color: var(--text-secondary); line-height: 1.75; }
.sidebar-toggle, .primary-button, .outline-button, .square-button, .clear-button, .retry-button { min-height: 38px; border-radius: 7px; font: inherit; font-size: 0.78rem; font-weight: 700; cursor: pointer; }
.sidebar-toggle, .outline-button, .square-button, .clear-button { border: 1px solid var(--border-strong); color: var(--text-primary); background: rgba(255,255,255,0.72); }
.sidebar-toggle { flex: 0 0 auto; padding: 0.55rem 0.8rem; }
.sidebar-toggle--compact { margin-left: auto; }
.primary-button { padding: 0.55rem 0.9rem; border: 1px solid var(--accent); color: white; background: var(--accent); box-shadow: 3px 3px 0 var(--accent-pink); }
.outline-button { padding: 0.55rem 0.8rem; }
.square-button { min-width: 38px; padding: 0.45rem; }
.clear-button { min-height: 30px; padding: 0.3rem 0.55rem; color: var(--text-muted); font-weight: 500; }
.retry-button { align-self: flex-start; padding: 0.5rem 0.7rem; border: 1px solid var(--accent); color: var(--accent-strong); background: var(--surface-elevated); }
button:disabled { cursor: not-allowed; opacity: 0.45; }
.config-panel { margin-bottom: 1rem; border: 1px solid var(--border-subtle); border-radius: 9px; background: var(--surface-card); }
.config-panel summary { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.75rem 1rem; cursor: pointer; color: var(--text-secondary); font-size: 0.78rem; }
.config-panel summary::marker { color: var(--accent); }
.config-grid { display: grid; grid-template-columns: 1.2fr 1.2fr 1fr auto; align-items: end; gap: 0.7rem; padding: 0 1rem 0.9rem; }
.field { display: grid; gap: 0.3rem; color: var(--text-muted); font-size: 0.7rem; font-weight: 700; }
.field input { width: 100%; min-height: 38px; padding: 0.5rem 0.65rem; border: 1px solid var(--border-subtle); border-radius: 6px; color: var(--text-primary); background: rgba(255,255,255,0.78); font: inherit; font-size: 0.8rem; }
.panel-hint, .error-message { margin: 0 1rem 0.9rem; color: var(--text-muted); font-size: 0.72rem; }
.error-message { color: #a1384b; }
.status { padding: 0.2rem 0.45rem; border-radius: 999px; color: var(--text-muted); background: var(--surface-elevated); font-size: 0.68rem; }
.status--ready { color: #22794c; background: #e6f6ec; }
.status--error { color: #a1384b; background: #fdecef; }
.reader-layout { display: grid; grid-template-columns: minmax(0, 1fr); gap: 1rem; align-items: start; }
.reader-layout--sidebar { grid-template-columns: minmax(0, 1fr) minmax(310px, 360px); }
.document-panel, .translation-sidebar { border: 1px solid var(--border-subtle); border-radius: 10px; background: var(--surface-card); box-shadow: 0 12px 30px rgba(55,89,144,0.07); }
.reader-toolbar { display: flex; align-items: center; flex-wrap: wrap; gap: 0.5rem; min-height: 58px; padding: 0.65rem 0.8rem; border-bottom: 1px solid var(--border-subtle); }
.file-button { max-width: 260px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.page-count, .loading-label { color: var(--text-muted); font-size: 0.75rem; font-variant-numeric: tabular-nums; }
.loading-label { margin-left: auto; }
.pdf-viewport { overflow: auto; max-height: calc(100vh - 190px); min-height: 560px; padding: 1rem; background: rgba(222,232,247,0.7); }
.pdf-viewport :deep(.pdfViewer) { position: relative; width: 100%; min-height: 100%; }
.pdf-viewport :deep(.pdfViewer .page) { margin: 1rem auto; }
.pdf-viewport :deep(.pdfViewer .textLayer) { cursor: text; user-select: text; }
.pdf-viewport :deep(.annotationLayer :is(.linkAnnotation, .buttonWidgetAnnotation.pushButton)) { display: none !important; }
.toolbar-divider { width: 1px; height: 24px; margin: 0 0.15rem; background: var(--border-subtle); }
.empty-document { display: grid; min-height: 560px; place-items: center; align-content: center; gap: 0.45rem; color: var(--text-muted); font-size: 0.8rem; }
.empty-document strong { color: var(--text-primary); font-size: 1rem; }
.reader-error { max-width: 34rem; margin: 0.6rem 1rem 0; color: #a1384b; font-size: 0.74rem; line-height: 1.6; text-align: center; }
.empty-mark { display: grid; width: 64px; height: 64px; place-items: center; margin-bottom: 0.35rem; border: 1px solid var(--accent); border-radius: 12px 4px; color: var(--accent-strong); background: var(--surface-elevated); font-size: 0.8rem; font-weight: 800; letter-spacing: 0.12em; }
.translation-sidebar { position: sticky; top: 86px; min-height: 560px; max-height: calc(100vh - 104px); overflow: auto; }
.sidebar-heading { position: sticky; top: 0; z-index: 2; display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 1rem; border-bottom: 1px solid var(--border-subtle); background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); }
.sidebar-heading h2 { margin: 0; font-family: var(--font-display); font-size: 1.2rem; }
.sidebar-actions { display: flex; align-items: center; gap: 0.45rem; }
.sidebar-close { display: grid; width: 30px; height: 30px; place-items: center; padding: 0; border: 1px solid var(--border-subtle); border-radius: 6px; color: var(--text-muted); background: transparent; cursor: pointer; font: inherit; font-size: 1.15rem; line-height: 1; }
.sidebar-close:hover { color: var(--accent-strong); border-color: var(--accent); background: var(--surface-elevated); }
.sidebar-tabs { display: grid; grid-template-columns: 1fr 1fr; gap: 0.25rem; margin: 0.65rem 0.75rem 0; padding: 0.2rem; border-radius: 7px; background: var(--surface-elevated); }
.sidebar-tabs button { min-height: 32px; padding: 0.35rem 0.5rem; border: 0; border-radius: 5px; color: var(--text-muted); background: transparent; cursor: pointer; font: inherit; font-size: 0.72rem; }
.sidebar-tabs button.active { color: var(--accent-strong); background: rgba(255,255,255,0.92); box-shadow: 0 2px 8px rgba(55,89,144,0.1); font-weight: 700; }
.translation-content { display: grid; gap: 1rem; padding: 1rem; }
.source-section, .target-section { display: grid; gap: 0.45rem; }
.section-label { color: var(--accent-pink); font-size: 0.68rem; font-weight: 800; letter-spacing: 0.1em; }
.source-section p, .target-section p { margin: 0; color: var(--text-secondary); font-size: 0.84rem; line-height: 1.75; white-space: pre-wrap; }
.source-section { max-height: 190px; overflow: auto; padding-bottom: 1rem; border-bottom: 1px solid var(--border-subtle); }
.target-section p { color: var(--text-primary); font-size: 0.92rem; }
.target-section p.placeholder { color: var(--text-muted); }
.target-heading { display: flex; align-items: center; justify-content: space-between; gap: 0.8rem; }
.translating-state { color: var(--accent-strong); font-size: 0.68rem; }
.sidebar-empty { display: grid; place-items: center; align-content: center; min-height: 450px; padding: 2rem; color: var(--text-muted); text-align: center; }
.sidebar-empty strong { margin: 0.75rem 0 0.25rem; color: var(--text-primary); font-size: 0.92rem; }
.sidebar-empty p { max-width: 15rem; margin: 0; font-size: 0.78rem; line-height: 1.6; }
.selection-icon { display: grid; width: 52px; height: 52px; place-items: center; border: 1px solid var(--accent); border-radius: 50%; color: var(--accent-strong); background: var(--surface-elevated); font-family: var(--font-display); font-size: 1rem; }
.sidebar-error { margin: 0 1rem 1rem; }
.history-list { display: grid; gap: 0.55rem; padding: 0.75rem; }
.history-item { position: relative; display: flex; border: 1px solid var(--border-subtle); border-radius: 7px; background: rgba(255,255,255,0.66); }
.history-main { display: grid; flex: 1; min-width: 0; gap: 0.25rem; padding: 0.7rem 2.1rem 0.7rem 0.7rem; border: 0; color: inherit; background: transparent; cursor: pointer; text-align: left; }
.history-main strong, .history-main span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.history-main strong { color: var(--text-primary); font-size: 0.78rem; }
.history-main span { color: var(--text-secondary); font-size: 0.75rem; }
.history-main small { color: var(--text-muted); font-size: 0.64rem; }
.history-remove { position: absolute; top: 0.45rem; right: 0.45rem; width: 24px; height: 24px; padding: 0; border: 0; color: var(--text-muted); background: transparent; cursor: pointer; font-size: 0.9rem; }
.history-item:hover { border-color: var(--accent); }
.history-empty { display: grid; min-height: 300px; place-items: center; align-content: center; gap: 0.3rem; padding: 1.5rem; color: var(--text-muted); text-align: center; }
.history-empty strong { color: var(--text-primary); font-size: 0.86rem; }
.history-empty p { max-width: 15rem; margin: 0; font-size: 0.74rem; line-height: 1.6; }
.term-popover { position: fixed; z-index: 50; width: min(320px, calc(100vw - 24px)); overflow: hidden; border: 1px solid var(--border-strong); border-radius: 9px; background: rgba(255,255,255,0.97); box-shadow: 0 18px 48px rgba(37,62,101,0.24); backdrop-filter: blur(14px); }
.term-popover-heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; padding: 0.7rem 0.8rem 0.55rem; border-bottom: 1px solid var(--border-subtle); }
.term-popover-heading strong { overflow: hidden; color: var(--text-secondary); font-size: 0.75rem; font-weight: 600; text-overflow: ellipsis; white-space: nowrap; }
.term-popover-heading button { width: 24px; height: 24px; padding: 0; border: 0; color: var(--text-muted); background: transparent; cursor: pointer; font-size: 1rem; line-height: 1; }
.term-popover > p { min-height: 46px; margin: 0; padding: 0.75rem 0.8rem; color: var(--text-primary); font-family: var(--font-display); font-size: 1rem; line-height: 1.55; }
.term-popover > p.placeholder { color: var(--text-muted); font-family: var(--font-body); font-size: 0.8rem; }
.term-popover-footer { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.45rem 0.8rem; background: var(--surface-elevated); }
.term-popover-footer span { color: var(--text-muted); font-size: 0.64rem; }
.term-popover-footer button { padding: 0; border: 0; color: var(--accent-strong); background: transparent; cursor: pointer; font: inherit; font-size: 0.68rem; font-weight: 700; }

@media (max-width: 900px) {
  .translator-page--embedded { width: 100%; margin-left: 0; }
  .reader-layout--sidebar { grid-template-columns: minmax(0, 1fr) 300px; }
  .config-grid { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 720px) {
  .page-header { align-items: flex-start; flex-direction: column; gap: 0.8rem; }
  .reader-layout--sidebar { grid-template-columns: 1fr; }
  .translation-sidebar { position: relative; top: auto; min-height: 340px; max-height: none; }
  .pdf-viewport, .empty-document { min-height: 420px; }
  .config-grid { grid-template-columns: 1fr; }
}
</style>
