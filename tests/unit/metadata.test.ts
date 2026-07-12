import { test, expect } from 'vitest'
import { buildMetadata } from '../../src/metadata'

test('assembles a self-contained metadata object including requested WCAG tags', () => {
  const context = {
    timestamp: '2026-05-14T12:00:00.000Z',
    url: 'https://portal.ifba.edu.br/',
    browser: 'chromium',
    browserVersion: '145.0.7632.6',
    viewport: { width: 1280, height: 720 },
    device: 'desktop',
    tool: 'axe-core' as const,
    toolVersion: '4.11.1',
    wcagTags: ['wcag2a', 'wcag22aa'],
  }

  const metadata = buildMetadata(context)

  expect(metadata).toEqual({
    timestamp: '2026-05-14T12:00:00.000Z',
    url: 'https://portal.ifba.edu.br/',
    browser: 'chromium',
    browserVersion: '145.0.7632.6',
    viewport: { width: 1280, height: 720 },
    device: 'desktop',
    tool: 'axe-core',
    toolVersion: '4.11.1',
    wcagTags: ['wcag2a', 'wcag22aa'],
  })
})

test('omits wcagTags when no tags are requested', () => {
  const context = {
    timestamp: '2026-05-14T12:00:00.000Z',
    url: 'https://portal.ifba.edu.br/',
    browser: 'chromium',
    browserVersion: '145.0.7632.6',
    viewport: { width: 375, height: 667 },
    device: 'mobile',
    tool: 'ibm-equal-access' as const,
    toolVersion: '4.0.14',
  }

  const metadata = buildMetadata(context)

  expect(metadata).not.toHaveProperty('wcagTags')
})
