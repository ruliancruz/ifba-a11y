import { test, expect } from 'vitest'
import { normalizeIbm, type IbmInput } from '../../collection/normalize/ibm'

test('groups confirmed violations by rule into the common shape', () => {
  const raw: IbmInput = {
    results: [
      {
        ruleId: 'img_alt_valid',
        level: 'violation',
        message: 'Image alternative text is missing',
        help: 'https://example.test/rules/img_alt_valid',
        path: { dom: '/html[1]/body[1]/img[1]' },
      },
      {
        ruleId: 'img_alt_valid',
        level: 'violation',
        message: 'Image alternative text is missing',
        help: 'https://example.test/rules/img_alt_valid',
        path: { dom: '/html[1]/body[1]/img[2]' },
      },
      {
        ruleId: 'a_text_purpose',
        level: 'violation',
        message: 'Hyperlink has no link text',
        help: 'https://example.test/rules/a_text_purpose',
        path: { dom: '/html[1]/body[1]/a[1]' },
      },
      {
        ruleId: 'aria_content_in_landmark',
        level: 'potentialviolation',
        message: 'Content is not within a landmark element',
        help: 'https://example.test/rules/aria_content_in_landmark',
        path: { dom: '/html[1]/body[1]/div[1]' },
      },
      {
        ruleId: 'html_lang_exists',
        level: 'pass',
        message: 'Page language is set',
        help: 'https://example.test/rules/html_lang_exists',
        path: { dom: '/html[1]' },
      },
    ],
  }

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
