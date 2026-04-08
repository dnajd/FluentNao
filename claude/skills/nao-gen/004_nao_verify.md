# Protocol: Connect Hub and Verify Graph

**Trigger Condition**: After all module entities are created — this is Step 4 of nao-gen

## Family Tag
Every relation created in this file uses entities tagged with `"family: nao-gen"`.

## Goal

Connect all module entities to `nao_rule_general` as the hub, then verify the graph.

## Step 1: Discover all module entities

Use `mcp__neo4j-mcp__search_memories` with query `nao_module` to find all module entities created in Steps 1-3.

Build a list of all entity names (e.g., `nao:arms`, `nao:camera`, `nao:env`, `nao:sdk_motion`, etc.).

## Step 2: Connect all modules to the rule hub

Use `mcp__neo4j-mcp__create_relations` to create a `HAS_MODULE` relation from `nao_rule_general` to EVERY module entity found in Step 1.

This is the key design: when nao-boot loads `find_memories_by_name(["nao_rule_general"])`, it gets back:
- The rule observations (boot sequence, safety, command patterns)
- HAS_MODULE edges showing ALL available modules by name
- The model sees what's available without loading any method details
- It only calls `find_memories_by_name(["nao:<module>"])` when it needs that specific module

Create the relations in one batch:
```
nao_rule_general --HAS_RULE--> nao_rule_safety
nao_rule_general --HAS_MODULE--> nao:abilities
nao_rule_general --HAS_MODULE--> nao:arms
nao_rule_general --HAS_MODULE--> nao:elbows
nao_rule_general --HAS_MODULE--> nao:wrists
nao_rule_general --HAS_MODULE--> nao:hands
nao_rule_general --HAS_MODULE--> nao:head
nao_rule_general --HAS_MODULE--> nao:legs
nao_rule_general --HAS_MODULE--> nao:feet
nao_rule_general --HAS_MODULE--> nao:camera
nao_rule_general --HAS_MODULE--> nao:audio
nao_rule_general --HAS_MODULE--> nao:vision
nao_rule_general --HAS_MODULE--> nao:people
nao_rule_general --HAS_MODULE--> nao:sensors
nao_rule_general --HAS_MODULE--> nao:navigation
nao_rule_general --HAS_MODULE--> nao:tracker
nao_rule_general --HAS_MODULE--> nao:reach
nao_rule_general --HAS_MODULE--> nao:leds
nao_rule_general --HAS_MODULE--> nao:events
nao_rule_general --HAS_MODULE--> nao:env
nao_rule_general --HAS_MODULE--> nao:memory_util
nao_rule_general --HAS_MODULE--> nao:broker
nao_rule_general --HAS_MODULE--> nao:sdk_motion
nao_rule_general --HAS_MODULE--> nao:sdk_vision
... (include any additional modules discovered in Steps 2-3)
```

## Step 3: Verify the hub

Use `mcp__neo4j-mcp__find_memories_by_name` with `["nao_rule_general"]`.

Verify:
- Entity exists with type `nao_rule`
- Has boot sequence, command pattern, safety observations
- Has RULE_FOR relation to `nao`
- Has HAS_MODULE relations to ALL module entities — count should match the number of modules created
- Loading this ONE entity gives you a complete map of available capabilities

## Step 4: Spot-check 3 modules

Use `mcp__neo4j-mcp__find_memories_by_name` with `["nao:camera", "nao:env", "nao:sdk_motion"]`.

For each, verify:
- Has `method:` or `proxy:` or `const:` observations (detailed content)
- Has BELONGS_TO relation to `nao`
- Has the belt-and-suspenders reminder

## Step 5: Report

Print a summary:
- Total entities created (root + rule + modules + env + SDK)
- Total relations created (BELONGS_TO + HAS_MODULE + RULE_FOR + USES)
- Hub test: "Loading nao_rule_general shows N available modules"
- Any issues found
- Confirmation that the graph is ready for use by nao-boot

Describe the traversal strategy for nao-boot:
```
Boot:  find_memories_by_name(["nao_rule_general"])
       → rules + list of all modules via HAS_MODULE edges
Need camera? find_memories_by_name(["nao:camera"])
       → all camera methods and usage patterns
Need raw joints? find_memories_by_name(["nao:env"])
       → all ALModule proxy mappings
```
