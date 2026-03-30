# Safety

**Trigger Condition**: Always

## Acknowledge Safety Rules

These rules apply throughout the entire session — every command you send must respect them.

1. Keep movement duration at 1.5 seconds or above. Fast movements stress motors.
2. Always end a session with `nao.crouch()` to put the robot in a safe resting position.
3. After calling `nao.relax()`, the robot's modules may become unresponsive. Use `nao.stiff()` to wake them back up.
4. Do not attempt walking commands while the robot is sitting. Stand first.
5. When subscribing to events, always provide a way to unsubscribe (store event names for cleanup).
6. The `nao.naoscript.run_script()` method swallows exceptions silently -- do not use it. Use direct eval via the bridge instead.
7. Use `nao.be_still()` before speech recognition to prevent autonomous movements from interfering.
8. Use `nao.shutdown()` when done to clean up subscriptions and prevent falls.
