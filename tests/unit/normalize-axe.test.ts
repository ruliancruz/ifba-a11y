import { test, expect } from 'vitest'
import { normalizeAxe } from '../../src/normalize/axe'
import { axeRaw } from '../fixtures/axe'

test('maps each axe rule to the common violation shape', () => {
  const raw = axeRaw

  const violations = normalizeAxe(raw)

  expect(violations).toEqual([
    {
      tool: 'axe-core',
      ruleId: 'image-alt',
      wcag: ['1.1.1'],
      description: 'Images must have alternate text',
      count: 2,
      targets: ['img.logo', '#hero > img'],
      impact: 'critical',
      helpUrl: 'https://example.test/rules/image-alt',
    },
    {
      tool: 'axe-core',
      ruleId: 'color-contrast',
      wcag: ['1.4.3'],
      description: 'Elements must meet minimum color contrast ratio thresholds',
      count: 2,
      targets: ['a.tile-footer', '#modal button.close'],
      impact: 'serious',
      helpUrl: 'https://example.test/rules/color-contrast',
    },
  ])
})
