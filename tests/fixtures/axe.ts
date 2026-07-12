import type { AxeInput } from '../../src/normalize/axe'

export const axeRaw: AxeInput = {
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
