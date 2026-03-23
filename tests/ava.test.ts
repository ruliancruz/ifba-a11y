import { test } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import * as aChecker from 'accessibility-checker'
import fs from 'fs'

const WCAG_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']
const OUTPUT_DIR = 'results/ava'

test.beforeAll(() => {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true })
})

test.describe('AVA IFBA', () => {
  test('axe-core: homepage', async ({ page }) => {
    await page.goto('https://ava.ifba.edu.br')

    const results = await new AxeBuilder({ page })
      .withTags(WCAG_TAGS)
      .analyze()

    fs.writeFileSync(
      `${OUTPUT_DIR}/axe.json`,
      JSON.stringify(results.violations, null, 2)
    )

    console.log(`axe violations: ${results.violations.length}`)
  })

  test('IBM Equal Access: homepage', async ({ page }) => {
    await page.goto('https://ava.ifba.edu.br')

    const results = await aChecker.getCompliance(page, 'ava-homepage')

    fs.writeFileSync(
      `${OUTPUT_DIR}/ibm.json`,
      JSON.stringify(results.report, null, 2)
    )

    const violations = results.report.results.filter(
      (r: { level: string }) => r.level === 'violation'
    )

    console.log(`IBM violations: ${violations.length}`)
  })
})
