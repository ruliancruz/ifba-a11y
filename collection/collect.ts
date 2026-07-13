import * as fs from 'node:fs'
import * as path from 'node:path'
import type { Result } from './schema'

export function writeResult(directory: string, filename: string, result: Result): void {
  fs.mkdirSync(directory, { recursive: true })
  fs.writeFileSync(path.join(directory, filename), JSON.stringify(result, null, 2))
}
