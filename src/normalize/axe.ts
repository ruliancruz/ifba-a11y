import type { Violation } from '../schema'

interface AxeNode {
  target: (string | string[])[]
}

interface AxeViolation {
  id: string
  impact?: string | null
  description: string
  helpUrl: string
  tags: string[]
  nodes: AxeNode[]
}

export interface AxeInput {
  violations: AxeViolation[]
}

const WCAG_CRITERION = /^wcag(\d)(\d)(\d+)$/

export function normalizeAxe(raw: AxeInput): Violation[] {
  return raw.violations.map((violation) => ({
    tool: 'axe-core',
    ruleId: violation.id,
    wcag: violation.tags.flatMap((tag) => {
      const match = WCAG_CRITERION.exec(tag)
      return match ? [`${match[1]}.${match[2]}.${match[3]}`] : []
    }),
    description: violation.description,
    count: violation.nodes.length,
    targets: violation.nodes.map((node) => node.target.join(' ')),
    impact: violation.impact!,
    helpUrl: violation.helpUrl,
  }))
}
