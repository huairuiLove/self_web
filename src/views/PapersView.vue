<script setup lang="ts">
import { computed, shallowRef } from 'vue'
import PaperCard from '../components/papers/PaperCard.vue'
import { papers, type PaperCategory } from '../data/papers'

const selectedCategory = shallowRef<PaperCategory | '全部'>('全部')
const categories = ['全部', ...Array.from(new Set(papers.map((paper) => paper.category)))] as Array<PaperCategory | '全部'>
const visiblePapers = computed(() => selectedCategory.value === '全部'
  ? papers
  : papers.filter((paper) => paper.category === selectedCategory.value))
const activeLearningCount = papers.filter((paper) => paper.category.startsWith('主动学习')).length
</script>

<template>
  <div class="page">
    <header class="page-header">
      <p class="page-kicker">READING ROOM / 03</p>
      <h1 class="page-title">研究论文库</h1>
      <p class="page-lead">保留 Agent 学习资料，并新增 {{ activeLearningCount }} 篇主动学习阅读条目。基础线用来搭建方法框架，医学线用来校准真实标注成本、数据划分与临床工作流。</p>
    </header>

    <div class="filters" role="group" aria-label="论文分类">
      <button
        v-for="category in categories"
        :key="category"
        type="button"
        class="filter"
        :class="{ 'filter--active': selectedCategory === category }"
        :aria-pressed="selectedCategory === category"
        @click="selectedCategory = category"
      >
        {{ category }}
      </button>
    </div>

    <div class="paper-grid">
      <PaperCard v-for="paper in visiblePapers" :key="paper.id" :paper="paper" />
    </div>
  </div>
</template>

<style scoped>
.page-header { max-width: 44rem; margin-bottom: 2rem; }
.page-kicker { margin: 0 0 0.65rem; color: var(--accent-pink); font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em; }
.page-title { margin: 0 0 0.75rem; font-family: var(--font-display); font-size: clamp(2rem, 4vw, 2.8rem); font-weight: 600; }
.page-lead { margin: 0; color: var(--text-secondary); line-height: 1.8; }
.filters { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem; }
.filter { padding: 0.45rem 0.7rem; border: 1px solid var(--border-subtle); border-radius: 6px; color: var(--text-secondary); background: rgba(255,255,255,0.66); cursor: pointer; font: inherit; font-size: 0.78rem; }
.filter:hover, .filter--active { color: var(--accent-strong); border-color: var(--accent); background: var(--surface-elevated); }
.paper-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); gap: 1rem; }
</style>
