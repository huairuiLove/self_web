<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'

const nav = [
  { to: '/', index: '00', label: '首页' },
  { to: '/projects', index: '01', label: '项目' },
  { to: '/posts', index: '02', label: '经验贴' },
  { to: '/papers', index: '03', label: '论文库' },
  { to: '/about', index: '04', label: '关于我' },
]

const route = useRoute()

function isActive(path: string) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

<template>
  <header class="header">
    <RouterLink to="/" class="brand">
      <span class="brand-mark" aria-hidden="true">逢</span>
      <span class="brand-text">逢瑾fengjin<span class="brand-dot">/</span></span>
    </RouterLink>
    <nav class="nav" aria-label="主导航">
      <RouterLink
        v-for="item in nav"
        :key="item.to"
        :to="item.to"
        class="nav-link"
        :class="{ 'nav-link--active': isActive(item.to) }"
      >
        <span class="nav-index">{{ item.index }}</span>{{ item.label }}
      </RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.header { position: sticky; top: 0; z-index: 10; display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 1.1rem 1.5rem; margin: 0 auto; width: min(1120px, 100%); backdrop-filter: blur(12px); background: color-mix(in srgb, var(--bg-base) 88%, transparent); border-bottom: 1px solid var(--border-subtle); }
.brand { display: inline-flex; align-items: center; gap: 0.65rem; flex: 0 0 auto; text-decoration: none; color: var(--text-primary); font-size: 0.95rem; font-weight: 700; letter-spacing: 0.16em; }
.brand-mark { display: grid; width: 30px; height: 30px; place-items: center; border: 1px solid var(--accent); border-radius: 8px 2px 8px 2px; color: var(--bg-base); background: var(--accent); font-family: var(--font-display); font-size: 0.95rem; letter-spacing: 0; box-shadow: 4px 4px 0 var(--accent-pink); }
.brand-dot, .nav-index { color: var(--accent-pink); }
.nav { display: flex; gap: 0.25rem; overflow-x: auto; scrollbar-width: none; }
.nav::-webkit-scrollbar { display: none; }
.nav-link { position: relative; padding: 0.45rem 0.58rem; border-radius: 6px; white-space: nowrap; font-size: 0.78rem; font-weight: 500; color: var(--text-muted); text-decoration: none; transition: color 0.2s ease, background 0.2s ease; }
.nav-index { margin-right: 0.25rem; font-size: 0.62rem; }
.nav-link:hover { color: var(--text-primary); background: var(--surface-hover); }
.nav-link--active { color: var(--text-primary); background: var(--surface-elevated); box-shadow: inset 0 -2px 0 var(--accent); }
@media (max-width: 960px) { .header { align-items: flex-start; flex-direction: column; padding: 0.9rem 1rem 0.7rem; } .nav { width: 100%; } }
</style>
