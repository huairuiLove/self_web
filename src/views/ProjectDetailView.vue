<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { getProjectById } from '../data/projects'

const route = useRoute()
const project = computed(() => getProjectById(route.params.id as string))
</script>

<template>
  <div v-if="project" class="page">
    <RouterLink to="/projects" class="back">← 返回项目列表</RouterLink>
    <div class="banner" :style="{ background: project.gradient }" />
    <header class="detail-header">
      <p class="meta">{{ project.year }} · {{ project.tags.join(' / ') }}</p>
      <h1 class="title">{{ project.title }}</h1>
      <p class="summary">{{ project.summary }}</p>
      <div class="actions">
        <a
          v-if="project.repo"
          :href="project.repo"
          class="btn btn-primary"
          target="_blank"
          rel="noopener noreferrer"
        >
          查看仓库
        </a>
        <a
          v-if="project.link"
          :href="project.link"
          class="btn btn-ghost"
          target="_blank"
          rel="noopener noreferrer"
        >
          在线访问
        </a>
      </div>
    </header>
    <p class="prose">{{ project.description }}</p>
  </div>
  <div v-else class="empty">
    <p>未找到该项目。</p>
    <RouterLink to="/projects">回到项目列表</RouterLink>
  </div>
</template>

<style scoped>
.back {
  display: inline-block;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
  color: var(--text-muted);
  text-decoration: none;
}

.back:hover {
  color: var(--accent);
}

.banner {
  height: 14rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  border: 1px solid var(--border-subtle);
}

.detail-header {
  margin-bottom: 2rem;
  max-width: 40rem;
}

.meta {
  margin: 0 0 0.5rem;
  font-size: 0.85rem;
  color: var(--accent);
  letter-spacing: 0.04em;
}

.title {
  margin: 0 0 0.75rem;
  font-family: var(--font-display);
  font-size: clamp(1.85rem, 4vw, 2.35rem);
  font-weight: 500;
  line-height: 1.2;
}

.summary {
  margin: 0 0 1.5rem;
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--text-muted);
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.55rem 1.15rem;
  border-radius: 7px;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
}

.btn-primary {
  color: var(--bg-base);
  background: linear-gradient(135deg, var(--accent), var(--accent-muted));
}

.btn-ghost {
  color: var(--text-primary);
  border: 1px solid var(--border-strong);
}

.prose {
  max-width: 40rem;
  line-height: 1.8;
  color: var(--text-secondary);
}

.empty {
  text-align: center;
  padding: 4rem 1rem;
  color: var(--text-muted);
}

.empty a {
  color: var(--accent);
}
</style>

<style>
.prose p {
  margin: 0 0 1rem;
}
</style>
