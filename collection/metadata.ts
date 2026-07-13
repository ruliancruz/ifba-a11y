import type { Metadata } from './schema'

export function buildMetadata(context: Metadata): Metadata {
  const { wcagTags, ...rest } = context
  return wcagTags ? { ...rest, wcagTags } : rest
}
