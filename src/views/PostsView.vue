<script setup lang="ts">
import { computed } from 'vue'
import { posts } from '../data/posts'
import PostCard from '../components/posts/PostCard.vue'

const sortedPosts = computed(() =>
  [...posts].sort((a, b) => b.publishedAt.localeCompare(a.publishedAt)),
)
</script>

<template>
  <div class="page">
    <header class="page-header">
      <p class="page-kicker">FIELD NOTES / 02</p>
      <h1 class="page-title">经验贴</h1>
      <p class="page-lead">整理后的实践记录，方便检索、复盘与分享。</p>
    </header>
    <div class="list">
      <PostCard v-for="post in sortedPosts" :key="post.id" :post="post" />
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

.list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
