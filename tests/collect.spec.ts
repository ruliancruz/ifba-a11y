import { test } from '@playwright/test'
import type { Browser, Page } from '@playwright/test'
import * as fs from 'node:fs'
import { TARGET_URL, WCAG_TAGS } from '../collection/config'
import { buildMetadata } from '../collection/metadata'
import { normalizeAxe } from '../collection/normalize/axe'
import { normalizeIbm } from '../collection/normalize/ibm'
import { runAxe } from '../collection/engines/axe'
import { runIbm } from '../collection/engines/ibm'
import { writeResult } from '../collection/collect'

const IBM_VERSION = (
  JSON.parse(
    fs.readFileSync(`${process.cwd()}/node_modules/accessibility-checker/package.json`, 'utf-8'),
  ) as { version: string }
).version

function executionContext(page: Page, browser: Browser, device: string) {
  return {
    timestamp: new Date().toISOString(),
    url: page.url(),
    browser: browser.browserType().name(),
    browserVersion: browser.version(),
    viewport: page.viewportSize(),
    device,
  }
}

test.describe('Portal IFBA accessibility', () => {
  test('axe-core', async ({ page, browser }, testInfo) => {
    await page.goto(TARGET_URL)
    const raw = await runAxe(page)

    writeResult(`results/${testInfo.project.name}`, 'axe.json', {
      metadata: buildMetadata({
        ...executionContext(page, browser, testInfo.project.name),
        tool: 'axe-core',
        toolVersion: raw.testEngine.version,
        wcagTags: WCAG_TAGS,
      }),
      violations: normalizeAxe(raw),
      raw,
    })
  })

  test('IBM Equal Access', async ({ page, browser }, testInfo) => {
    await page.goto(TARGET_URL)
    const raw = await runIbm(page, `portal-${testInfo.project.name}`)

    writeResult(`results/${testInfo.project.name}`, 'ibm.json', {
      metadata: buildMetadata({
        ...executionContext(page, browser, testInfo.project.name),
        tool: 'ibm-equal-access',
        toolVersion: IBM_VERSION,
      }),
      violations: normalizeIbm(raw),
      raw,
    })
  })
})
