<script setup lang="ts">
import { RouterLink } from 'vue-router'
import heroImage from '../../assets/hero.png'
import { profile } from '../../data/profile'
import ThemeSwitcher from './ThemeSwitcher.vue'
</script>

<template>
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-copy">
      <p class="hero-eyebrow"><span class="eyebrow-dot" aria-hidden="true" /> PORTFOLIO / 2026</p>
      <h1 id="hero-title" class="hero-title">
        你好，我是<br />
        <span class="hero-name">{{ profile.name }}</span>
      </h1>
      <p class="hero-english">{{ profile.englishName }}</p>
      <p class="hero-bio">{{ profile.bio }}</p>
      <div class="hero-actions">
        <RouterLink to="/projects" class="btn btn-primary">浏览项目 <span aria-hidden="true">↗</span></RouterLink>
        <RouterLink to="/posts" class="btn btn-ghost">阅读手记</RouterLink>
      </div>
      <ThemeSwitcher />
      <div class="hero-links" aria-label="外部链接">
        <a
          v-for="link in profile.links"
          :key="link.href"
          :href="link.href"
          class="hero-link"
          target="_blank"
          rel="noopener noreferrer"
        >
          {{ link.label }} <span aria-hidden="true">↗</span>
        </a>
      </div>
    </div>

    <div class="hero-art" aria-label="个人主页视觉标识">
      <div class="art-label art-label--top">CREATE / EXPLORE</div>
      <div class="art-frame">
        <span class="art-corner art-corner--tl" aria-hidden="true" />
        <span class="art-corner art-corner--br" aria-hidden="true" />
        <img :src="heroImage" alt="紫色发光的几何层叠视觉" class="art-image" />
        <div class="art-orbit art-orbit--one" aria-hidden="true" />
        <div class="art-orbit art-orbit--two" aria-hidden="true" />
      </div>
      <div class="art-note"><span>01</span> 个人作品集<br />与技术实验场</div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr);
  align-items: center;
  gap: clamp(2.5rem, 7vw, 6rem);
  min-height: 560px;
  padding: 2.5rem 0 5rem;
}

.hero-copy { max-width: 590px; }

.hero-eyebrow {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  margin: 0 0 1.4rem;
  color: var(--accent);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.16em;
}

.eyebrow-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent-pink);
  box-shadow: 0 0 0 4px rgba(255, 120, 188, 0.13);
}

.hero-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(2.9rem, 7vw, 5.4rem);
  font-weight: 600;
  line-height: 1.08;
  letter-spacing: 0;
}

.hero-name {
  color: var(--accent-yellow);
  text-shadow: 5px 5px 0 rgba(255, 120, 188, 0.2);
}

.hero-english {
  margin: 0.8rem 0 1.35rem;
  color: var(--accent-pink);
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.hero-bio {
  max-width: 32rem;
  margin: 0 0 2rem;
  color: var(--text-secondary);
  font-size: 1.05rem;
  line-height: 1.85;
}

.hero-actions { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 2rem; }

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  justify-content: center;
  min-height: 44px;
  padding: 0.65rem 1.2rem;
  border-radius: 7px;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  transition: transform 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
}

.btn-primary { color: var(--bg-base); background: var(--accent); box-shadow: 4px 4px 0 var(--accent-pink); }
.btn-primary:hover { transform: translate(2px, 2px); box-shadow: 2px 2px 0 var(--accent-pink); }
.btn-ghost { color: var(--text-primary); border: 1px solid var(--border-strong); background: var(--surface-card); }
.btn-ghost:hover { background: var(--surface-hover); }

.hero-links { display: flex; flex-wrap: wrap; gap: 1.25rem; }
.hero-link { color: var(--text-muted); font-size: 0.82rem; text-decoration: none; }
.hero-link:hover { color: var(--accent); }

.hero-art { position: relative; min-height: 430px; }
.art-label { position: absolute; color: var(--text-muted); font-size: 0.68rem; font-weight: 700; letter-spacing: 0.15em; }
.art-label--top { top: 0; right: 0; }

.art-frame {
  position: absolute;
  inset: 3rem 1rem 1.5rem 1rem;
  display: grid;
  place-items: center;
  border: 1px solid rgba(108, 232, 243, 0.35);
  background: rgba(255, 255, 255, 0.7);
  overflow: hidden;
}

.art-frame::before,
.art-frame::after { content: ''; position: absolute; background: var(--accent-pink); }
.art-frame::before { top: 30%; left: -8%; width: 30%; height: 1px; transform: rotate(-24deg); }
.art-frame::after { right: -8%; bottom: 23%; width: 34%; height: 1px; transform: rotate(-24deg); background: var(--accent-yellow); }
.art-image { position: relative; z-index: 2; width: min(72%, 295px); filter: saturate(1.25) drop-shadow(0 0 28px rgba(37, 116, 216, 0.18)); }
.art-corner { position: absolute; z-index: 3; width: 26px; height: 26px; border-color: var(--accent); border-style: solid; }
.art-corner--tl { top: 14px; left: 14px; border-width: 1px 0 0 1px; }
.art-corner--br { right: 14px; bottom: 14px; border-width: 0 1px 1px 0; }
.art-orbit { position: absolute; border: 1px solid rgba(255, 213, 106, 0.45); border-radius: 50%; transform: rotate(-25deg); }
.art-orbit--one { width: 54%; height: 25%; }
.art-orbit--two { width: 76%; height: 40%; border-color: rgba(255, 120, 188, 0.35); transform: rotate(35deg); }
.art-note { position: absolute; bottom: 0; left: 0; color: var(--text-secondary); font-size: 0.82rem; line-height: 1.6; }
.art-note span { margin-right: 0.5rem; color: var(--accent-yellow); font-size: 0.7rem; font-weight: 700; }

@media (max-width: 760px) {
  .hero { grid-template-columns: 1fr; min-height: auto; padding-top: 1.5rem; }
  .hero-art { min-height: 360px; margin-top: 1rem; }
  .art-frame { inset: 2.5rem 0.5rem 1.5rem; }
}

@media (max-width: 480px) {
  .hero-title { font-size: clamp(2.7rem, 15vw, 4rem); }
  .hero-art { min-height: 300px; }
  .art-image { width: 70%; }
}
</style>
