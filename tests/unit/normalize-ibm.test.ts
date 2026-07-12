import { test, expect } from 'vitest'
import { normalizeIbm } from '../../src/normalize/ibm'
import { ibmRaw } from '../fixtures/ibm'

test('groups confirmed violations by rule into the common shape', () => {
  const raw = ibmRaw

  const violations = normalizeIbm(raw)

  expect(violations).toEqual([
    {
      tool: 'ibm-equal-access',
      ruleId: 'img_alt_valid',
      wcag: [],
      description: 'Image alternative text is missing',
      count: 2,
      targets: ['/html[1]/body[1]/img[1]', '/html[1]/body[1]/img[2]'],
      helpUrl: 'https://example.test/rules/img_alt_valid',
    },
    {
      tool: 'ibm-equal-access',
      ruleId: 'a_text_purpose',
      wcag: [],
      description: 'Hyperlink has no link text',
      count: 1,
      targets: ['/html[1]/body[1]/a[1]'],
      helpUrl: 'https://example.test/rules/a_text_purpose',
    },
  ])
})
