<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import DOMPurify from 'dompurify'
import { getPostBySlug } from '../data/posts'

const route = useRoute()
const post = computed(() => getPostBySlug(route.params.slug as string))
const safeContent = computed(() => (post.value ? DOMPurify.sanitize(post.value.content) : ''))

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>

<template>
  <article v-if="post" class="article">
    <RouterLink to="/posts" class="back">← 返回经验贴</RouterLink>
    <header class="article-header">
      <time :datetime="post.publishedAt">{{ formatDate(post.publishedAt) }}</time>
      <h1>{{ post.title }}</h1>
      <p class="excerpt">{{ post.excerpt }}</p>
      <ul class="tags">
        <li v-for="tag in post.tags" :key="tag">{{ tag }}</li>
      </ul>
      <span class="read">{{ post.readMinutes }} 分钟阅读</span>
    </header>
    <!-- DOMPurify sanitizes the trusted article payload before this render. -->
    <!-- eslint-disable-next-line vue/no-v-html -->
    <div class="prose" v-html="safeContent" />
  </article>
  <div v-else class="empty">
    <p>文章不存在。</p>
    <RouterLink to="/posts">回到列表</RouterLink>
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

.article-header {
  margin-bottom: 2.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border-subtle);
  max-width: 42rem;
}

.article-header time {
  display: block;
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.article-header h1 {
  margin: 0 0 1rem;
  font-family: var(--font-display);
  font-size: clamp(1.85rem, 4vw, 2.5rem);
  font-weight: 500;
  line-height: 1.25;
}

.excerpt {
  margin: 0 0 1rem;
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--text-muted);
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin: 0 0 0.75rem;
  padding: 0;
  list-style: none;
}

.tags li {
  font-size: 0.75rem;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  background: var(--surface-elevated);
  color: var(--text-secondary);
}

.read {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.prose {
  max-width: 42rem;
  line-height: 1.85;
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
.prose h2 {
  margin: 2rem 0 0.75rem;
  font-family: var(--font-display);
  font-size: 1.35rem;
  font-weight: 500;
  color: var(--text-primary);
}

.prose p {
  margin: 0 0 1rem;
}

.prose ul {
  margin: 0 0 1rem;
  padding-left: 1.25rem;
}

.prose li {
  margin-bottom: 0.35rem;
}

.prose code {
  font-size: 0.88em;
  padding: 0.12rem 0.35rem;
  border-radius: 5px;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  color: var(--accent);
}
</style>
