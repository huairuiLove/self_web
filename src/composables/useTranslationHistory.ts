import { readonly, shallowRef } from 'vue'

export interface TranslationHistoryEntry {
  id: string
  source: string
  translation: string
  mode: 'term' | 'academic'
  model: string
  createdAt: string
}

interface AddTranslationInput {
  source: string
  translation: string
  mode: TranslationHistoryEntry['mode']
  model: string
}

const storageKey = 'huairui-translation-history-v1'
const maxEntries = 60

function loadHistory(): TranslationHistoryEntry[] {
  if (typeof window === 'undefined') return []
  try {
    const raw = window.localStorage.getItem(storageKey)
    if (!raw) return []
    const parsed = JSON.parse(raw) as TranslationHistoryEntry[]
    return Array.isArray(parsed) ? parsed.slice(0, maxEntries) : []
  } catch {
    return []
  }
}

const entries = shallowRef<TranslationHistoryEntry[]>(loadHistory())

function persist() {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(storageKey, JSON.stringify(entries.value))
  } catch {
    // History is an optional local enhancement; translation still works without it.
  }
}

export function useTranslationHistory() {
  function findTranslation(source: string, mode: TranslationHistoryEntry['mode'], model: string) {
    return entries.value.find((entry) => entry.source === source && entry.mode === mode && entry.model === model)
  }

  function addTranslation(input: AddTranslationInput) {
    const duplicate = findTranslation(input.source, input.mode, input.model)
    const entry: TranslationHistoryEntry = {
      id: duplicate?.id ?? crypto.randomUUID(),
      ...input,
      createdAt: new Date().toISOString(),
    }
    entries.value = [entry, ...entries.value.filter((item) => item.id !== entry.id)].slice(0, maxEntries)
    persist()
    return entry
  }

  function removeTranslation(id: string) {
    entries.value = entries.value.filter((entry) => entry.id !== id)
    persist()
  }

  function clearHistory() {
    entries.value = []
    persist()
  }

  return {
    history: readonly(entries),
    findTranslation,
    addTranslation,
    removeTranslation,
    clearHistory,
  }
}
