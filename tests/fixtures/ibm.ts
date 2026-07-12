import type { IbmInput } from '../../src/normalize/ibm'

export const ibmRaw: IbmInput = {
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
