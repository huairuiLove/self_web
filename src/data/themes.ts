// Local copies keep the site reliable; replace these assets if redistribution rights are not available.
import sandroneBackground from '../assets/backgrounds/sandrone.png'
import columbinaBackground from '../assets/backgrounds/columbina.webp'
import fengjinBackground from '../assets/backgrounds/fengjin.jpg'
import fengjinPortraitBackground from '../assets/backgrounds/fengjin-portrait.jpg'

export type VisualThemeName = 'sandrone' | 'columbina' | 'fengjin'

export interface VisualTheme {
  name: VisualThemeName
  label: string
  subtitle: string
  image: string
  images?: string[]
  imageFits?: Array<'cover' | 'contain'>
  accent: string
}

export const visualThemes: Record<VisualThemeName, VisualTheme> = {
  sandrone: {
    name: 'sandrone',
    label: '桑多涅',
    subtitle: '机械 · 深蓝',
    image: sandroneBackground,
    accent: '#2574d8',
  },
  columbina: {
    name: 'columbina',
    label: '哥伦比娅',
    subtitle: '新月 · 冰蓝',
    image: columbinaBackground,
    accent: '#715bd8',
  },
  fengjin: {
    name: 'fengjin',
    label: '逢瑾',
    subtitle: '风堇·鲜花',
    image: fengjinBackground,
    images: [fengjinBackground, fengjinPortraitBackground],
    imageFits: ['cover', 'contain'],
    accent: '#d35c91',
  },
}
