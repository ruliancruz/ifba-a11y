import { test } from '@playwright/test'
import type { Browser, Page } from '@playwright/test'
import * as fs from 'node:fs'
import { TARGET_URL, WCAG_TAGS } from '../src/config'
import { buildMetadata } from '../src/metadata'
import { normalizeAxe } from '../src/normalize/axe'
import { normalizeIbm } from '../src/normalize/ibm'
import { runAxe } from '../src/engines/axe'
import { runIbm } from '../src/engines/ibm'
import { writeResult } from '../src/collect'

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
