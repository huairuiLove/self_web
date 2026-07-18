export interface Project {
  id: string
  title: string
  summary: string
  description: string
  tags: string[]
  link?: string
  repo?: string
  year: string
  featured?: boolean
  gradient: string
}

export interface Post {
  id: string
  slug: string
  title: string
  excerpt: string
  content: string
  tags: string[]
  publishedAt: string
  readMinutes: number
}

export interface SiteProfile {
  name: string
  englishName: string
  title: string
  bio: string
  location: string
  email: string
  links: { label: string; href: string }[]
}
