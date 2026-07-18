// Local copies keep the site reliable; replace these assets if redistribution rights are not available.
import sandroneBackground from '../assets/backgrounds/sandrone.png'
import columbinaBackground from '../assets/backgrounds/columbina.webp'

export type VisualThemeName = 'sandrone' | 'columbina'

export interface VisualTheme {
  name: VisualThemeName
  label: string
  subtitle: string
  image: string
  accent: string
  backgroundPosition: string
}

export const visualThemes: Record<VisualThemeName, VisualTheme> = {
  sandrone: {
    name: 'sandrone',
    label: '桑多涅',
    subtitle: '机械 · 深蓝',
    image: sandroneBackground,
    accent: '#2574d8',
    backgroundPosition: 'center',
  },
  columbina: {
    name: 'columbina',
    label: '哥伦比娅',
    subtitle: '新月 · 冰蓝',
    image: columbinaBackground,
    accent: '#715bd8',
    backgroundPosition: 'center 35%',
  },
}
