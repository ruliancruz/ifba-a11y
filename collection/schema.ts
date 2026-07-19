export type Tool = 'axe-core' | 'ibm-equal-access'

export interface Violation {
  tool: Tool
  ruleId: string
  wcag: string[]
  description: string
  count: number
  targets: string[]
  impact?: string
  helpUrl?: string
}

export interface Metadata {
  timestamp: string
  url: string
  browser: string
  browserVersion: string
  viewport: { width: number; height: number } | null
  device: string
  tool: Tool
  toolVersion: string
  wcagTags?: readonly string[]
}

export interface Result<Raw = unknown> {
  metadata: Metadata
  violations: Violation[]
  raw: Raw
}

export interface MissingAsset {
  status: number
  resourceType: string
  url: string
}

export interface Fidelity {
  stylesheets: number
  missingAssets: MissingAsset[]
}
