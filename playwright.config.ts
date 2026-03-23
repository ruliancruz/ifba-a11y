import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  reporter: [
    ['html', { outputFolder: 'reports/html' }],
    ['json', { outputFile: 'reports/results.json' }],
  ],
})
