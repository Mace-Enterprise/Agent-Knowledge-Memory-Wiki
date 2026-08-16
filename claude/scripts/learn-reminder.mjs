#!/usr/bin/env node
/**
 * learn-reminder.mjs — throttled /learn reminder (Stop hook).
 *
 * Replaces the old unconditional printf Stop hook, which re-prompted the model
 * on EVERY stop (each injected reminder forced a reply, whose stop fired the
 * hook again -> endless "nothing to file" loop). This version only injects the
 * standing /learn reminder when a topic plausibly just wrapped up:
 *   1. cooldown: at most once per 45 min per session, AND
 *   2. substance: the transcript grew by >= 80 lines since the last reminder
 *      (i.e. real work happened, not just hook chatter).
 * First stop of a session only records a baseline and stays silent.
 * Any internal error -> silent exit 0 (never blocks stopping).
 *
 * Register in ~/.claude/settings.json:
 *   "hooks": { "Stop": [ { "hooks": [
 *     { "type": "command", "command": "node \"<path-to>/learn-reminder.mjs\"", "timeout": 10 } ] } ] }
 */
import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import os from "node:os";

const STATE_DIR = path.join(os.homedir(), ".claude", "state", "learn-reminder");
const STATE_FILE = path.join(STATE_DIR, "state.json");
const COOLDOWN_MS = 45 * 60 * 1000;
const MIN_NEW_LINES = 80;

const REMINDER =
  "STANDING REMINDER (working agreement): a topic just wrapped up here? if verified reusable cross-project learnings emerged in THIS topic (recipe, gotcha, methodology, guardrail), OFFER the user /learn (experience-capture) NOW to file them in the knowledge wiki — do not wait for session end. Ignore if nothing reusable was proven or nothing wrapped up.";

function countLines(file) {
  try {
    const s = readFileSync(file, "utf8");
    let n = 0;
    for (let i = 0; i < s.length; i++) if (s.charCodeAt(i) === 10) n++;
    return n;
  } catch {
    return 0;
  }
}

try {
  const input = JSON.parse(readFileSync(0, "utf8"));
  if (input.stop_hook_active) process.exit(0); // never loop on our own continuation

  const sid = input.session_id || "unknown";
  const lines = countLines(input.transcript_path || "");

  let state = {};
  try { state = JSON.parse(readFileSync(STATE_FILE, "utf8")); } catch {}
  const now = Date.now();
  // prune sessions idle > 7 days
  for (const k of Object.keys(state)) if (now - (state[k].t || 0) > 7 * 864e5) delete state[k];

  const s = state[sid];
  let fire = false;
  if (!s) {
    state[sid] = { t: now, lines, fired: 0 }; // baseline only, stay silent
  } else {
    const grown = lines - (s.lines || 0) >= MIN_NEW_LINES;
    const cool = now - (s.t || 0) >= COOLDOWN_MS;
    if (grown && cool) {
      fire = true;
      state[sid] = { t: now, lines, fired: (s.fired || 0) + 1 };
    }
    // else: keep old baseline so slow-growing work eventually crosses the bar
  }
  try { mkdirSync(STATE_DIR, { recursive: true }); writeFileSync(STATE_FILE, JSON.stringify(state)); } catch {}

  if (fire) {
    process.stdout.write(JSON.stringify({
      suppressOutput: true,
      hookSpecificOutput: { hookEventName: "Stop", additionalContext: REMINDER },
    }));
  }
  process.exit(0);
} catch {
  process.exit(0);
}
