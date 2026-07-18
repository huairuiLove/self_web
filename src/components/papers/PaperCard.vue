<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { ResearchPaper } from '../../data/papers'

defineProps<{ paper: ResearchPaper }>()
</script>

<template>
  <article class="paper-card">
    <div class="paper-topline">
      <span class="paper-category">{{ paper.category }}</span>
      <span class="paper-year">{{ paper.year }}</span>
    </div>
    <h2 class="paper-title">
      <RouterLink :to="`/papers/${paper.slug}`">{{ paper.title }}</RouterLink>
    </h2>
    <p v-if="paper.authors" class="paper-authors">{{ paper.authors }}</p>
    <p v-if="paper.venue" class="paper-venue">{{ paper.venue }}</p>
    <p class="paper-contribution">{{ paper.contribution }}</p>
    <div class="paper-actions">
      <RouterLink :to="`/papers/${paper.slug}`" class="paper-detail">
        站内查看 <span aria-hidden="true">↗</span>
      </RouterLink>
      <a
        v-if="paper.externalUrl"
        :href="paper.externalUrl"
        class="paper-source"
        target="_blank"
        rel="noopener noreferrer"
      >
        原文
      </a>
    </div>
  </article>
</template>

<style scoped>
.paper-card { display: flex; flex-direction: column; min-height: 238px; padding: 1.25rem 1.35rem 1.35rem; border: 1px solid var(--border-subtle); border-radius: 12px; background: var(--surface-card); box-shadow: 0 12px 30px rgba(55, 89, 144, 0.07); transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease; }
.paper-card:hover { transform: translateY(-2px); border-color: var(--accent); box-shadow: 0 16px 34px rgba(55, 89, 144, 0.12); }
.paper-topline { display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin-bottom: 0.9rem; color: var(--text-muted); font-size: 0.72rem; }
.paper-category { color: var(--accent-pink); font-weight: 700; letter-spacing: 0.06em; }
.paper-year { font-variant-numeric: tabular-nums; }
.paper-title { margin: 0 0 0.45rem; font-family: var(--font-display); font-size: 1.12rem; line-height: 1.45; }
.paper-title a { color: var(--text-primary); text-decoration: none; }
.paper-title a:hover { color: var(--accent-strong); }
.paper-authors { margin: 0 0 0.65rem; color: var(--text-muted); font-size: 0.78rem; }
.paper-venue { margin: -0.35rem 0 0.65rem; color: var(--accent-strong); font-size: 0.72rem; }
.paper-contribution { flex: 1; margin: 0; color: var(--text-secondary); font-size: 0.88rem; line-height: 1.65; }
.paper-actions { display: flex; align-items: center; gap: 1rem; margin-top: 1.1rem; }
.paper-detail { color: var(--accent-strong); font-size: 0.82rem; font-weight: 700; text-decoration: none; }
.paper-source { color: var(--text-muted); font-size: 0.78rem; text-decoration: none; }
.paper-detail:hover, .paper-source:hover { color: var(--accent-pink); }
</style>
