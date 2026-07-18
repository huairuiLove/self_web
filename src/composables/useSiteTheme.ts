import { computed, readonly, ref, shallowRef, watch } from 'vue'
import { visualThemes, type VisualThemeName } from '../data/themes'

const storageKey = 'huairui-visual-theme'
function readStoredTheme(): VisualThemeName | null {
  if (typeof window === 'undefined') return null
  try {
    const value = window.localStorage.getItem(storageKey) as VisualThemeName | null
    return value && Object.hasOwn(visualThemes, value) ? value : null
  } catch {
    return null
  }
}

const currentTheme = shallowRef<VisualThemeName>(readStoredTheme() ?? 'sandrone')
const slideIndex = ref(0)

if (typeof window !== 'undefined') {
  watch(currentTheme, (name) => {
    try {
      window.localStorage.setItem(storageKey, name)
    } catch {
      // Private browsing may disable localStorage; theme selection still works for this session.
    }
  }, { immediate: true })
  window.setInterval(() => {
    const images = visualThemes[currentTheme.value].images
    if (images && images.length > 1) slideIndex.value = (slideIndex.value + 1) % images.length
  }, 10_000)
}

export function useSiteTheme() {
  const activeTheme = computed(() => visualThemes[currentTheme.value])
  const activeImage = computed(() => {
    const images = activeTheme.value.images ?? [activeTheme.value.image]
    return images[slideIndex.value % images.length]
  })
  const activeImageFit = computed(() => {
    const fits = activeTheme.value.imageFits
    return fits?.[slideIndex.value % fits.length] ?? 'cover'
  })
  const hasMultipleImages = computed(() => (activeTheme.value.images?.length ?? 1) > 1)

  function nextImage() {
    const length = activeTheme.value.images?.length ?? 1
    slideIndex.value = (slideIndex.value + 1) % length
  }

  function previousImage() {
    const length = activeTheme.value.images?.length ?? 1
    slideIndex.value = (slideIndex.value - 1 + length) % length
  }

  watch(currentTheme, () => {
    slideIndex.value = 0
  })

  function setTheme(name: VisualThemeName) {
    currentTheme.value = name
  }

  return {
    theme: readonly(currentTheme),
    activeTheme,
    activeImage,
    activeImageFit,
    hasMultipleImages,
    nextImage,
    previousImage,
    setTheme,
    themes: visualThemes,
  }
}
