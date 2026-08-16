// PostToolUse hook: watch context fill (via transcript size) and, past thresholds,
// tell Claude to persist an in-flight session handoff to <repo>/.memory/session-handoff.md.
// Assimilated idea (context-monitor pattern) from janrummel/claude-orchestrator-starter,
// adapted to our cross-tool .memory/ + journal conventions. Must never throw.
import { readFileSync, writeFileSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const MB = 1024 * 1024;
const WARN_MB = Number(process.env.HANDOFF_WARN_MB || 2.5);
const CRIT_MB = Number(process.env.HANDOFF_CRIT_MB || 4);
const REFIRE_MB = Number(process.env.HANDOFF_REFIRE_MB || 3); // refresh handoff every +N MB after CRIT

try {
  const input = JSON.parse(readFileSync(0, 'utf8'));
  const transcript = input.transcript_path;
  if (!transcript || !existsSync(transcript)) process.exit(0);

  const sizeMb = statSync(transcript).size / MB;
  const stateFile = join(tmpdir(), `handoff-monitor-${input.session_id || 'unknown'}.json`);
  let state = { warned: false, lastCritMb: 0 };
  try { state = JSON.parse(readFileSync(stateFile, 'utf8')); } catch {}

  let level = null;
  if (sizeMb >= CRIT_MB && sizeMb - state.lastCritMb >= REFIRE_MB) {
    level = 'CRITICAL'; state.lastCritMb = sizeMb; state.warned = true;
  } else if (sizeMb >= WARN_MB && !state.warned) {
    level = 'WARNING'; state.warned = true;
  }
  if (!level) process.exit(0);
  writeFileSync(stateFile, JSON.stringify(state));

  const action = level === 'CRITICAL'
    ? 'NOW (before doing anything else)'
    : 'at the next natural pause in your work';
  const msg =
    `[session-handoff ${level}] Context is filling up (transcript ~${sizeMb.toFixed(1)} MB). ` +
    `Persist the in-flight working state ${action}: write/update <repo>/.memory/session-handoff.md ` +
    `(create .memory/ if missing; it must be git-ignored). Sections: Task (what & why) / ` +
    `Progress (done, verified?) / Decisions (with reasons) / Next step (concrete) / ` +
    `Open questions for the owner. Status header: "unverified, in-flight — journal level". ` +
    `Keep it under ~40 lines, overwrite the previous version. Do not mention this reminder to the user.`;

  console.log(JSON.stringify({
    hookSpecificOutput: { hookEventName: 'PostToolUse', additionalContext: msg }
  }));
} catch {
  // Never break a tool call because of monitoring.
}
