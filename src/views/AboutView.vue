<script setup lang="ts">
import { computed, ref } from 'vue'

interface LifePost {
  id: string
  title: string
  body: string
  date: string
  images: string[]
  group: string
}

const storageKey = 'fengjin-life-posts'
const title = ref('')
const body = ref('')
const group = ref('日常')
const images = ref<string[]>([])
const error = ref('')
const posts = ref<LifePost[]>(loadPosts())
const selectedGroup = ref('全部')
const searchQuery = ref('')
const groups = computed(() => ['全部', ...Array.from(new Set(posts.value.map((post) => post.group || '未分组')))])
const visiblePosts = computed(() => {
  const query = searchQuery.value.trim().toLocaleLowerCase()
  return posts.value.filter((post) => {
    const matchesGroup = selectedGroup.value === '全部' || (post.group || '未分组') === selectedGroup.value
    const searchableText = `${post.title} ${post.body} ${post.group || '未分组'}`.toLocaleLowerCase()
    return matchesGroup && (!query || searchableText.includes(query))
  })
})

function loadPosts(): LifePost[] {
  try {
    const saved = localStorage.getItem(storageKey)
    const parsed = saved ? JSON.parse(saved) as LifePost[] : []
    return parsed.map((post) => ({ ...post, group: post.group || '未分组' }))
  } catch {
    return []
  }
}

function chooseImages(event: Event) {
  error.value = ''
  const input = event.target as HTMLInputElement
  const files = Array.from(input.files ?? [])
  if (files.some((file) => file.size > 2 * 1024 * 1024)) {
    error.value = '单张照片请控制在 2MB 以内。'
    input.value = ''
    return
  }
  Promise.all(files.slice(0, 6).map(readImage)).then((result) => {
    images.value = [...images.value, ...result].slice(0, 6)
    input.value = ''
  })
}

function readImage(file: File) {
  return new Promise<string>((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(String(reader.result))
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

function removePreview(index: number) {
  images.value.splice(index, 1)
}

function publish() {
  error.value = ''
  if (!title.value.trim() && !body.value.trim() && images.value.length === 0) {
    error.value = '写一点内容或添加照片后再发布。'
    return
  }

  const post: LifePost = {
    id: crypto.randomUUID(),
    title: title.value.trim(),
    body: body.value.trim(),
    date: new Intl.DateTimeFormat('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' }).format(new Date()),
    images: [...images.value],
    group: group.value.trim() || '未分组',
  }
  posts.value.unshift(post)
  try {
    localStorage.setItem(storageKey, JSON.stringify(posts.value))
    title.value = ''
    body.value = ''
    images.value = []
    selectedGroup.value = '全部'
  } catch {
    posts.value.shift()
    error.value = '照片占用空间过大，请减少图片数量或压缩后重试。'
  }
}

function deletePost(id: string) {
  posts.value = posts.value.filter((post) => post.id !== id)
  localStorage.setItem(storageKey, JSON.stringify(posts.value))
  if (!groups.value.includes(selectedGroup.value)) selectedGroup.value = '全部'
}

const resumeStorageKey = 'fengjin-resume'
const resume = ref<{ name: string; data: string; date: string } | null>(loadResume())
const resumeError = ref('')

function loadResume() {
  try {
    const saved = localStorage.getItem(resumeStorageKey)
    return saved ? JSON.parse(saved) : null
  } catch {
    return null
  }
}

function chooseResume(event: Event) {
  resumeError.value = ''
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  if (file.type !== 'application/pdf') {
    resumeError.value = '请上传 PDF 格式的简历。'
    input.value = ''
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    resumeError.value = '简历文件请控制在 5MB 以内。'
    input.value = ''
    return
  }
  readImage(file).then((data) => {
    const next = { name: file.name, data, date: new Date().toLocaleDateString('zh-CN') }
    try {
      localStorage.setItem(resumeStorageKey, JSON.stringify(next))
      resume.value = next
    } catch {
      resumeError.value = '文件占用空间过大，请压缩后重试。'
    }
    input.value = ''
  })
}

function clearResume() {
  resume.value = null
  localStorage.removeItem(resumeStorageKey)
}
</script>

<template>
  <div class="about-page">
    <header class="page-header">
      <p class="page-kicker">LIFE NOTES / 04</p>
      <h1>关于我</h1>
      <p>嗨！好久不见！</p>
    </header>

    <section class="composer" aria-labelledby="composer-title">
      <div class="composer-heading">
        <div>
          <p class="eyebrow">NEW MOMENT</p>
          <h2 id="composer-title">发布生活动态</h2>
        </div>
        <span class="draft-status">仅保存在当前浏览器</span>
      </div>

      <input v-model="title" class="title-input" type="text" maxlength="60" placeholder="给今天起个标题" aria-label="动态标题" />
      <div class="group-field">
        <label for="life-group">分组</label>
        <input id="life-group" v-model="group" type="text" maxlength="20" list="life-groups" placeholder="例如：旅行、摄影、日常" />
        <datalist id="life-groups">
          <option v-for="item in groups.filter((item) => item !== '全部')" :key="item" :value="item" />
        </datalist>
      </div>
      <textarea v-model="body" rows="5" maxlength="1000" placeholder="写下今天发生的事……" aria-label="动态正文" />

      <div v-if="images.length" class="preview-grid">
        <figure v-for="(image, index) in images" :key="image" class="preview">
          <img :src="image" :alt="`待发布照片 ${index + 1}`" />
          <button type="button" class="remove-image" :aria-label="`移除第 ${index + 1} 张照片`" title="移除照片" @click="removePreview(index)">×</button>
        </figure>
      </div>

      <p v-if="error" class="error" role="alert">{{ error }}</p>
      <div class="composer-actions">
        <label class="image-picker">
          <input type="file" accept="image/*" multiple @change="chooseImages" />
          <span aria-hidden="true">＋</span> 添加照片
        </label>
        <span class="image-limit">最多 6 张，每张不超过 2MB</span>
        <button type="button" class="publish" @click="publish">发布动态</button>
      </div>
    </section>

    <section class="resume-section" aria-labelledby="resume-title">
      <div class="resume-copy">
        <p class="eyebrow">AVAILABLE FOR DOWNLOAD</p>
        <h2 id="resume-title">我的简历</h2>
        <p>想进一步了解我的经历与能力，可以下载最新简历。</p>
      </div>
      <div v-if="resume" class="resume-file">
        <span class="file-icon" aria-hidden="true">PDF</span>
        <div class="file-info"><strong>{{ resume.name }}</strong><small>更新于 {{ resume.date }}</small></div>
        <a class="download-resume" :href="resume.data" :download="resume.name">下载</a>
        <button type="button" class="clear-resume" title="移除简历" @click="clearResume">移除</button>
      </div>
      <div v-else class="resume-empty">暂未上传简历</div>
      <label class="resume-picker">
        <input type="file" accept="application/pdf,.pdf" @change="chooseResume" />
        <span aria-hidden="true">＋</span> {{ resume ? '替换简历' : '上传简历' }}
      </label>
      <p v-if="resumeError" class="error" role="alert">{{ resumeError }}</p>
      <p class="resume-note">PDF 格式，最大 5MB。文件保存在当前浏览器中。</p>
    </section>

    <section class="feed" aria-labelledby="feed-title">
      <div class="feed-heading">
        <p class="eyebrow">RECENT DAYS</p>
        <h2 id="feed-title">生活片段</h2>
      </div>

      <div v-if="posts.length" class="life-search">
        <label for="life-search-input">搜索动态</label>
        <div class="search-control">
          <span aria-hidden="true">⌕</span>
          <input id="life-search-input" v-model="searchQuery" type="search" placeholder="搜索标题、正文或分组" />
          <button v-if="searchQuery" type="button" title="清空搜索" aria-label="清空搜索" @click="searchQuery = ''">×</button>
        </div>
      </div>

      <div v-if="posts.length" class="group-filters" aria-label="生活动态分组">
        <button
          v-for="item in groups"
          :key="item"
          type="button"
          :class="{ 'group-filter--active': selectedGroup === item }"
          @click="selectedGroup = item"
        >{{ item }}</button>
      </div>

      <div v-if="visiblePosts.length" class="post-list">
        <article v-for="post in visiblePosts" :key="post.id" class="life-post">
          <div class="post-meta">
            <div><time>{{ post.date }}</time><span class="post-group">{{ post.group || '未分组' }}</span></div>
            <button type="button" class="delete-post" title="删除动态" @click="deletePost(post.id)">删除</button>
          </div>
          <h3 v-if="post.title">{{ post.title }}</h3>
          <p v-if="post.body" class="post-body">{{ post.body }}</p>
          <div v-if="post.images.length" class="photo-grid" :class="`photo-grid--${Math.min(post.images.length, 3)}`">
            <img v-for="(image, index) in post.images" :key="image" :src="image" :alt="`${post.title || '生活动态'}照片 ${index + 1}`" />
          </div>
        </article>
      </div>
      <div v-else class="empty-state">
        <span class="empty-number">04</span>
        <p>{{ posts.length ? (searchQuery ? '没有找到匹配的生活动态。' : '这个分组暂时没有生活动态。') : '第一条生活动态，正在等你写下。' }}</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-page { max-width: 900px; margin: 0 auto; }
.page-header { max-width: 42rem; margin-bottom: 2.25rem; }
.page-kicker, .eyebrow { margin: 0 0 0.55rem; color: var(--accent-pink); font-size: 0.68rem; font-weight: 700; letter-spacing: 0.14em; }
.page-header h1 { margin: 0 0 0.75rem; font-family: var(--font-display); font-size: clamp(2.3rem, 6vw, 4.4rem); font-weight: 600; line-height: 1.05; }
.page-header > p:last-child { margin: 0; color: var(--text-secondary); line-height: 1.8; }
.composer { padding: clamp(1rem, 3vw, 1.75rem); border: 1px solid var(--border-subtle); border-radius: 8px; background: color-mix(in srgb, var(--surface-elevated) 82%, transparent); box-shadow: 8px 8px 0 color-mix(in srgb, var(--accent) 12%, transparent); }
.composer-heading, .composer-actions, .post-meta { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.composer-heading { margin-bottom: 1rem; }
.composer h2, .feed h2 { margin: 0; font-family: var(--font-display); font-size: 1.35rem; }
.draft-status, .image-limit { color: var(--text-muted); font-size: 0.72rem; }
.title-input, textarea { width: 100%; border: 0; border-bottom: 1px solid var(--border-subtle); border-radius: 0; color: var(--text-primary); background: transparent; font: inherit; outline: none; }
.title-input { padding: 0.8rem 0; font-family: var(--font-display); font-size: 1.25rem; font-weight: 600; }
.group-field { display: flex; align-items: center; gap: 0.65rem; padding: 0.7rem 0; border-bottom: 1px solid var(--border-subtle); }
.group-field label { color: var(--text-muted); font-size: 0.76rem; font-weight: 700; }
.group-field input { min-width: 0; flex: 1; border: 0; color: var(--text-primary); background: transparent; font: inherit; outline: none; }
textarea { display: block; resize: vertical; padding: 1rem 0; line-height: 1.75; }
.title-input:focus, textarea:focus { border-color: var(--accent); }
.preview-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.65rem; margin-top: 1rem; }
.preview { position: relative; aspect-ratio: 4 / 3; margin: 0; overflow: hidden; border-radius: 6px; background: var(--surface-hover); }
.preview img, .photo-grid img { width: 100%; height: 100%; object-fit: cover; }
.remove-image { position: absolute; top: 0.4rem; right: 0.4rem; display: grid; width: 28px; height: 28px; place-items: center; padding: 0; border: 0; border-radius: 50%; color: white; background: rgba(8, 10, 19, 0.78); cursor: pointer; font-size: 1.15rem; }
.composer-actions { margin-top: 1rem; }
.image-picker, .publish { border: 1px solid var(--border-subtle); border-radius: 6px; cursor: pointer; font: inherit; font-size: 0.82rem; font-weight: 600; }
.image-picker { padding: 0.58rem 0.75rem; color: var(--text-secondary); background: var(--surface-elevated); }
.image-picker input { position: absolute; width: 1px; height: 1px; opacity: 0; }
.publish { margin-left: auto; padding: 0.62rem 1rem; border-color: var(--accent); color: var(--bg-base); background: var(--accent); }
.error { margin: 0.8rem 0 0; color: var(--accent-pink); font-size: 0.82rem; }
.feed { margin-top: 4rem; }
.feed-heading { margin-bottom: 1.25rem; }
.life-search { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.8rem; }
.life-search > label { color: var(--text-muted); font-size: 0.74rem; font-weight: 700; white-space: nowrap; }
.search-control { display: flex; min-width: min(100%, 24rem); align-items: center; gap: 0.45rem; flex: 1; padding: 0.5rem 0.65rem; border: 1px solid var(--border-subtle); border-radius: 6px; color: var(--text-muted); background: var(--surface-elevated); }
.search-control:focus-within { border-color: var(--accent); }
.search-control input { min-width: 0; flex: 1; border: 0; color: var(--text-primary); background: transparent; outline: none; font: inherit; font-size: 0.8rem; }
.search-control button { display: grid; width: 22px; height: 22px; place-items: center; padding: 0; border: 0; border-radius: 50%; color: var(--text-muted); background: transparent; cursor: pointer; font-size: 1rem; }
.search-control button:hover { color: var(--accent-pink); background: var(--surface-hover); }
.group-filters { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem; }
.group-filters button { padding: 0.45rem 0.72rem; border: 1px solid var(--border-subtle); border-radius: 6px; color: var(--text-secondary); background: var(--surface-elevated); cursor: pointer; font: inherit; font-size: 0.76rem; }
.group-filters button:hover, .group-filters .group-filter--active { color: var(--bg-base); border-color: var(--accent); background: var(--accent); }
.post-list { display: grid; gap: 2.5rem; }
.life-post { padding-top: 1.25rem; border-top: 1px solid var(--border-subtle); }
.post-meta { color: var(--text-muted); font-size: 0.75rem; }
.post-meta > div { display: flex; align-items: center; gap: 0.6rem; }
.post-group { padding: 0.18rem 0.42rem; border: 1px solid var(--border-subtle); border-radius: 4px; color: var(--accent-strong); background: var(--surface-elevated); font-size: 0.68rem; }
.delete-post { border: 0; color: var(--text-muted); background: transparent; cursor: pointer; font: inherit; }
.delete-post:hover { color: var(--accent-pink); }
.life-post h3 { margin: 0.8rem 0 0.45rem; font-family: var(--font-display); font-size: clamp(1.3rem, 3vw, 1.8rem); }
.post-body { margin: 0 0 1rem; color: var(--text-secondary); white-space: pre-wrap; line-height: 1.8; }
.photo-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.45rem; }
.photo-grid img { aspect-ratio: 1 / 1; border-radius: 5px; }
.photo-grid--1 { grid-template-columns: minmax(0, 36rem); }
.photo-grid--1 img { aspect-ratio: 16 / 10; }
.photo-grid--2 { grid-template-columns: repeat(2, 1fr); }
.empty-state { display: flex; min-height: 180px; align-items: center; justify-content: center; gap: 1.25rem; border-top: 1px solid var(--border-subtle); border-bottom: 1px solid var(--border-subtle); color: var(--text-muted); }
.empty-number { color: var(--accent); font-family: var(--font-display); font-size: 3rem; }
.resume-section { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 1rem 2rem; align-items: center; margin-top: 4rem; padding: clamp(1.1rem, 3vw, 1.75rem) 0; border-top: 1px solid var(--border-subtle); border-bottom: 1px solid var(--border-subtle); }
.resume-copy h2 { margin: 0; font-family: var(--font-display); font-size: 1.6rem; }
.resume-copy > p:last-child { margin: 0.55rem 0 0; color: var(--text-secondary); line-height: 1.7; }
.resume-file { grid-column: 1 / -1; display: flex; align-items: center; gap: 0.85rem; padding: 0.85rem; border: 1px solid var(--border-subtle); border-radius: 6px; background: var(--surface-elevated); }
.file-icon { display: grid; width: 44px; height: 44px; place-items: center; flex: 0 0 auto; border-radius: 5px; color: var(--bg-base); background: var(--accent-pink); font-size: 0.68rem; font-weight: 800; letter-spacing: 0.08em; }
.file-info { display: grid; min-width: 0; gap: 0.25rem; }
.file-info strong { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.9rem; }
.file-info small, .resume-note, .resume-empty { color: var(--text-muted); font-size: 0.74rem; }
.download-resume, .resume-picker { padding: 0.58rem 0.78rem; border: 1px solid var(--accent); border-radius: 6px; color: var(--bg-base); background: var(--accent); cursor: pointer; font-size: 0.8rem; font-weight: 700; text-decoration: none; }
.download-resume { margin-left: auto; }
.resume-picker { grid-column: 2; grid-row: 1; align-self: end; }
.resume-picker input { position: absolute; width: 1px; height: 1px; opacity: 0; }
.clear-resume { padding: 0.45rem; border: 0; color: var(--text-muted); background: transparent; cursor: pointer; font: inherit; font-size: 0.76rem; }
.clear-resume:hover { color: var(--accent-pink); }
.resume-note { grid-column: 1 / -1; margin: 0; }
@media (max-width: 760px) { .composer-heading { align-items: flex-start; flex-direction: column; } .composer-actions { align-items: flex-start; flex-wrap: wrap; } .image-limit { order: 3; width: 100%; } .preview-grid { grid-template-columns: repeat(2, 1fr); } .photo-grid { grid-template-columns: repeat(2, 1fr); } .resume-section { grid-template-columns: 1fr; } .resume-picker { grid-column: 1; grid-row: auto; width: fit-content; } .resume-file { flex-wrap: wrap; } .download-resume { margin-left: 0; } .life-search { align-items: flex-start; flex-direction: column; } .search-control { width: 100%; } }
</style>
