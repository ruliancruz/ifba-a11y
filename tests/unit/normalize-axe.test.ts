import { test, expect } from 'vitest'
import { normalizeAxe, type AxeInput } from '../../collection/normalize/axe'

test('maps each axe rule to the common violation shape', () => {
  const raw: AxeInput = {
    violations: [
      {
        id: 'image-alt',
        impact: 'critical',
        description: 'Images must have alternate text',
        helpUrl: 'https://example.test/rules/image-alt',
        tags: ['cat.text-alternatives', 'wcag2a', 'wcag111', 'ACT'],
        nodes: [{ target: ['img.logo'] }, { target: ['#hero > img'] }],
      },
      {
        id: 'color-contrast',
        impact: 'serious',
        description: 'Elements must meet minimum color contrast ratio thresholds',
        helpUrl: 'https://example.test/rules/color-contrast',
        tags: ['cat.color', 'wcag2aa', 'wcag143'],
        nodes: [{ target: ['a.tile-footer'] }, { target: ['#modal', 'button.close'] }],
      },
    ],
  }

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
