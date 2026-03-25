import { test } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import * as aChecker from 'accessibility-checker'
import fs from 'fs'

const WCAG_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']
const IBM_VERSION = (JSON.parse(
  fs.readFileSync(`${process.cwd()}/node_modules/accessibility-checker/package.json`, 'utf-8')
) as { version: string }).version

test.describe('AVA IFBA', () => {
  test('axe-core: homepage', async ({ page, browser }, testInfo) => {
    const outputDir = `results/ava/${testInfo.project.name}`
    fs.mkdirSync(outputDir, { recursive: true })

    await page.goto('https://ava.ifba.edu.br')

    const results = await new AxeBuilder({ page })
      .withTags(WCAG_TAGS)
      .analyze()

    fs.writeFileSync(
      `${outputDir}/axe.json`,
      JSON.stringify({
        metadata: {
          timestamp: new Date().toISOString(),
          url: page.url(),
          browser: browser.browserType().name(),
          browserVersion: browser.version(),
          viewport: page.viewportSize(),
          device: testInfo.project.name,
          tool: 'axe-core',
          toolVersion: results.testEngine.version,
          wcagTags: WCAG_TAGS,
        },
        violations: results.violations,
      }, null, 2)
    )

    console.log(`axe violations: ${results.violations.length}`)
  })

  test('IBM Equal Access: homepage', async ({ page, browser }, testInfo) => {
    const outputDir = `results/ava/${testInfo.project.name}`
    fs.mkdirSync(outputDir, { recursive: true })

    await page.goto('https://ava.ifba.edu.br')

    await aChecker.setConfig({ outputFormat: [] })
    const results = await aChecker.getCompliance(page, `ava-homepage-${testInfo.project.name}`)

    fs.writeFileSync(
      `${outputDir}/ibm.json`,
      JSON.stringify({
        metadata: {
          timestamp: new Date().toISOString(),
          url: page.url(),
          browser: browser.browserType().name(),
          browserVersion: browser.version(),
          viewport: page.viewportSize(),
          device: testInfo.project.name,
          tool: 'ibm-equal-access',
          toolVersion: IBM_VERSION,
        },
        report: results.report,
      }, null, 2)
    )

    const violations = results.report.results.filter(
      (r: { level: string }) => r.level === 'violation'
    )

    console.log(`IBM violations: ${violations.length}`)
  })
})
