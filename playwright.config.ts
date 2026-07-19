import { defineConfig } from '@playwright/test'
import { VIEWPORTS } from './collection/config'

export default defineConfig({
  testDir: './tests',
  testMatch: '**/*.spec.ts',
  timeout: 90_000,
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
