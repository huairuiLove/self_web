import { computed, readonly, shallowRef, watch } from 'vue'
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

if (typeof window !== 'undefined') {
  watch(currentTheme, (name) => {
    try {
      window.localStorage.setItem(storageKey, name)
    } catch {
      // Private browsing may disable localStorage; theme selection still works for this session.
    }
  }, { immediate: true })
}

export function useSiteTheme() {
  const activeTheme = computed(() => visualThemes[currentTheme.value])

  function setTheme(name: VisualThemeName) {
    currentTheme.value = name
  }

  return {
    theme: readonly(currentTheme),
    activeTheme,
    setTheme,
    themes: visualThemes,
  }
}
