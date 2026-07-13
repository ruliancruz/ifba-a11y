import type { Violation } from '../schema'

interface IbmResult {
  ruleId: string
  level: string
  message: string
  help: string
  path: { dom?: string }
}

export interface IbmInput {
  results: IbmResult[]
}

export function normalizeIbm(raw: IbmInput): Violation[] {
  const confirmed = raw.results.filter((result) => result.level === 'violation')
  const byRule = new Map<string, IbmResult[]>()

  for (const result of confirmed) {
    const group = byRule.get(result.ruleId) ?? []
    group.push(result)
    byRule.set(result.ruleId, group)
  }

  return [...byRule].map(([ruleId, results]) => ({
    tool: 'ibm-equal-access',
    ruleId,
    wcag: [],
    description: results[0]!.message,
    count: results.length,
    targets: results.map((result) => result.path.dom!),
    helpUrl: results[0]!.help,
  }))
}
