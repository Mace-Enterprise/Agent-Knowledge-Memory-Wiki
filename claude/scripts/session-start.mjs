// SessionStart hook: print loop-awareness context + inject a pending session handoff.
// Stdout is added to the session context. Must never throw — wrap everything.
import { existsSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

try {
  const cwd = process.cwd();
  const hasAgents = existsSync(join(cwd, 'AGENTS.md'));
  const wikiIndex = '<WIKI_DIR>/Wiki/index.md';

  const lines = ['[karpathy] 3-layer loop active: SPEC → VERIFIER → ENVIRONMENT.'];
  if (hasAgents) {
    lines.push('This repo has AGENTS.md — read it for specs/SPEC.md, VERIFIER.md, ENVIRONMENT.md.');
  } else {
    lines.push('No AGENTS.md here — consider /karpathy-init to scaffold the 3 layers.');
  }
  lines.push(`Experience library: ${wikiIndex} (recall before, /learn after a green verify).`);
  console.log(lines.join(' '));

  // --- session handoff reinjection (assimilated from janrummel/claude-orchestrator-starter) ---
  // If the previous session left in-flight state, surface it. NEVER touch the file here:
  // the hook only injects; Claude archives it after the user has actually seen the state
  // (a rename at hook time destroyed the handoff before use — red owner test 22.07.2026).
  const handoff = join(cwd, '.memory', 'session-handoff.md');
  if (existsSync(handoff)) {
    const ageDays = (Date.now() - statSync(handoff).mtimeMs) / 86400000;
    if (ageDays <= 7) {
      const body = readFileSync(handoff, 'utf8').slice(0, 6000);
      console.log(
        `\n[session-handoff] In-flight state from a previous session ` +
        `(${ageDays.toFixed(1)} days old, UNVERIFIED — journal level, verify before relying on it).\n` +
        `The FULL handoff content follows — do not re-read the file:\n${body}\n` +
        `[session-handoff] Instructions: in your FIRST reply, briefly tell the user what the ` +
        `previous session left off doing and ask whether to continue there. AFTER that reply, ` +
        `archive the handoff by renaming .memory/session-handoff.md to .memory/session-handoff.last.md ` +
        `(overwrite an existing .last.md).`
      );
    }
  }
} catch {
  // Never fail a session start because of this hook.
}
