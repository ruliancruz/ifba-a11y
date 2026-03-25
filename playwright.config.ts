import { defineConfig } from '@playwright/test'

const BROWSER = 'chromium'
const DESKTOP_VIEWPORT = { width: 1280, height: 720 }
const MOBILE_VIEWPORT = { width: 375, height: 667 }

export default defineConfig({
  testDir: './tests',
  reporter: [
    ['html', { outputFolder: 'reports/html' }],
    ['json', { outputFile: 'reports/results.json' }],
  ],
  projects: [
    {
      name: 'desktop',
      use: {
        browserName: BROWSER,
        viewport: DESKTOP_VIEWPORT,
      },
    },
    {
      name: 'mobile',
      use: {
        browserName: BROWSER,
        viewport: MOBILE_VIEWPORT,
      },
    },
  ],
})
