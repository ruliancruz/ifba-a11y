import type { Page } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import { WCAG_TAGS } from '../config'

export function runAxe(page: Page) {
  return new AxeBuilder({ page }).withTags([...WCAG_TAGS]).analyze()
}
