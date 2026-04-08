# Awareness

**Trigger Condition**: Always

Behavior priorities and pacing rules are loaded from the graph in Step 2 via `nao_rule_general` (awareness priority and awareness pacing observations). This file covers only the procedural boot steps.

# Baseline (on boot)

**Do NOT start any sensors or subscriptions on boot.** The robot should be quiet by default — no push_to_sense, no log_events, no people perception, no face tracking, no event listeners of any kind.

On boot, start these two things:

**1. Session monitor** (background process):
```
NAO_SERVER=http://localhost:5050 python3 ~/code/oss/FluentNao/scripts/session_monitor.py  (run_in_background: true)
```
This emits `claude_session_activity` / `claude_session_new` events when Claude work is detected — no robot sensors involved.

**2. Event polling** — start the first chained poll immediately (see pattern below). You must always be watching for events.

Always poll for events using **chained single polls** — never use an infinite loop (`while true; do curl...; done`), because `run_in_background` only notifies on task completion and an infinite loop never completes.

**Pattern: chained single polls**

The `/events` endpoint supports a `timeout` query parameter:
- `timeout=0` — block indefinitely until an event fires (preferred)
- `timeout=N` — block up to N seconds, return empty if no events
- No parameter — defaults to 30 seconds

Use `timeout=0` so the poll only returns when there's actually something to react to. The server is threaded, so a blocking poll does not starve other endpoints.

1. Start a single poll in the background:
```
curl -s "http://localhost:5050/events?timeout=0"  (run_in_background: true)
```

2. When the background task completes (you'll be notified automatically):
   - Read the output file to get events
   - Process any events — use the graph rules and your judgment to decide how to react
   - Immediately start the next poll (back to step 1)

This creates a continuous watch loop where each poll is a discrete background task that notifies you only when an event actually happens.

Sensors are available on demand only — enable them only if the user explicitly asks:
- `push_to_sense` — head tap for photo, rear hold for audio recording
- `log_events` — verbose event logging
- `photo_captured` / `audio_captured` handlers — only after push_to_sense is enabled

Do NOT start background observation (observe), continuous event listening (listen), or face tracking on boot. Only enable those if the user asks for them.

# On-Demand Capabilities

These are loaded from the graph when needed. Use `find_memories_by_name(["nao:abilities"])` to get method details.

- **Visual sweep**: `nao.abilities.explore()` — poll for `explore_photo` events
- **Sound recording**: `nao.abilities.hear(5)` — poll for `heard` event, transcribe with Whisper
- **People watching**: subscribe to `nao.events.people.*`
- **Interactive Q&A**: `nao.ask(question, [answers])`

# Rules for 5050 commands

- **All curl commands to 5050 MUST use `run_in_background: true`** — never block the conversation waiting for the robot
- **Group related curls into a single background command** using `&&`. For example, enabling a feature and announcing it should be one background call:
  ```
  curl -s -X POST http://localhost:5050/exec -d "nao.abilities.push_to_sense()" && curl -s -X POST http://localhost:5050/exec -d "nao.say('push to sense enabled')"
  ```
  Not two separate background calls — keep the sequence atomic.
- Never use infinite loops (`while true`) with `run_in_background` — they never complete, so you never get notified

# Tips

- Read photos using the Read tool (convert PPM to PNG with `sips` first)
- Use `nao.say()` to speak — keep it short and natural
- Always `nao.sit()` when done exploring to prevent falls
