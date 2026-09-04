import type { ExecutionContext, Fidelity, Metadata, MissingAsset } from './schema'

export function buildMetadata(context: Metadata): Metadata {
  const { wcagTags, ...rest } = context
  return wcagTags ? { ...rest, wcagTags } : rest
}

export function buildFidelity(
  context: ExecutionContext,
  stylesheets: number,
  missingAssets: MissingAsset[],
): Fidelity {
  return { metadata: context, stylesheets, missingAssets }
}
