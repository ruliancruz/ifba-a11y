import type { Page } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import { WCAG_TAGS } from '../config'

export async function runAxe(page: Page) {
  const result = await new AxeBuilder({ page }).withTags([...WCAG_TAGS]).analyze()
  delete (result as { passes?: unknown }).passes
  return result
}
