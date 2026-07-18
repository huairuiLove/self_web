<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import SiteHeader from '../components/layout/SiteHeader.vue'
import SiteFooter from '../components/layout/SiteFooter.vue'
import { useSiteTheme } from '../composables/useSiteTheme'

const route = useRoute()
const isHome = computed(() => route.name === 'home')
const { activeImage, activeImageFit } = useSiteTheme()
</script>

<template>
  <div class="site-shell" :style="{ '--character-bg': `url(${activeImage})`, '--character-size': activeImageFit }">
    <div class="site-grid" aria-hidden="true" />
    <SiteHeader />
    <main class="site-main" :class="{ 'site-main--home': isHome }">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <SiteFooter />
  </div>
</template>

<style scoped>
.site-shell {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  isolation: isolate;
  overflow: clip;
  background: var(--bg-base);
}

.site-shell::before {
  content: '';
  position: fixed;
  inset: 0;
  z-index: -2;
  background-image: var(--character-bg);
  background-position: center;
  background-size: var(--character-size, cover);
  background-repeat: no-repeat;
  opacity: 0.5;
  filter: saturate(1.05) contrast(1.02);
  mask-image: linear-gradient(90deg, transparent 0%, black 34%, black 100%);
  transition: background-image 0.35s ease, opacity 0.35s ease;
}

.site-shell::after {
  content: '';
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background: linear-gradient(90deg, rgba(248, 250, 255, 0.82) 0%, rgba(248, 250, 255, 0.62) 43%, rgba(248, 250, 255, 0.35) 100%);
}

.site-grid {
  pointer-events: none;
  position: fixed;
  inset: 0;
  opacity: 0.6;
  background-image: linear-gradient(rgba(37, 116, 216, 0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(37, 116, 216, 0.07) 1px, transparent 1px);
  background-size: 42px 42px;
  mask-image: linear-gradient(to bottom, black, transparent 82%);
  z-index: 0;
}

.site-main {
  position: relative;
  z-index: 1;
  flex: 1;
  width: min(1120px, 100%);
  margin: 0 auto;
  padding: 2.5rem 1.5rem 5rem;
}

.site-main--home {
  padding-top: 1.25rem;
}

.page-enter-active,
.page-leave-active {
  transition: opacity 0.22s ease, transform 0.22s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
