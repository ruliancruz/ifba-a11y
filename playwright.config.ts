import { defineConfig } from '@playwright/test'
import { VIEWPORTS } from './src/config'

export default defineConfig({
  testDir: './tests',
  testMatch: '**/*.spec.ts',
  retries: 2,
  reporter: [
    ['html', { outputFolder: 'reports/html' }],
    ['json', { outputFile: 'reports/results.json' }],
  ],
  projects: Object.entries(VIEWPORTS).map(([name, viewport]) => ({
    name,
    use: { browserName: 'chromium', viewport },
  })),
})
