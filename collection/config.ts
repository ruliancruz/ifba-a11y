export const PORTAL_ROOT_URL = 'https://portal.ifba.edu.br/'

export const HOMEPAGE_CAPTURE = '20260418162956'

export interface Target {
  label: string
  url: string
  mode: 'live' | 'archive'
  outDir: string
}

export const TARGETS: Target[] = [
  {
    label: 'homepage',
    url: `https://web.archive.org/web/${HOMEPAGE_CAPTURE}/${PORTAL_ROOT_URL}`,
    mode: 'archive',
    outDir: 'results/archive',
  },
  {
    label: 'live-root',
    url: PORTAL_ROOT_URL,
    mode: 'live',
    outDir: 'results/live',
  },
]

export const WCAG_TAGS = [
  'wcag2a',
  'wcag2aa',
  'wcag21a',
  'wcag21aa',
  'wcag22a',
  'wcag22aa',
] as const

export const VIEWPORTS = {
  desktop: { width: 1280, height: 720 },
  mobile: { width: 375, height: 667 },
} as const
