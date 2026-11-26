import type { Target } from './config'

const MODES: readonly Target['mode'][] = ['live', 'archive']
const FIELDS = ['label', 'url', 'mode', 'outDir'] as const

// Validates a targets manifest (the parsed JSON of a TARGETS_FILE) and returns it
// in the Target shape. A study evaluates other pages by supplying its own
// manifest instead of editing TARGETS, so the instrument's code stays the same
// across studies and the manifest is the only thing that varies.
export function parseTargets(input: unknown): Target[] {
  if (!Array.isArray(input) || input.length === 0) {
    throw new Error('Targets manifest must be a non-empty array')
  }
  const targets = input.map(parseTarget)
  rejectDuplicates(targets, 'label')
  rejectDuplicates(targets, 'outDir')
  return targets
}

function parseTarget(entry: unknown, index: number): Target {
  if (typeof entry !== 'object' || entry === null || Array.isArray(entry)) {
    throw new Error(`Target ${index} must be an object`)
  }
  const record = entry as Record<string, unknown>
  for (const field of FIELDS) {
    const value = record[field]
    if (typeof value !== 'string' || value === '') {
      throw new Error(`Target ${index}: "${field}" must be a non-empty string`)
    }
  }
  const { label, url, mode, outDir } = record as Record<(typeof FIELDS)[number], string>
  if (!MODES.includes(mode as Target['mode'])) {
    throw new Error(`Target ${index}: "mode" must be "live" or "archive"`)
  }
  if (!isHttpUrl(url)) {
    throw new Error(`Target ${index}: "url" must be an http(s) URL`)
  }
  if (!isUnderResults(outDir)) {
    throw new Error(`Target ${index}: "outDir" must be a path under results/`)
  }
  return { label, url, mode: mode as Target['mode'], outDir }
}

function isHttpUrl(value: string): boolean {
  if (!URL.canParse(value)) return false
  const { protocol } = new URL(value)
  return protocol === 'http:' || protocol === 'https:'
}

// Results are written relative to the working directory, and the collection run
// mounts only results/, so anything outside it would be lost with the container.
function isUnderResults(value: string): boolean {
  const segments = value.split('/')
  return segments[0] === 'results' && segments.length > 1 && !segments.includes('..')
}

function rejectDuplicates(targets: Target[], field: 'label' | 'outDir'): void {
  const seen = new Set<string>()
  for (const target of targets) {
    if (seen.has(target[field])) throw new Error(`Duplicate target ${field}: ${target[field]}`)
    seen.add(target[field])
  }
}
