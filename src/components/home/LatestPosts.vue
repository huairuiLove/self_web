<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { posts } from '../../data/posts'
import PostCard from '../posts/PostCard.vue'

const latest = computed(() =>
  [...posts].sort((a, b) => b.publishedAt.localeCompare(a.publishedAt)).slice(0, 3),
)
</script>

<template>
  <section class="section" aria-labelledby="latest-posts-heading">
    <div class="section-head">
      <div>
        <p class="section-kicker">FIELD NOTES / 02</p>
        <h2 id="latest-posts-heading" class="section-title">最新经验贴</h2>
        <p class="section-desc">把实践中的判断、取舍与复盘，留给未来的自己。</p>
      </div>
      <RouterLink to="/posts" class="section-link">全部文章</RouterLink>
    </div>
    <div class="list">
      <PostCard v-for="post in latest" :key="post.id" :post="post" />
    </div>
  </section>
</template>

<style scoped>
.section {
  margin-bottom: 2rem;
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

.list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
