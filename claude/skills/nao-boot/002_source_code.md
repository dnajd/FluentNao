# Source Code

**Trigger Condition**: Always

## Goal

Load the FluentNao API knowledge from the graph instead of reading source files directly.

## Step 1: Load the rule hub

Use `mcp__neo4j-mcp__find_memories_by_name` with `["nao_rule_general"]`.

This returns:
- Rule observations: boot sequence, command patterns, playSine, photos, audio, events, LEDs, awareness priorities
- HAS_MODULE edges listing ALL available modules by name (arms, camera, audio, env, sdk_motion, etc.)
- HAS_RULE edge to `nao_rule_safety`

Acknowledge: you now know what modules exist. Do NOT load them all — only load a specific module when the user asks for that capability.

## Step 2: Load the safety rules

Use `mcp__neo4j-mcp__find_memories_by_name` with `["nao_rule_safety"]`.

Read every observation. These are hard constraints for the entire session. Acknowledge them all.

## Step 3: Load the root entity

Use `mcp__neo4j-mcp__find_memories_by_name` with `["nao"]`.

This gives you the HTTP bridge details, response formats, and the top-level nao.py methods (say, sit, stand, walk, etc.).

## On-demand module loading

When you need a specific capability during the session, load it:
```
find_memories_by_name(["nao:camera"])    — photo methods
find_memories_by_name(["nao:arms"])      — arm movements
find_memories_by_name(["nao:env"])       — raw ALModule proxy access
find_memories_by_name(["nao:sdk_motion"]) — motion constants
```

If the graph is empty (nao-gen hasn't been run yet), fall back to reading source files directly from `~/code/oss/FluentNao/src/main/python/fluentnao/`. Use the file listing below as a guide:

# Fallback: FluentNao Source Tree

~/code/oss/FluentNao/src/main/python/fluentnao
  |- nao.py                     # Main Nao class
  +- core/                      # All modules (arms, camera, audio, etc.)

~/code/oss/FluentNao
  |- server.py                  # HTTP bridge
  |- Makefile                   # Docker commands
