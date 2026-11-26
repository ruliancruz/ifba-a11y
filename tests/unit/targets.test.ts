import { test, expect } from 'vitest'
import { parseTargets } from '../../collection/targets'

test('accepts a manifest of live and archive targets unchanged', () => {
  const manifest = [
    {
      label: 'ead',
      url: 'https://portal.ifba.edu.br/ead',
      mode: 'live',
      outDir: 'results/ead',
    },
    {
      label: 'homepage',
      url: 'https://web.archive.org/web/20260418162956/https://portal.ifba.edu.br/',
      mode: 'archive',
      outDir: 'results/archive',
    },
  ]

  const targets = parseTargets(manifest)

  expect(targets).toEqual(manifest)
})

test('drops fields the target shape does not declare', () => {
  const manifest = [
    {
      label: 'ead',
      url: 'https://portal.ifba.edu.br/ead',
      mode: 'live',
      outDir: 'results/ead',
      note: 'public EaD area',
    },
  ]

  const targets = parseTargets(manifest)

  expect(targets).toEqual([
    { label: 'ead', url: 'https://portal.ifba.edu.br/ead', mode: 'live', outDir: 'results/ead' },
  ])
})

test('rejects a manifest that is not a non-empty array', () => {
  const notArray = { label: 'ead' }
  const empty: unknown[] = []

  const parsing = [() => parseTargets(notArray), () => parseTargets(empty)]

  for (const parse of parsing) expect(parse).toThrow('non-empty array')
})

test('rejects an entry that is not an object', () => {
  const manifest = ['https://portal.ifba.edu.br/ead']

  const parse = () => parseTargets(manifest)

  expect(parse).toThrow('Target 0 must be an object')
})

test('rejects an entry with a missing or empty field', () => {
  const manifest = [{ label: '', url: 'https://portal.ifba.edu.br/ead', mode: 'live' }]

  const parse = () => parseTargets(manifest)

  expect(parse).toThrow('Target 0: "label" must be a non-empty string')
})

test('rejects a mode other than live or archive', () => {
  const manifest = [
    { label: 'ead', url: 'https://portal.ifba.edu.br/ead', mode: 'cached', outDir: 'results/ead' },
  ]

  const parse = () => parseTargets(manifest)

  expect(parse).toThrow('Target 0: "mode" must be "live" or "archive"')
})

test('rejects a url that is not http or https', () => {
  const invalid = ['file:///etc/passwd', 'not a url']

  const parsing = invalid.map(
    (url) => () => parseTargets([{ label: 'ead', url, mode: 'live', outDir: 'results/ead' }]),
  )

  for (const parse of parsing) expect(parse).toThrow('Target 0: "url" must be an http(s) URL')
})

test('rejects an outDir outside results/', () => {
  const outside = ['reports/ead', 'results/../ead', '/app/results/ead', 'results']

  const parsing = outside.map(
    (outDir) => () =>
      parseTargets([{ label: 'ead', url: 'https://portal.ifba.edu.br/ead', mode: 'live', outDir }]),
  )

  for (const parse of parsing) expect(parse).toThrow('Target 0: "outDir" must be a path under results/')
})

test('rejects duplicate labels', () => {
  const manifest = [
    { label: 'ead', url: 'https://portal.ifba.edu.br/ead', mode: 'live', outDir: 'results/ead' },
    { label: 'ead', url: 'https://portal.ifba.edu.br/ead/uab', mode: 'live', outDir: 'results/uab' },
  ]

  const parse = () => parseTargets(manifest)

  expect(parse).toThrow('Duplicate target label: ead')
})

test('rejects duplicate output directories', () => {
  const manifest = [
    { label: 'ead', url: 'https://portal.ifba.edu.br/ead', mode: 'live', outDir: 'results/ead' },
    { label: 'uab', url: 'https://portal.ifba.edu.br/ead/uab', mode: 'live', outDir: 'results/ead' },
  ]

  const parse = () => parseTargets(manifest)

  expect(parse).toThrow('Duplicate target outDir: results/ead')
})
