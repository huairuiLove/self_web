<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { Post } from '../../types/content'

defineProps<{
  post: Post
}>()

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>

<template>
  <article class="post-card">
    <time class="post-date" :datetime="post.publishedAt">{{ formatDate(post.publishedAt) }}</time>
    <h3 class="post-title">
      <RouterLink :to="`/posts/${post.slug}`">{{ post.title }}</RouterLink>
    </h3>
    <p class="post-excerpt">{{ post.excerpt }}</p>
    <div class="post-meta">
      <ul class="post-tags">
        <li v-for="tag in post.tags" :key="tag">{{ tag }}</li>
      </ul>
      <span class="post-read">{{ post.readMinutes }} 分钟阅读</span>
    </div>
    <RouterLink :to="`/posts/${post.slug}`" class="post-link">阅读全文 →</RouterLink>
  </article>
</template>

<style scoped>
.post-card {
  padding: 1.5rem 1.65rem;
  border-radius: 12px;
  border: 1px solid var(--border-subtle);
  background: var(--surface-card);
  transition: border-color 0.25s ease, background 0.25s ease;
}

.post-card:hover {
  border-color: color-mix(in srgb, var(--accent) 30%, var(--border-subtle));
  background: color-mix(in srgb, var(--surface-card) 92%, var(--accent) 8%);
}

.post-date {
  display: block;
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}

.post-title {
  margin: 0 0 0.65rem;
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 500;
  line-height: 1.4;
}

.post-title a {
  color: var(--text-primary);
  text-decoration: none;
}

.post-title a:hover {
  color: var(--accent);
}

.post-excerpt {
  margin: 0 0 1rem;
  font-size: 0.925rem;
  line-height: 1.7;
  color: var(--text-muted);
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.post-tags li {
  font-size: 0.72rem;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: var(--surface-elevated);
  color: var(--text-secondary);
}

.post-read {
  font-size: 0.78rem;
  color: var(--text-muted);
}

.post-link {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--accent);
  text-decoration: none;
}

.post-link:hover {
  text-decoration: underline;
}
</style>
