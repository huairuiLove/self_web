<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { getPaperBySlug, getPaperPdfUrl, getPaperUrl } from '../data/papers'

const route = useRoute()
const paper = computed(() => getPaperBySlug(route.params.slug as string))
const pdfUrl = computed(() => (paper.value ? getPaperPdfUrl(paper.value) : undefined))
</script>

<template>
  <div v-if="paper" class="paper-detail-page">
    <RouterLink to="/papers" class="back">← 返回论文库</RouterLink>
    <header class="detail-header">
      <p class="meta">{{ paper.category }} · {{ paper.year }}</p>
      <h1 class="title">{{ paper.title }}</h1>
      <p v-if="paper.authors" class="authors">{{ paper.authors }}</p>
      <p class="summary">{{ paper.contribution }}</p>
      <a :href="getPaperUrl(paper)" class="source-link" target="_blank" rel="noopener noreferrer">
        打开原文 ↗
      </a>
    </header>

    <div v-if="pdfUrl" class="pdf-shell">
      <iframe :src="pdfUrl" :title="`${paper.title} PDF`" loading="lazy" />
    </div>
    <div v-else class="external-note">
      <p>这是一篇产品文章，不是 PDF 论文，已保留原文入口。</p>
      <a :href="getPaperUrl(paper)" target="_blank" rel="noopener noreferrer">阅读原文 ↗</a>
    </div>
  </div>
  <div v-else class="empty">
    <p>没有找到这篇资料。</p>
    <RouterLink to="/papers">回到论文库</RouterLink>
  </div>
</template>

<style scoped>
.paper-detail-page { max-width: 1120px; }
.back { display: inline-block; margin-bottom: 1.5rem; color: var(--text-muted); font-size: 0.85rem; text-decoration: none; }
.back:hover { color: var(--accent-strong); }
.detail-header { max-width: 54rem; margin-bottom: 1.5rem; }
.meta { margin: 0 0 0.55rem; color: var(--accent-pink); font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; }
.title { margin: 0 0 0.65rem; font-family: var(--font-display); font-size: clamp(1.9rem, 4vw, 3rem); line-height: 1.25; }
.authors { margin: 0 0 0.6rem; color: var(--text-muted); font-size: 0.85rem; }
.summary { max-width: 46rem; margin: 0 0 1rem; color: var(--text-secondary); line-height: 1.8; }
.source-link { display: inline-flex; color: var(--accent-strong); font-size: 0.85rem; font-weight: 700; text-decoration: none; }
.pdf-shell { overflow: hidden; min-height: 78vh; border: 1px solid var(--border-subtle); border-radius: 12px; background: #dbe7f7; box-shadow: 0 18px 45px rgba(55,89,144,0.12); }
.pdf-shell iframe { display: block; width: 100%; height: 78vh; border: 0; background: white; }
.external-note { padding: 2rem; border: 1px solid var(--border-subtle); border-radius: 12px; background: var(--surface-card); color: var(--text-secondary); }
.external-note a, .empty a { color: var(--accent-strong); }
.empty { padding: 4rem 1rem; color: var(--text-muted); text-align: center; }
</style>
