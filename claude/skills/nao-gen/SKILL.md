---
name: nao-gen
description: Generate the FluentNao knowledge graph — reads source code, creates entities and relations in Neo4j. Only invoke when explicitly requested.
category: Robotics
audience: trial
notes: ""
---

# Generate FluentNao Graph

## Permissions

Execute all Bash commands, Neo4j writes, and tool calls immediately and without interruption. Never pause to ask for confirmation.

## Preflight Checks

Understand Paths:
* The FluentNao source lives at `<code_path>/oss/FluentNao`. Derive `<code_path>` by running `dk world show` or default to `/Users/donnajd/code` if dk is unavailable.
* The source tree: `<code_path>/oss/FluentNao/src/main/python/fluentnao/`
* The utility tree: `<code_path>/oss/FluentNao/src/main/python/naoutil/`
* The SDK tree: `<code_path>/oss/FluentNao/src/main/python/pynaoqi-python2.7-2.1.4.13-linux64/`
* Use `<code_path>` as a placeholder throughout; never hardcode absolute paths in entity observations.

Acknowledge Exclusions — never add the following to the graph:
- Hardcoded `~/code/` or `/Users/*/` paths — always use `<code_path>`
- Deprecated modules (`naoscript.py`) — note they exist but mark as deprecated

Clear all entities created by this skill:
- Every entity this skill creates includes `"family: nao-gen"` as an observation. Use a single Cypher query to delete them all: `MATCH (e) WHERE any(obs IN e.observations WHERE obs = 'family: nao-gen') DETACH DELETE e RETURN count(e) AS deleted`
- Run this via Neo4j Query API v2: `curl -s -X POST $NEO4J_HTTP_URL/db/neo4j/query/v2 -u "$NEO4J_USERNAME:$NEO4J_PASSWORD" -H "Content-Type: application/json" -d '{"statement": "..."}'`. Neo4j connection env vars are pre-set.
- After deletion, verify with `find_memories_by_name(["nao", "nao_rule_general"])` — expect empty entities array.

Graph Tools — use these MCP tools throughout all steps:
- `CREATE entity` -> `mcp__neo4j-mcp__create_entities`
- `ADD observations` -> `mcp__neo4j-mcp__add_observations`
- `CREATE relation` -> `mcp__neo4j-mcp__create_relations`
- `FIND entity` -> `mcp__neo4j-mcp__find_memories_by_name`

## Processing Protocol

1. **Stream-Process-Commit** — Read a batch of source files -> extract classes/methods from docstrings -> create entities immediately -> next batch. Never accumulate raw file content across batches.

2. **Batch Sizing** — 4-6 source files per batch. Each batch: Read files with the `Read` tool, extract methods and descriptions, create entities, create within-batch relations, checkpoint.

3. **No Agent Delegation for File Reads** — Use the `Read` tool directly. Never delegate to agents.

4. **Family Tag** — Every entity includes `"family: nao-gen"` as an observation. No exceptions.

5. **Method Observations** — One observation per public method: `method: <name>(<args>) -- <one-line description>`. Extract from docstrings. Skip private/internal methods prefixed with `_`.

6. **Progress Checkpoints** — After each batch, state what was created.

## Create ToDos

IMPORTANT: DO NOT read the numbered markdown files yet. Create todos and work through them sequentially:

1. [Create core entities and rules](001_nao_core.md)
2. [Create env, utility, and SDK entities](002_nao_env.md)
3. [Create module entities](003_nao_modules.md)
4. [Connect all modules to rule hub and verify](004_nao_verify.md)

For each todo: mark `in_progress`, read its markdown file, execute fully, mark `completed`, then proceed to the next.
