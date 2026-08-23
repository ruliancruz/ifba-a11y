import { test } from '@playwright/test'
import type { Browser, Page } from '@playwright/test'
import * as fs from 'node:fs'
import { TARGETS, WCAG_TAGS } from '../collection/config'
import type { Target } from '../collection/config'
import { buildMetadata } from '../collection/metadata'
import { normalizeAxe } from '../collection/normalize/axe'
import { normalizeIbm } from '../collection/normalize/ibm'
import { runAxe } from '../collection/engines/axe'
import { runIbm } from '../collection/engines/ibm'
import type { MissingAsset } from '../collection/schema'
import { gotoTarget } from '../collection/navigate'
import { writeFidelity, writeResult } from '../collection/collect'

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

function trackMissingAssets(page: Page): MissingAsset[] {
  const missing: MissingAsset[] = []
  page.on('response', (response) => {
    if (response.status() >= 400) {
      missing.push({
        status: response.status(),
        resourceType: response.request().resourceType(),
        url: response.url(),
      })
    }
  })
  return missing
}

async function captureFidelity(page: Page, target: Target, missing: MissingAsset[], directory: string) {
  if (target.mode !== 'archive') return
  const stylesheets = await page.evaluate(() => document.styleSheets.length)
  writeFidelity(directory, { stylesheets, missingAssets: missing })
}

for (const target of TARGETS) {
  test(`Portal IFBA accessibility — ${target.label}`, async ({ page, browser }, testInfo) => {
    const directory = `${target.outDir}/${testInfo.project.name}`
    const missing = trackMissingAssets(page)
    await gotoTarget(page, target)
    await captureFidelity(page, target, missing, directory)

    const axeRaw = await runAxe(page)
    writeResult(directory, 'axe.json', {
      metadata: buildMetadata({
        ...executionContext(page, browser, testInfo.project.name),
        tool: 'axe-core',
        toolVersion: axeRaw.testEngine.version,
        wcagTags: WCAG_TAGS,
      }),
      violations: normalizeAxe(axeRaw),
      raw: axeRaw,
    })

    const ibmRaw = await runIbm(page, `portal-${target.label}-${testInfo.project.name}`)
    writeResult(directory, 'ibm.json', {
      metadata: buildMetadata({
        ...executionContext(page, browser, testInfo.project.name),
        tool: 'ibm-equal-access',
        toolVersion: IBM_VERSION,
      }),
      violations: normalizeIbm(ibmRaw),
      raw: ibmRaw,
    })
  })
}
