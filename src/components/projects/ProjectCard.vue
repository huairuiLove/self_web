<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { Project } from '../../types/content'

defineProps<{
  project: Project
  compact?: boolean
}>()
</script>

<template>
  <article class="card">
    <RouterLink
      :to="`/projects/${project.id}`"
      class="card-visual"
      :class="{ 'card-visual--cover': project.cover }"
      :style="{ background: project.gradient }"
    >
      <img v-if="project.cover" class="card-cover" :src="project.cover" :alt="`${project.title}封面`" />
      <span class="card-index">{{ project.id === 'portfolio' ? '01' : project.id === 'toolkit' ? '02' : project.id === 'ttc-company-map' ? '04' : '03' }}</span>
      <span class="card-year">{{ project.year }}</span>
    </RouterLink>
    <div class="card-body">
      <h3 class="card-title">
        <RouterLink :to="`/projects/${project.id}`">{{ project.title }}</RouterLink>
      </h3>
      <p class="card-summary">{{ compact ? project.summary : project.summary }}</p>
      <ul v-if="!compact" class="card-tags">
        <li v-for="tag in project.tags" :key="tag">{{ tag }}</li>
      </ul>
      <div class="card-actions">
        <RouterLink :to="`/projects/${project.id}`" class="card-more">查看详情 →</RouterLink>
        <a
          v-if="project.repo"
          :href="project.repo"
          class="card-ext"
          target="_blank"
          rel="noopener noreferrer"
          @click.stop
        >
          仓库
        </a>
        <a
          v-else-if="project.link"
          :href="project.link"
          class="card-ext"
          target="_blank"
          rel="noopener noreferrer"
          @click.stop
        >
          访问
        </a>
      </div>
    </div>
  </article>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-radius: 12px;
  border: 1px solid var(--border-subtle);
  background: var(--surface-card);
  overflow: hidden;
  transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
}

.card:hover {
  border-color: color-mix(in srgb, var(--accent) 35%, var(--border-subtle));
  transform: translateY(-3px);
  box-shadow: var(--shadow-card);
}

.card-visual {
  display: block;
  position: relative;
  aspect-ratio: 16 / 9;
  background-position: center;
  background-size: cover;
  text-decoration: none;
  isolation: isolate;
}

.card-visual::after { content: ''; position: absolute; inset: 0; background: linear-gradient(135deg, rgba(8, 10, 19, 0.08), rgba(8, 10, 19, 0.6)); z-index: -1; }
.card-visual--cover::after { background: transparent; }
.card-cover { width: 100%; height: 100%; object-fit: contain; }

.card-index {
  position: absolute;
  z-index: 1;
  top: 0.85rem;
  left: 0.95rem;
  color: rgba(255, 255, 255, 0.78);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
}

.card-year {
  position: absolute;
  z-index: 1;
  bottom: 0.75rem;
  right: 0.85rem;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: rgba(255, 255, 255, 0.85);
  background: rgba(0, 0, 0, 0.35);
  padding: 0.25rem 0.45rem;
  border-radius: 4px;
  backdrop-filter: blur(4px);
}

.card-body {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 1.25rem 1.35rem 1.35rem;
  gap: 0.65rem;
}

.card-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.2rem;
  font-weight: 500;
  line-height: 1.35;
}

.card-title a {
  color: var(--text-primary);
  text-decoration: none;
}

.card-title a:hover {
  color: var(--accent);
}

.card-summary {
  margin: 0;
  flex: 1;
  font-size: 0.925rem;
  line-height: 1.65;
  color: var(--text-muted);
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.card-tags li {
  font-size: 0.72rem;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: var(--surface-elevated);
  color: var(--text-secondary);
  border: 1px solid var(--border-subtle);
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.25rem;
}

.card-more {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--accent);
  text-decoration: none;
}

.card-more:hover {
  text-decoration: underline;
}

.card-ext {
  font-size: 0.8rem;
  color: var(--text-muted);
  text-decoration: none;
}

.card-ext:hover {
  color: var(--text-primary);
}
</style>
