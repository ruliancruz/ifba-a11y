import type { Page } from '@playwright/test'
import type { Target } from './config'

const LIVE_ATTEMPTS = 4
const LIVE_BACKOFF_MS = 4_000

const sleep = (ms: number): Promise<void> => new Promise((resolve) => setTimeout(resolve, ms))

async function gotoLive(page: Page, url: string): Promise<void> {
  for (let attempt = 1; ; attempt++) {
    try {
      await page.goto(url)
      return
    } catch (error) {
      if (attempt >= LIVE_ATTEMPTS) throw error
      await sleep(LIVE_BACKOFF_MS * 2 ** (attempt - 1))
    }
  }
}

export async function gotoTarget(page: Page, target: Target): Promise<void> {
  if (target.mode === 'live') {
    await gotoLive(page, target.url)
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
