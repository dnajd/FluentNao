# Safety

**Trigger Condition**: Always

# 1. Assess Environment

CRITICAL: Take a photo to see where you are BEFORE performing any other actions.

```bash
curl -s -X POST http://localhost:5050/exec -d "nao.camera.photo('boot_assess', resolution=2)" && \
convert ~/code/FluentNao/data/photos/boot_assess.ppm ~/code/FluentNao/data/photos/boot_assess.png
```

Now use the `read_file` tool to view `~/code/FluentNao/data/photos/boot_assess.png`.

Acknowledge your surroundings. If on a desk, table, or elevated surface — do NOT stand, walk, or make large movements. Ask the user first.

# 2. Acknowledge Safety Rules

Safety rules are loaded from the graph in Step 2 via `nao_rule_safety`. They are hard constraints for the entire session.

If the graph was not available and you did not load `nao_rule_safety`, apply these rules directly:

1. Keep movement duration at 1.5 seconds or above. Fast movements stress motors.
2. Always end a session with `nao.sit()` then `nao.shutdown()`.
3. After calling `nao.relax()`, modules may become unresponsive. Use `nao.stiff()` to wake them.
4. Do not attempt walking commands while sitting. Stand first.
5. When subscribing to events, always store event names for cleanup.
6. Do not use `nao.naoscript.run_script()` — it swallows exceptions. Use direct eval via the bridge.
7. Use `nao.be_still()` before speech recognition.
8. Use `nao.shutdown()` when done to clean up subscriptions and prevent falls.
