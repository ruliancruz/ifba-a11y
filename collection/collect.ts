import * as fs from 'node:fs'
import * as path from 'node:path'
import type { Target } from './config'
import type { Fidelity, Result } from './schema'
import { parseTargets } from './targets'

export function writeResult(directory: string, filename: string, result: Result): void {
  fs.mkdirSync(directory, { recursive: true })
  fs.writeFileSync(path.join(directory, filename), JSON.stringify(result, null, 2))
}

export function writeFidelity(directory: string, fidelity: Fidelity): void {
  fs.mkdirSync(directory, { recursive: true })
  fs.writeFileSync(path.join(directory, 'fidelity.json'), JSON.stringify(fidelity, null, 2))
}

export function loadTargets(file: string | undefined, defaults: Target[]): Target[] {
  if (file === undefined || file === '') return defaults

  return parseTargets(JSON.parse(fs.readFileSync(file, 'utf-8')))
}
