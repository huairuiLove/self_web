<script setup lang="ts">
import { projects } from '../data/projects'
import ProjectCard from '../components/projects/ProjectCard.vue'
</script>

<template>
  <div class="page">
    <header class="page-header">
      <p class="page-kicker">SELECTED WORKS / 01</p>
      <h1 class="page-title">项目</h1>
      <p class="page-lead">个人作品与实验，记录从想法到交付的过程。</p>
    </header>
    <div class="grid">
      <ProjectCard v-for="project in projects" :key="project.id" :project="project" />
    </div>
  </div>
</template>

<style scoped>
.page-header {
  margin-bottom: 2.5rem;
  max-width: 36rem;
}

.page-title {
  margin: 0 0 0.75rem;
  font-family: var(--font-display);
  font-size: clamp(2rem, 4vw, 2.5rem);
  font-weight: 500;
}

.page-kicker { margin: 0 0 0.65rem; color: var(--accent-pink); font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em; }

.page-lead {
  margin: 0;
  line-height: 1.7;
  color: var(--text-muted);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
  gap: 1.25rem;
}
</style>
