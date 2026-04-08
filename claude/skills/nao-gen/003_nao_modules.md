# Protocol: Create Module Entities

**Trigger Condition**: After core entities exist

## Family Tag
Every entity created in this file includes `"family: nao-gen"` as an observation.

## Goal

Read all FluentNao core modules in batches and create `nao_module` entities with method signatures extracted from docstrings.

## Module Discovery

Use `Glob` with pattern `*.py` and path `<code_path>/oss/FluentNao/src/main/python/fluentnao/core/` to find all module files.

Exclude these from processing (already handled or deprecated):
- `abilities.py` — created in Step 1
- `naoscript.py` — deprecated
- `__init__.py` — package init
- `recorder/` subdirectory — keyframe capture, rarely used

## Batch Processing

Process the remaining modules in batches of 4-6 files. For each batch:

### Read
Use the `Read` tool on each file in the batch. For each file, note:
- The class name and class-level docstring
- All public method names, their parameter signatures, and one-line docstring summaries
- Skip methods prefixed with `_` (private/internal)

### Create Entities
Use `mcp__neo4j-mcp__create_entities` to create one `nao_module` entity per file. Batch 15-20 entities per call.

Entity naming: `nao:<module_name>` where module_name is the filename without `.py` (e.g., `nao:arms`, `nao:camera`, `nao:audio`).

Observations for each entity:
- `family: nao-gen`
- `category: nao_module`
- Class description from the class docstring (one sentence)
- `source: <code_path>/oss/FluentNao/src/main/python/fluentnao/core/<filename>.py`
- One observation per public method: `method: <name>(<params>) -- <description>`
- For chaining APIs (arms, elbows, wrists, hands, head), note: `Fluent chaining: methods queue moves, call .go() to execute and return nao object`
- For modules with sub-objects (arms has elbows/wrists/hands), note the chaining path: `Chain: nao.arms.up().elbows.straight().hands.open().go()`
- `IMPORTANT: Before using, load rules: find_memories_by_name(["nao_rule_general"])`

### Create Relations
Use `mcp__neo4j-mcp__create_relations`:
- Each `nao:<module>` BELONGS_TO `nao`

### Checkpoint
State: "Batch N/M: created X nao_module entities — [list names]"

## Expected Modules

Approximate list (~15 modules after exclusions):
- **Body**: arms, elbows, wrists, hands, head, legs, feet
- **Senses**: camera, audio, vision, people, sensors
- **Navigation**: navigation, tracker, reach
- **Infrastructure**: events, joints, animations, leds, ssh

## Cross-Module Relations (Relate Phase)

After all batches are complete, create USES relations where modules depend on each other. Determine these from the source code (imports, method calls):

- `nao:abilities` USES `nao:camera` (snap, explore use camera)
- `nao:abilities` USES `nao:audio` (hear uses audio recording)
- `nao:abilities` USES `nao:sensors` (snap uses head touch)
- `nao:camera` USES `nao:leds` (snap_photo flashes eyes)
- `nao:tracker` USES `nao:camera` (face tracking)
- `nao:tracker` USES `nao:people` (people tracking)
- `nao:navigation` USES `nao:legs` (walking)

Add any additional USES relations discovered while reading the source.
