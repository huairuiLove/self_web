<script setup lang="ts">
import { useSiteTheme } from '../../composables/useSiteTheme'
import type { VisualThemeName } from '../../data/themes'

const { theme, themes, setTheme } = useSiteTheme()

function chooseTheme(name: VisualThemeName) {
  setTheme(name)
}
</script>

<template>
  <div class="theme-switcher" aria-label="选择角色背景">
    <span class="theme-label">背景主题</span>
    <div class="theme-options" role="group" aria-label="角色背景选项">
      <button
        v-for="item in Object.values(themes)"
        :key="item.name"
        type="button"
        class="theme-option"
        :class="{ 'theme-option--active': theme === item.name }"
        :aria-pressed="theme === item.name"
        @click="chooseTheme(item.name)"
      >
        <span class="theme-swatch" :style="{ backgroundColor: item.accent }" aria-hidden="true" />
        <span>
          <strong>{{ item.label }}</strong>
          <small>{{ item.subtitle }}</small>
        </span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.theme-switcher { display: grid; gap: 0.7rem; }
.theme-label { color: var(--text-muted); font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em; }
.theme-options { display: flex; flex-wrap: wrap; gap: 0.55rem; }
.theme-option {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  min-width: 132px;
  padding: 0.55rem 0.7rem;
  border: 1px solid var(--border-subtle);
  border-radius: 9px;
  color: var(--text-secondary);
  background: rgba(255, 255, 255, 0.7);
  text-align: left;
  cursor: pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}
.theme-option:hover { transform: translateY(-1px); border-color: var(--border-strong); }
.theme-option--active { border-color: var(--accent); box-shadow: 0 5px 18px rgba(37, 116, 216, 0.14); }
.theme-swatch { width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 0 4px color-mix(in srgb, currentColor 12%, transparent); }
.theme-option strong, .theme-option small { display: block; }
.theme-option strong { color: var(--text-primary); font-size: 0.8rem; font-weight: 700; }
.theme-option small { margin-top: 0.08rem; color: var(--text-muted); font-size: 0.66rem; }

@media (max-width: 480px) {
  .theme-option { flex: 1; min-width: 0; }
}
</style>
