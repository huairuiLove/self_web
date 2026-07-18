<script setup lang="ts">
import { profile } from '../../data/profile'
</script>

<template>
  <footer class="footer">
    <p class="footer-copy"><span class="footer-kicker">MH / 01</span> © {{ new Date().getFullYear() }} {{ profile.englishName }}</p>
    <div class="footer-links">
      <a
        v-for="link in profile.links"
        :key="link.href"
        :href="link.href"
        class="footer-link"
        target="_blank"
        rel="noopener noreferrer"
      >
        {{ link.label }}
      </a>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  position: relative;
  z-index: 1;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  width: min(1120px, 100%);
  margin: 0 auto;
  padding: 2.25rem 1.5rem 2.75rem;
  border-top: 1px solid var(--border-subtle);
  color: var(--text-muted);
  font-size: 0.875rem;
}

.footer-links {
  display: flex;
  gap: 1rem;
}

.footer-link {
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: var(--accent);
}

.footer-kicker {
  margin-right: 0.75rem;
  color: var(--accent-pink);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
}
</style>
