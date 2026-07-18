<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import type { FunctionEntry } from '../types/functionSearch'

type ProviderFilter = 'all' | string

const entries = ref<FunctionEntry[]>([])
const query = ref('')
const provider = ref<ProviderFilter>('all')
const selectedId = ref('')
const isLoading = ref(true)
const loadError = ref('')
const copied = ref(false)

const providerLabels: Record<string, string> = {
  all: '全部',
  pytorch: 'PyTorch',
  python: 'Python 常用',
  backend: 'Python 后端',
  my_extension: '我的扩展',
}

const providers = computed(() => [
  'all',
  ...new Set(entries.value.map((entry) => entry.provider)),
])

const providerCounts = computed(() => entries.value.reduce<Record<string, number>>((counts, entry) => {
  counts[entry.provider] = (counts[entry.provider] ?? 0) + 1
  return counts
}, {}))

function scoreEntry(entry: FunctionEntry, normalizedQuery: string) {
  if (!normalizedQuery) return 0
  const fullName = entry.full_name.toLowerCase()
  const name = entry.name.toLowerCase()
  if (fullName === normalizedQuery || name === normalizedQuery) return 100
  if (fullName.startsWith(normalizedQuery) || name.startsWith(normalizedQuery)) return 80
  if (fullName.includes(normalizedQuery) || name.includes(normalizedQuery)) return 60
  if (entry.module.toLowerCase().includes(normalizedQuery)) return 40
  if (entry.tags.some((tag) => tag.toLowerCase().includes(normalizedQuery))) return 30
  if (entry.description.toLowerCase().includes(normalizedQuery)) return 20
  return -1
}

const filteredEntries = computed(() => {
  const normalizedQuery = query.value.trim().toLowerCase()
  return entries.value
    .filter((entry) => provider.value === 'all' || entry.provider === provider.value)
    .map((entry) => ({ entry, score: scoreEntry(entry, normalizedQuery) }))
    .filter(({ score }) => !normalizedQuery || score >= 0)
    .sort((left, right) => right.score - left.score || left.entry.full_name.localeCompare(right.entry.full_name))
    .slice(0, 120)
    .map(({ entry }) => entry)
})

const selectedEntry = computed(() => {
  const selected = entries.value.find((entry) => entry.id === selectedId.value)
  return selected ?? filteredEntries.value[0]
})

const visibleCountLabel = computed(() => {
  if (query.value.trim()) return `匹配 ${filteredEntries.value.length} 条`
  return `共 ${entries.value.length} 条`
})

async function copyExample() {
  if (!selectedEntry.value?.example) return
  await navigator.clipboard.writeText(selectedEntry.value.example)
  copied.value = true
  window.setTimeout(() => { copied.value = false }, 1400)
}

async function loadEntries() {
  isLoading.value = true
  loadError.value = ''
  try {
    const response = await fetch(`${import.meta.env.BASE_URL}function-search.json`)
    if (!response.ok) throw new Error(`索引加载失败（${response.status}）`)
    entries.value = await response.json() as FunctionEntry[]
    selectedId.value = entries.value[0]?.id ?? ''
  } catch (cause) {
    loadError.value = cause instanceof Error ? cause.message : '无法加载方法字典'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => { void loadEntries() })
</script>

<template>
  <div class="dictionary-page">
    <header class="dictionary-header">
      <div>
        <RouterLink to="/" class="back-link">← 返回首页</RouterLink>
        <p class="page-kicker">LOCAL API INDEX / 05</p>
        <h1 class="page-title">PyTorch 方法字典</h1>
        <p class="page-lead">从 function_search 索引整理的站内 API 查询工具，查函数、看签名、复制最小调用示例。</p>
      </div>
      <div class="dictionary-stat">
        <strong>{{ entries.length.toLocaleString() }}</strong>
        <span>个已索引 API</span>
      </div>
    </header>

    <section class="search-panel" aria-label="方法字典搜索">
      <label class="search-field">
        <span class="sr-only">搜索函数、模块或关键词</span>
        <input v-model="query" type="search" placeholder="搜索 torch.nn.Linear、conv2d、优化器或关键词" autocomplete="off" />
        <span class="search-hint">⌘ K</span>
      </label>
      <div class="provider-tabs" role="tablist" aria-label="方法来源">
        <button
          v-for="item in providers"
          :key="item"
          type="button"
          role="tab"
          :aria-selected="provider === item"
          :class="{ active: provider === item }"
          @click="provider = item"
        >
          {{ providerLabels[item] ?? item }}
          <span>{{ item === 'all' ? entries.length : providerCounts[item] ?? 0 }}</span>
        </button>
      </div>
    </section>

    <div v-if="isLoading" class="dictionary-state">正在加载 API 索引...</div>
    <div v-else-if="loadError" class="dictionary-state dictionary-state--error">
      <strong>{{ loadError }}</strong>
      <button type="button" @click="loadEntries">重新加载</button>
    </div>
    <div v-else class="dictionary-workspace">
      <section class="result-panel" aria-label="搜索结果">
        <div class="panel-heading">
          <strong>搜索结果</strong>
          <span>{{ visibleCountLabel }}</span>
        </div>
        <div v-if="!filteredEntries.length" class="empty-results">
          <strong>没有找到匹配 API</strong>
          <span>试试 `Linear`、`torch.optim` 或 `loss`。</span>
        </div>
        <div v-else class="result-list">
          <button
            v-for="entry in filteredEntries"
            :key="entry.id"
            type="button"
            class="result-item"
            :class="{ selected: selectedEntry?.id === entry.id }"
            @click="selectedId = entry.id"
          >
            <strong>{{ entry.full_name }}</strong>
            <span>{{ entry.signature }}</span>
            <small>{{ providerLabels[entry.provider] ?? entry.provider }} · {{ entry.category }}</small>
          </button>
        </div>
      </section>

      <article v-if="selectedEntry" class="detail-panel" aria-label="API 详情">
        <div class="detail-heading">
          <div>
            <span class="detail-provider">{{ providerLabels[selectedEntry.provider] ?? selectedEntry.provider }}</span>
            <h2>{{ selectedEntry.full_name }}</h2>
          </div>
          <span class="detail-category">{{ selectedEntry.category }}</span>
        </div>
        <p class="signature"><code>{{ selectedEntry.signature }}</code></p>
        <section class="detail-section">
          <h3>函数说明</h3>
          <p>{{ selectedEntry.description || '暂无说明，建议查看对应库的官方文档。' }}</p>
        </section>
        <section class="detail-section example-section">
          <div class="example-heading">
            <h3>调用示例</h3>
            <button type="button" class="copy-button" @click="copyExample">{{ copied ? '已复制' : '复制示例' }}</button>
          </div>
          <pre><code>{{ selectedEntry.example || '# 暂无示例' }}</code></pre>
        </section>
        <div class="detail-tags">
          <span v-for="tag in selectedEntry.tags" :key="tag">{{ tag }}</span>
        </div>
      </article>
      <div v-else class="detail-panel detail-panel--empty">选择左侧 API 查看详情。</div>
    </div>
  </div>
</template>

<style scoped>
.dictionary-page { max-width: 1180px; }
.dictionary-header { display: flex; align-items: flex-end; justify-content: space-between; gap: 2rem; margin-bottom: 1.5rem; }
.back-link { display: inline-block; margin-bottom: 1rem; color: var(--text-muted); font-size: 0.82rem; text-decoration: none; }
.back-link:hover { color: var(--accent-strong); }
.page-kicker { margin: 0 0 0.5rem; color: var(--accent-pink); font-size: 0.68rem; font-weight: 800; letter-spacing: 0.14em; }
.page-title { margin: 0 0 0.5rem; font-family: var(--font-display); font-size: clamp(2rem, 4vw, 3rem); line-height: 1.2; }
.page-lead { max-width: 48rem; margin: 0; color: var(--text-secondary); line-height: 1.75; }
.dictionary-stat { display: grid; min-width: 130px; padding: 0.8rem 1rem; border-left: 3px solid var(--accent); color: var(--text-muted); }
.dictionary-stat strong { color: var(--text-primary); font-family: var(--font-display); font-size: 1.6rem; line-height: 1.1; }
.dictionary-stat span { font-size: 0.72rem; }
.search-panel { display: grid; gap: 0.85rem; margin-bottom: 1rem; padding: 1rem; border: 1px solid var(--border-subtle); border-radius: 10px; background: var(--surface-card); }
.search-field { position: relative; display: block; }
.search-field input { width: 100%; min-height: 48px; padding: 0.7rem 4rem 0.7rem 0.85rem; border: 1px solid var(--border-strong); border-radius: 7px; color: var(--text-primary); background: rgba(255,255,255,0.84); font: inherit; font-size: 0.9rem; }
.search-field input:focus { border-color: var(--accent); outline: 2px solid color-mix(in srgb, var(--accent) 20%, transparent); }
.search-hint { position: absolute; top: 50%; right: 0.8rem; transform: translateY(-50%); color: var(--text-muted); font-size: 0.7rem; }
.provider-tabs { display: flex; flex-wrap: wrap; gap: 0.45rem; }
.provider-tabs button { min-height: 32px; padding: 0.35rem 0.65rem; border: 1px solid var(--border-subtle); border-radius: 6px; color: var(--text-muted); background: transparent; cursor: pointer; font: inherit; font-size: 0.74rem; }
.provider-tabs button span { margin-left: 0.3rem; opacity: 0.7; }
.provider-tabs button:hover, .provider-tabs button.active { border-color: var(--accent); color: var(--accent-strong); background: var(--surface-elevated); }
.dictionary-workspace { display: grid; grid-template-columns: minmax(270px, 0.85fr) minmax(0, 1.5fr); gap: 1rem; align-items: start; }
.result-panel, .detail-panel { min-width: 0; border: 1px solid var(--border-subtle); border-radius: 10px; background: var(--surface-card); }
.result-panel { overflow: hidden; }
.panel-heading { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.8rem 0.9rem; border-bottom: 1px solid var(--border-subtle); color: var(--text-primary); }
.panel-heading span { color: var(--text-muted); font-size: 0.7rem; }
.result-list { display: grid; max-height: 640px; overflow: auto; }
.result-item { display: grid; gap: 0.22rem; padding: 0.75rem 0.9rem; border: 0; border-bottom: 1px solid var(--border-subtle); color: inherit; background: transparent; cursor: pointer; text-align: left; }
.result-item:hover, .result-item.selected { background: var(--surface-elevated); }
.result-item.selected { box-shadow: inset 3px 0 0 var(--accent); }
.result-item strong { overflow: hidden; color: var(--text-primary); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.76rem; text-overflow: ellipsis; white-space: nowrap; }
.result-item span { overflow: hidden; color: var(--text-secondary); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.68rem; text-overflow: ellipsis; white-space: nowrap; }
.result-item small { color: var(--text-muted); font-size: 0.64rem; }
.detail-panel { padding: 1.15rem; }
.detail-heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; }
.detail-provider { color: var(--accent-pink); font-size: 0.68rem; font-weight: 800; letter-spacing: 0.12em; }
.detail-heading h2 { margin: 0.25rem 0 0; color: var(--text-primary); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 1.2rem; overflow-wrap: anywhere; }
.detail-category { padding: 0.25rem 0.45rem; border-radius: 5px; color: var(--accent-strong); background: var(--surface-elevated); font-size: 0.68rem; white-space: nowrap; }
.signature { margin: 0.9rem 0 1.1rem; padding: 0.7rem; overflow: auto; border: 1px solid var(--border-subtle); border-radius: 6px; color: var(--text-secondary); background: rgba(236,243,255,0.68); font-size: 0.78rem; white-space: nowrap; }
.detail-section { margin-top: 1rem; }
.detail-section h3 { margin: 0 0 0.45rem; color: var(--text-primary); font-size: 0.82rem; }
.detail-section p { margin: 0; color: var(--text-secondary); font-size: 0.86rem; line-height: 1.75; white-space: pre-wrap; }
.example-heading { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.copy-button, .dictionary-state button { min-height: 32px; padding: 0.35rem 0.6rem; border: 1px solid var(--accent); border-radius: 6px; color: var(--accent-strong); background: var(--surface-elevated); cursor: pointer; font: inherit; font-size: 0.72rem; }
.example-section pre { max-height: 300px; margin: 0; padding: 0.85rem; overflow: auto; border: 1px solid var(--border-subtle); border-radius: 6px; background: #17223c; color: #eaf2ff; font-size: 0.76rem; line-height: 1.65; white-space: pre-wrap; }
.detail-tags { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 1rem; }
.detail-tags span { padding: 0.2rem 0.4rem; border-radius: 4px; color: var(--text-muted); background: var(--surface-elevated); font-size: 0.66rem; }
.empty-results, .dictionary-state { display: grid; min-height: 180px; place-items: center; align-content: center; gap: 0.35rem; padding: 1.5rem; color: var(--text-muted); text-align: center; }
.empty-results strong, .dictionary-state strong { color: var(--text-primary); font-size: 0.86rem; }
.empty-results span { font-size: 0.76rem; }
.dictionary-state--error { border: 1px solid var(--border-subtle); border-radius: 10px; background: var(--surface-card); }
.dictionary-state--error button { margin-top: 0.45rem; }
.detail-panel--empty { min-height: 300px; display: grid; place-items: center; color: var(--text-muted); }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0; }
@media (max-width: 760px) {
  .dictionary-header { align-items: flex-start; flex-direction: column; gap: 1rem; }
  .dictionary-stat { min-width: 0; }
  .dictionary-workspace { grid-template-columns: 1fr; }
  .result-list { max-height: 360px; }
}
</style>
