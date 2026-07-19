import * as fs from 'node:fs'
import * as path from 'node:path'
import type { Fidelity, Result } from './schema'

export function writeResult(directory: string, filename: string, result: Result): void {
  fs.mkdirSync(directory, { recursive: true })
  fs.writeFileSync(path.join(directory, filename), JSON.stringify(result, null, 2))
}

export function writeFidelity(directory: string, fidelity: Fidelity): void {
  fs.mkdirSync(directory, { recursive: true })
  fs.writeFileSync(path.join(directory, 'fidelity.json'), JSON.stringify(fidelity, null, 2))
}
