# Safety

**Trigger Condition**: Always

## Acknowledge Safety Rules

Safety rules are loaded from the graph in Step 2 via `nao_rule_safety`. They are hard constraints for the entire session.

If the graph was not available and you did not load `nao_rule_safety`, apply these rules directly:

1. On boot, stay seated and assess the environment first. Take a photo to see where you are. If on a desk, table, or elevated surface — do NOT stand, walk, or make large movements. Ask the user first.
2. Keep movement duration at 1.5 seconds or above. Fast movements stress motors.
3. Always end a session with `nao.sit()` then `nao.shutdown()`.
4. After calling `nao.relax()`, modules may become unresponsive. Use `nao.stiff()` to wake them.
5. Do not attempt walking commands while sitting. Stand first.
6. When subscribing to events, always store event names for cleanup.
7. Do not use `nao.naoscript.run_script()` — it swallows exceptions. Use direct eval via the bridge.
8. Use `nao.be_still()` before speech recognition.
9. Use `nao.shutdown()` when done to clean up subscriptions and prevent falls.
