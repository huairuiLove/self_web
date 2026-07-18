import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: () => import('../views/HomeView.vue'), meta: { title: '首页' } },
    { path: '/projects', name: 'projects', component: () => import('../views/ProjectsView.vue'), meta: { title: '项目' } },
    { path: '/projects/:id', name: 'project-detail', component: () => import('../views/ProjectDetailView.vue'), meta: { title: '项目详情' } },
    { path: '/posts', name: 'posts', component: () => import('../views/PostsView.vue'), meta: { title: '经验贴' } },
    { path: '/posts/:slug', name: 'post-detail', component: () => import('../views/PostDetailView.vue'), meta: { title: '文章' } },
    { path: '/papers', name: 'papers', component: () => import('../views/PapersView.vue'), meta: { title: '论文库' } },
    { path: '/papers/:slug', name: 'paper-detail', component: () => import('../views/PaperDetailView.vue'), meta: { title: '论文阅读' } },
    { path: '/about', name: 'about', component: () => import('../views/AboutView.vue'), meta: { title: '关于我' } },
  ],
  scrollBehavior(to) {
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0 }
  },
})

router.afterEach((to) => {
  const base = 'jinfeng · 个人作品集'
  const title = to.meta.title as string | undefined
  document.title = title && title !== '首页' ? `${title} · ${base}` : base
})

export default router
