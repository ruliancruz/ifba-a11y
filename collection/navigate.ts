import type { Page } from '@playwright/test'
import type { Target } from './config'

export async function gotoTarget(page: Page, target: Target): Promise<void> {
  if (target.mode === 'live') {
    await page.goto(target.url)
    return
  }

  await page.route('**/*', async (route) => {
    if (route.request().url().includes('web-static.archive.org/_static/')) {
      await route.abort()
      return
    }
    await route.continue()
  })
  await page.goto(target.url, { waitUntil: 'networkidle' })
}
