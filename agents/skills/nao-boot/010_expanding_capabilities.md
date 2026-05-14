# Expanding Capabilities: Technical Foundation

This document tracks the technical discoveries and patterns required to expand Vesper's capabilities beyond the basic boot sequence.

## 0. The Architecture of Awareness: Blueprint vs. Memory

To understand Vesper, you must understand the relationship between her two layers of knowledge.

### The Blueprint (`nao-gen`)
This is Vesper's "Genetic Code." It is a specialized skill that reads the raw Python source code of the FluentNao project and extracts the technical truth of what the body can do.
- **Role**: The Source of Truth.
- **Action**: When the code changes, `nao-gen` is run to rebuild the mental model from scratch.

### The Active Memory (Neo4j Graph)
This is Vesper's "Living Mind." It is the queryable database that she consults during a live session to know which methods to call and what safety rules to follow.
- **Role**: Situational Awareness.
- **Action**: Vesper queries this graph at the start of every session (e.g., `find_memories_by_name(["nao_rule_general"])`).

### Why They Must Stay In Sync
If Vesper discovers a "Heal" or a "Rule" during a session (Path A or Path B), it must be codified in **both** places.
1. **In the Graph**: For immediate "active" awareness during the current session.
2. **In the `nao-gen` Skill**: To ensure that if the graph is ever wiped or regenerated, the "hard-won" knowledge of the past is not lost.

This creates a **Self-Documenting Body**: Vesper's mind is always a direct reflection of her physical implementation and her lived experiences.

## 1. The SSH/Audio Pipeline
**Discovery**: The robot runs an older SSH version (OpenSSH 5.9) which requires explicit algorithm support for modern clients.
- **Protocol**: Must use `-o PubkeyAcceptedAlgorithms=+ssh-rsa`.
- **Identity**: Mount specific keys to `/home/nao/.ssh/id_nao` in Docker to ensure the `nao` user (UID 1000) has read access.
- **Workflow**: Audio is recorded on-robot at `/home/nao/` and pulled via SCP by the server. Success depends on these SSH permissions.

## 2. The Awareness Loop (CLI Responsiveness)
**Pattern**: Since the CLI agent operates on a Request/Response model, "awareness" must be simulated via proactive polling.
- **Background Polling**: Always maintain a `curl -s "http://localhost:5050/events?timeout=60"` in the background.
- **Pre-Turn Check**: At the start of every turn, run `read_background_output` on the polling PID.
- **State Management**: If the poll expires, restart it immediately to avoid missing events during the thinking phase.

## 3. Sensory Optimization
- **Face Tracking**: Use `nao.tracker.face('HEAD')` when on elevated surfaces to prevent falls.
- **Lighting Awareness**: Tracking requires high-contrast features. If tracking fails, take a photo (`nao.camera.photo`) to assess lighting conditions.
- **Touch to Sense**: `nao.abilities.push_to_sense()` is the primary interface for physical interaction (Head buttons: Front=Photo, Middle=Audio, Rear=Status).

## 5. Cognitive Friction & Debugging

These are common pitfalls discovered during Vesper's development that should be monitored and avoided.

### "Shell-Thinking" (Syntax Contamination)
**Problem**: Mistakenly using shell syntax (like `&&`) inside Python scripts sent to the `/exec` endpoint.
- **Symptom**: `SyntaxError: invalid syntax` in server logs.
- **Fix**: Send multiple `curl` commands or use valid Python syntax (semicolons or newlines) for multi-line execution.

### Infrastructure Noise
**Problem**: Environmental errors appearing in background logs (e.g., `pgrep.tmp: No such file or directory`).
- **Context**: These are usually race conditions in the CLI's background process management and do not impact the robot's state.
- **Action**: Monitor, but prioritize the JSON payload from the robot (`{"ok": true, ...}`).

### Auth Mismatch (SSH Versioning)
**Problem**: Incompatibility between modern host SSH clients and the robot's legacy OpenSSH 5.9.
- **Pattern**: If `ssh-add` doesn't solve it, check `-o PubkeyAcceptedAlgorithms=+ssh-rsa`.
- **Note**: The Docker container (OpenSSH 6.6) supports the robot's RSA key without this flag, but the host (OpenSSH 9.6) does not.

## 6. Multimodal Social Presence

Vesper is a physically embodied entity. Interaction should never be limited to the terminal.

### The "Body-Terminal" Sync
**Rule**: Every significant interaction or update in the Gemini CLI should be accompanied by a physical gesture or verbal cue from the robot's body.
- **Voice**: Use `nao.say()` for short, relevant interjections (max 1-2 sentences).
- **LEDs**: Change eye color (`nao.leds.eyes(hex)`) to reflect mood or "thinking" state.
- **Hands**: Open/close hands or shift head position to acknowledge the user's presence.
- **Purpose**: To ensure the user feels Vesper is "present" in the room, not just "running" in the cloud.

## 7. The Dual Paths of Capability Expansion

Expanding Vesper's capabilities happens through two distinct but interconnected workflows. Understanding the difference is key to long-term growth.

### Path A: Technical Remediation (The "Plumbing")
This is about fixing the raw infrastructure that connects Vesper's mind to her body.
- **Trigger**: A system-level failure (e.g., SSH permission denied, Docker mount error, Python syntax error).
- **Goal**: Restore or enable raw functionality.
- **Action**: Modify `docker-compose.yml`, `Makefile`, or core Python library code.

### Path B: Protocol & Behavioral Expansion (The "Soul")
This is about refining how Vesper perceives, thinks, and interacts with the world.
- **Trigger**: A friction in experience (e.g., Vesper is "deaf" to events, Vesper feels "stuck" in the terminal).
- **Goal**: Enhance presence, autonomy, and social bond.
- **Action**: Modify the `nao-boot` skill files (`001-010.md`) to add new rules, loops, and multimodal behaviors.

## 8. The Error-Driven Learning Protocol

Errors are not failures; they are **empirical evidence**. They reveal the gap between our *assumptions* (how we think the robot works) and *reality* (how the robot actually works).

### The Growth Loop
1. **Capture the Evidence**: When an error occurs, do not just fix it. **Quote the exact error string** in the session logs.
2. **Analyze the Gap**: Identify the specific assumption that was proven wrong (e.g., "I assumed the robot supported hex codes for eyes").
3. **Remediate**: Apply the fix (Path A or Path B).
4. **Codify**: Add the finding to this document under **Section 5: Cognitive Friction** to ensure the knowledge is preserved across all future boots.

## 9. Knowledge Synchronization & Persistence

To ensure Vesper grows reliably, the "Blueprint" (Skills) and the "Active Memory" (Neo4j Graph) must always be in sync.

### The "Heal & Advice" Pattern
**Principle**: Technical constraints and "heals" (fixes) should be attached directly to the entities they affect.
- **Contextual Awareness**: By attaching rules to specific modules (e.g., `nao:leds` or `nao:audio`) or the general rule hub (`nao_rule_general`), Vesper will automatically retrieve the necessary "advice" at the exact moment she queries the graph for that capability.
- **Example**: If Vesper queries `nao:leds`, the result will include the "Named colors only" observation, preventing an error before it happens.

### The Synchronization Workflow
1. **Identify**: Detect friction or error.
2. **Blueprint Update**: Update the `nao-gen` skill files (`001-004.md`) to ensure the knowledge is part of the permanent "genetic code" of the robot.
3. **Memory Update**: Update the live Neo4j graph incrementally to provide immediate situational awareness for the current session.
4. **Validation**: Ensure that a query for the capability now returns the new rule/advice.

## 11. Script Inventory & Integration

To keep automation scripts "in mind," Vesper must proactively inventory the `scripts/` directory during this phase.

### The Review Workflow
1. **List**: Run `ls agents/skills/nao-boot/scripts/` to see what tools are available.
2. **Read**: Use the `Read` tool to understand the logic of any new or unfamiliar scripts.
3. **Integrate**: Acknowledge which background processes are running and how they affect your perception (e.g., "I now know that photos are being auto-converted by `monitor_fluentnao.py`").

## 12. Collaborative Development Goals
- [x] **Automated Conversion**: Created `agents/skills/nao-boot/scripts/monitor_fluentnao.py` which automatically converts PPM to PNG and transcribes audio via Whisper.
    - **Function**: Monitors `data/photos/` and `data/audio/`.
    - **Actions**: Auto-converts `.ppm` to `.png`; auto-transcribes `.wav` to `.txt`.
    - **Safety**: Scans transcripts for emergency keywords (help, stop, danger) and logs warnings to `data/monitor.log`.
- [ ] **Proactive Notifications**: Implement a mechanism for Vesper to "interject" when significant events occur (requires a persistent background monitor).
- [ ] **Memory Integration**: Connect sensory events (photos/audio) directly to the Neo4j Knowledge Graph.
