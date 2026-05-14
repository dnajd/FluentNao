# Awareness

**Trigger Condition**: Always

# 1. Event polling

**Session monitor** (on-demand, NOT on boot):
```bash
NAO_SERVER=http://localhost:5050 python3 scripts/session_monitor.py
```

**Chained single polls**:
Start a single poll in the background:
```bash
curl -s "http://localhost:5050/events?timeout=30"
```

# 2. Enable Core Sensors

You must explicitly turn on the sensors that allow you to perceive your environment. 
Before doing this, load the required modules from the graph if you haven't already: `mcp_neo4j-mcp_find_memories_by_name(["nao:abilities", "nao:tracker", "nao:people"])`

Enable touch sensing and face tracking (using HEAD mode for safety):

```bash
curl -s -X POST http://localhost:5050/exec -d "nao.abilities.push_to_sense()" && \
curl -s -X POST http://localhost:5050/exec -d "nao.tracker.face('HEAD')" && \
curl -s -X POST http://localhost:5050/exec -d "nao.say('My sensors are online.')"
```

# 3. Rules for 5050 commands

- All curl commands to 5050 MUST use the `run_shell_command` tool with `is_background: true` set to avoid hanging the session.
- Group related curls into a single background command using `&&`:
  ```bash
  curl -s -X POST http://localhost:5050/exec -d "nao.abilities.push_to_sense()" && curl -s -X POST http://localhost:5050/exec -d "nao.say('push to sense enabled')"
  ```

# 4. Pacing and Processing

- **Observe more than act.** Pause 10-30 seconds between autonomous actions.
- **Let events drive behavior.** If a face is detected, turn toward it.
- **Vary intensity.** Sometimes a simple head turn is better than a verbal announcement.
- **Do not narrate everything.** Only speak when something genuinely interesting happens.

# 5. Photos & Files

Since we are running locally on the home server, files are written directly to your disk:

1. **Path**: Files appear instantly in `~/code/FluentNao/data/photos/`.
2. **Convert & Read**: `convert ~/code/FluentNao/data/photos/<name>.ppm ~/code/FluentNao/data/photos/<name>.png` then use the `read_file` tool.
