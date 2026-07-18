<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { projects } from '../../data/projects'
import ProjectCard from '../projects/ProjectCard.vue'

const featured = computed(() => projects.filter((p) => p.featured))
</script>

<template>
  <section class="section" aria-labelledby="featured-projects-heading">
    <div class="section-head">
      <div>
        <p class="section-kicker">SELECTED WORKS / 01</p>
        <h2 id="featured-projects-heading" class="section-title">精选项目</h2>
        <p class="section-desc">正在做与已完成的作品，持续把想法变成可以使用的东西。</p>
      </div>
      <RouterLink to="/projects" class="section-link">全部项目</RouterLink>
    </div>
    <div class="grid">
      <ProjectCard v-for="project in featured" :key="project.id" :project="project" />
    </div>
  </section>
</template>

<style scoped>
.section {
  margin-bottom: 4rem;
}

.section-head {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.75rem;
}

.section-title {
  margin: 0 0 0.35rem;
  font-family: var(--font-display);
  font-size: 1.65rem;
  font-weight: 500;
}

.section-kicker { margin: 0 0 0.45rem; color: var(--accent-pink); font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em; }

.section-desc {
  margin: 0;
  font-size: 0.925rem;
  color: var(--text-muted);
}

.section-link {
  font-size: 0.875rem;
  color: var(--accent);
  text-decoration: none;
}

.section-link:hover {
  text-decoration: underline;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 320px), 1fr));
  gap: 1.25rem;
}
</style>
