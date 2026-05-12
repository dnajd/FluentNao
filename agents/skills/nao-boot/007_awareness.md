# Awareness

**Trigger Condition**: Always

... (procedural rules unchanged) ...

# 1. Event polling

**Session monitor** (on-demand, NOT on boot):
```bash
NAO_SERVER=http://localhost:5050 python3 scripts/session_monitor.py (run_in_background: true)
```

**Chained single polls**:
Start a single poll in the background:
```bash
curl -s "http://localhost:5050/events?timeout=0" (run_in_background: true)
```

... (pacing and processing rules unchanged) ...

# Rules for 5050 commands

- **All curl commands to 5050 MUST use `run_in_background: true`**
- **Group related curls into a single background command** using `&&`:
  ```bash
  curl -s -X POST http://localhost:5050/exec -d "nao.abilities.push_to_sense()" && curl -s -X POST http://localhost:5050/exec -d "nao.say('push to sense enabled')"
  ```

# Photos & Files

Since we are running locally on the home server, files are written directly to your disk:

1. **Path**: Files appear instantly in `data/photos/`.
2. **Convert & Read**: `convert data/photos/<name>.ppm data/photos/<name>.png` then use the `read_file` tool.
