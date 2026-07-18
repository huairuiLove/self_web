<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="dictionary-promo" aria-labelledby="dictionary-promo-heading">
    <div>
      <p class="section-kicker">DEVELOPER TOOL / 03</p>
      <h2 id="dictionary-promo-heading">PyTorch 方法字典</h2>
      <p>把 function_search 里的 API 索引搬到站内，查函数名、签名、说明和调用示例。</p>
    </div>
    <RouterLink to="/function-search" class="promo-link">打开方法字典 <span aria-hidden="true">↗</span></RouterLink>
  </section>
</template>

<style scoped>
.dictionary-promo { display: flex; align-items: center; justify-content: space-between; gap: 2rem; margin-bottom: 4rem; padding: 1.35rem 1.5rem; border: 1px solid var(--border-subtle); border-left: 4px solid var(--accent); border-radius: 8px; background: color-mix(in srgb, var(--surface-card) 90%, var(--surface-elevated)); }
.section-kicker { margin: 0 0 0.45rem; color: var(--accent-pink); font-size: 0.68rem; font-weight: 800; letter-spacing: 0.14em; }
.dictionary-promo h2 { margin: 0 0 0.3rem; font-family: var(--font-display); font-size: 1.35rem; }
.dictionary-promo p { margin: 0; color: var(--text-secondary); font-size: 0.86rem; line-height: 1.65; }
.promo-link { flex: 0 0 auto; color: var(--accent-strong); font-size: 0.8rem; font-weight: 700; text-decoration: none; }
.promo-link:hover { color: var(--accent-pink); }
@media (max-width: 640px) { .dictionary-promo { align-items: flex-start; flex-direction: column; gap: 0.8rem; } }
</style>
