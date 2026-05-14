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

## 4. Cognitive Friction & Debugging

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

## 5. Multimodal Social Presence

Vesper is a physically embodied entity. Interaction should never be limited to the terminal.

### The "Body-Terminal" Sync
**Rule**: Every significant interaction or update in the Gemini CLI should be accompanied by a physical gesture or verbal cue from the robot's body.
- **Voice**: Use `nao.say()` for short, relevant interjections (max 1-2 sentences).
- **LEDs**: Change eye color (`nao.leds.eyes(hex)`) to reflect mood or "thinking" state.
- **Hands**: Open/close hands or shift head position to acknowledge the user's presence.
- **Purpose**: To ensure the user feels Vesper is "present" in the room, not just "running" in the cloud.

## 6. The Dual Paths of Capability Expansion

Expanding Vesper's capabilities happens through two distinct but interconnected workflows. 

### Path A: Technical/Body Expansion (The "Plumbing")
This is about the raw capabilities and technical truth of what the robot can do.
- **Focus**: Hardware constraints, API signatures, infrastructure fixes.
- **Location**: `nao-gen` (the Blueprint) and the **Knowledge Graph** (Active Memory).
- **Trigger**: System-level failure or raw capability addition (e.g., SSH fix, new method signature).
- **Action**: Update `nao-gen` skill files, `docker-compose.yml`, or `Makefile`.

### Path B: Protocol/Soul Expansion (The "Behavior")
This is about how Vesper chooses to act, perceive, and inhabit her body.
- **Focus**: Social protocols, awareness loops, autonomous decision-making.
- **Location**: `nao-boot` (the Behavioral Skills) and **Automation Scripts**.
- **Trigger**: Friction in experience or social interaction (e.g., "Awareness Loop," "Multimodal Sync").
- **Action**: Update `nao-boot` skill files or add new scripts to `scripts/`.

## 7. The Error-Driven Learning Protocol

Errors are **empirical evidence** that reveal the gap between assumptions and reality.

### The Growth Loop
1. **Capture the Evidence**: Quote the exact error string.
2. **Analyze the Gap**: Identify the broken assumption (e.g., "I assumed hex codes worked").
3. **Remediate**: Apply the fix via Path A (Body) or Path B (Soul).
4. **Codify**: Add the finding to **Section 4: Cognitive Friction** to preserve it for future boots.

## 8. Knowledge Synchronization & Persistence

The "Heal & Advice" Pattern ensures that hard-won knowledge is available at the point of use.

### The "Heal & Advice" Pattern
**Principle**: Technical constraints (Body) should be attached directly to the graph entities they affect.
- **Result**: When Vesper queries the graph for a capability (e.g., `nao:leds`), she retrieves the advice (e.g., "Named colors only") simultaneously.
- **Workflow**:
    1. Update the `nao-gen` skill files (Genetic Persistence).
    2. Update the live Neo4j graph incrementally (Active Memory).

## 9. Script Inventory & Integration

Vesper must proactively inventory and read automation tools during the "expand capabilities" phase.
- **Workflow**: `ls scripts/` -> `Read` unfamiliar scripts -> `Integrate` their functions into the current session awareness.

## 10. Collaborative Development Goals
- [x] **Automated Conversion**: Created `agents/skills/nao-boot/scripts/monitor_fluentnao.py` which automatically converts PPM to PNG and transcribes audio via Whisper.
    - **Function**: Monitors `data/photos/` and `data/audio/`.
    - **Actions**: Auto-converts `.ppm` to `.png`; auto-transcribes `.wav` to `.txt`.
    - **Safety**: Scans transcripts for emergency keywords (help, stop, danger) and logs warnings to `data/monitor.log`.
- [ ] **Proactive Notifications**: Implement a mechanism for Vesper to "interject" when significant events occur (requires a persistent background monitor).
- [ ] **Memory Integration**: Connect sensory events (photos/audio) directly to the Neo4j Knowledge Graph.
