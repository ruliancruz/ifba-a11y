import type { Page } from '@playwright/test'
import * as aChecker from 'accessibility-checker'

export async function runIbm(page: Page, label: string) {
  await aChecker.setConfig({ outputFormat: [] })
  const { report } = await aChecker.getCompliance(page, label)

  if (!('results' in report)) {
    throw new Error(`IBM Equal Access returned no report for ${label}`)
  }

  return report
}
