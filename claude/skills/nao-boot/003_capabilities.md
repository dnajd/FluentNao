# Capabilities

**Trigger Condition**: Always

All API reference knowledge is stored in the graph. You loaded it in Step 2 via `nao_rule_general`.

## What you already know from the graph

The `nao_rule_general` observations cover:
- HTTP bridge command pattern (`/exec`, `/reload`, `/health`, `/events`, `/audio`)
- playSine tone generation with frequency table
- Photo capture and PPM-to-PNG conversion pipeline
- Audio recording and Whisper transcription pipeline
- Event subscription and long polling
- LED color control and eye tracking
- Fluent chaining API pattern

## How to learn more

When you need methods for a specific module, load it from the graph:
```
find_memories_by_name(["nao:<module>"])
```

Each module entity has `method:` observations listing every public method with its signature and description.

## Acknowledge

You have the full API available through the graph. No source files need to be read unless the graph is empty (fallback in Step 2 covers this).
