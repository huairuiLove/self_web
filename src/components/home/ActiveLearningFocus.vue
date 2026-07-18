<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { activeLearningFocus, researchQuestions } from '../../data/research'
</script>

<template>
  <section class="focus" aria-labelledby="research-focus-heading">
    <div class="focus-intro">
      <div class="focus-heading">
        <p class="focus-kicker">CURRENT RESEARCH / NOW</p>
        <h2 id="research-focus-heading" class="focus-title">{{ activeLearningFocus.title }}</h2>
      </div>
      <p class="focus-summary">{{ activeLearningFocus.summary }}</p>
    </div>

    <div class="focus-loop" aria-label="主动学习闭环">
      <p class="loop-definition">{{ activeLearningFocus.definition }}</p>
      <ol class="loop-steps">
        <li v-for="(step, index) in activeLearningFocus.loop" :key="step" class="loop-step">
          <span class="step-index">0{{ index + 1 }}</span>
          <span>{{ step }}</span>
        </li>
      </ol>
    </div>

    <div class="question-grid">
      <article v-for="question in researchQuestions" :key="question.index" class="question">
        <p class="question-index">{{ question.index }}</p>
        <h3 class="question-title">{{ question.title }}</h3>
        <p class="question-note">{{ question.note }}</p>
      </article>
    </div>

    <div class="focus-footer">
      <p class="focus-reminder">给自己的判断标准：先问是否真的减少专家成本，再问是否提高指标。</p>
      <RouterLink to="/papers" class="focus-link">查看主动学习阅读清单 <span aria-hidden="true">↗</span></RouterLink>
    </div>
  </section>
</template>

<style scoped>
.focus {
  margin-bottom: 4.5rem;
  padding: 3rem 0 2.5rem;
  border-top: 1px solid var(--border-strong);
  border-bottom: 1px solid var(--border-strong);
}

.focus-intro {
  display: grid;
  grid-template-columns: minmax(220px, 0.72fr) minmax(0, 1.28fr);
  gap: clamp(2rem, 6vw, 5rem);
  align-items: start;
}

.focus-kicker,
.question-index {
  margin: 0 0 0.55rem;
  color: var(--accent-pink);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.14em;
}

.focus-title {
  max-width: 18rem;
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.85rem;
  font-weight: 600;
  line-height: 1.45;
}

.focus-summary {
  max-width: 45rem;
  margin: 0;
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.9;
}

.focus-loop {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(320px, 1fr);
  gap: clamp(2rem, 5vw, 4rem);
  margin: 2.5rem 0;
  padding: 1.4rem 0;
  border-top: 1px solid var(--border-subtle);
  border-bottom: 1px solid var(--border-subtle);
}

.loop-definition {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.8;
}

.loop-steps {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0;
  margin: 0;
  padding: 0;
  list-style: none;
}

.loop-step {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
  padding: 0 0.65rem;
  color: var(--text-primary);
  font-size: 0.78rem;
  line-height: 1.45;
}

.loop-step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 0.65rem;
  right: -2px;
  width: 5px;
  height: 5px;
  border-top: 1px solid var(--accent);
  border-right: 1px solid var(--accent);
  transform: rotate(45deg);
}

.step-index { color: var(--accent-strong); font-size: 0.65rem; font-weight: 700; }

.question-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0;
}

.question {
  min-width: 0;
  padding: 0.4rem clamp(1rem, 3vw, 2rem);
  border-left: 1px solid var(--border-subtle);
}

.question:first-child { padding-left: 0; border-left: 0; }
.question:last-child { padding-right: 0; }
.question-title { margin: 0 0 0.55rem; font-family: var(--font-display); font-size: 1.05rem; }
.question-note { margin: 0; color: var(--text-secondary); font-size: 0.85rem; line-height: 1.75; }

.focus-footer {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 2.25rem;
}

.focus-reminder { margin: 0; color: var(--text-muted); font-size: 0.82rem; }
.focus-link { color: var(--accent-strong); font-size: 0.85rem; font-weight: 700; text-decoration: none; }
.focus-link:hover { color: var(--accent-pink); }

@media (max-width: 760px) {
  .focus-intro,
  .focus-loop { grid-template-columns: 1fr; gap: 1.25rem; }
  .focus-title { max-width: none; }
  .question-grid { grid-template-columns: 1fr; }
  .question,
  .question:first-child,
  .question:last-child { padding: 1.25rem 0; border-top: 1px solid var(--border-subtle); border-left: 0; }
}

@media (max-width: 480px) {
  .focus { padding-top: 2.25rem; }
  .loop-steps { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 1.25rem; }
  .loop-step:nth-child(2)::after { display: none; }
}
</style>
