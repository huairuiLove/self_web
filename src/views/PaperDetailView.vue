<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { getPaperBySlug, getPaperPdfUrl, getPaperUrl } from '../data/papers'

const PdfTranslateView = defineAsyncComponent(() => import('./PdfTranslateView.vue'))

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
      <p v-if="paper.venue" class="venue">{{ paper.venue }}</p>
      <p class="summary">{{ paper.contribution }}</p>
      <div class="detail-actions">
        <a v-if="paper.externalUrl" :href="getPaperUrl(paper)" class="source-link" target="_blank" rel="noopener noreferrer">
          阅读原文
        </a>
      </div>
    </header>

    <section v-if="paper.readingGoal" class="reading-guide" aria-labelledby="reading-guide-title">
      <div class="guide-heading">
        <p class="guide-kicker">READING NOTES</p>
        <h2 id="reading-guide-title" class="guide-title">给自己的阅读提醒</h2>
      </div>
      <dl class="guide-list">
        <div class="guide-item">
          <dt>这次读什么</dt>
          <dd>{{ paper.readingGoal }}</dd>
        </div>
        <div v-if="paper.keyIdea" class="guide-item">
          <dt>抓住的主线</dt>
          <dd>{{ paper.keyIdea }}</dd>
        </div>
        <div v-if="paper.watchFor" class="guide-item">
          <dt>不要直接相信</dt>
          <dd>{{ paper.watchFor }}</dd>
        </div>
      </dl>
    </section>

    <PdfTranslateView v-if="pdfUrl" embedded :paper="paper" />
    <div v-else class="external-note">
      <p>这篇资料暂未保存在站内，阅读入口指向作者页面、出版方或 arXiv。</p>
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
.venue { margin: -0.25rem 0 0.7rem; color: var(--accent-strong); font-size: 0.8rem; }
.summary { max-width: 46rem; margin: 0 0 1rem; color: var(--text-secondary); line-height: 1.8; }
.detail-actions { display: flex; flex-wrap: wrap; align-items: center; gap: 1rem; }
.source-link { display: inline-flex; color: var(--text-muted); font-size: 0.82rem; text-decoration: none; }
.source-link:hover { color: var(--accent-pink); }
.reading-guide { display: grid; grid-template-columns: minmax(180px, 0.42fr) minmax(0, 1fr); gap: clamp(2rem, 6vw, 5rem); margin: 2rem 0; padding: 1.5rem 0; border-top: 1px solid var(--border-strong); border-bottom: 1px solid var(--border-strong); }
.guide-kicker { margin: 0 0 0.45rem; color: var(--accent-pink); font-size: 0.68rem; font-weight: 700; letter-spacing: 0.14em; }
.guide-title { margin: 0; font-family: var(--font-display); font-size: 1.3rem; font-weight: 600; }
.guide-list { display: grid; gap: 1rem; margin: 0; }
.guide-item { display: grid; grid-template-columns: 7rem minmax(0, 1fr); gap: 1rem; }
.guide-item dt { color: var(--accent-strong); font-size: 0.78rem; font-weight: 700; }
.guide-item dd { margin: 0; color: var(--text-secondary); font-size: 0.88rem; line-height: 1.75; }
.external-note { padding: 2rem; border: 1px solid var(--border-subtle); border-radius: 12px; background: var(--surface-card); color: var(--text-secondary); }
.external-note a, .empty a { color: var(--accent-strong); }
.empty { padding: 4rem 1rem; color: var(--text-muted); text-align: center; }

@media (max-width: 640px) {
  .reading-guide { grid-template-columns: 1fr; gap: 1.25rem; }
  .guide-item { grid-template-columns: 1fr; gap: 0.25rem; }
}
</style>
