# Protocol: Create Core Entities and Rules

**Trigger Condition**: Always — this is Step 1 of nao-gen

## Family Tag
Every entity created in this file includes `"family: nao-gen"` as an observation.

## Goal

Read nao.py, server.py, and abilities.py to create the root `nao` entity, the `nao_rule_general` rule entity, and the `nao_rule_safety` rule entity.

## Step 1: Read core source files

Use `Read` on these files:
- `<code_path>/oss/FluentNao/src/main/python/fluentnao/nao.py`
- `<code_path>/oss/FluentNao/server.py`
- `<code_path>/oss/FluentNao/src/main/python/fluentnao/core/abilities.py`

For each file, extract:
- Class name and class docstring
- All public method signatures and their docstrings (one-line summaries)
- Key constants or patterns

## Step 2: Create root entity

Use `mcp__neo4j-mcp__create_entities` to create:

**Entity: `nao`** (type: `nao_tool`)
Observations:
- `family: nao-gen`
- `category: nao_tool`
- `FluentNao HTTP bridge — Python 2.7 server in Docker on port 5050, evals Python against a live nao object connected to a NAO robot`
- `Send commands: curl -s -X POST http://localhost:5050/exec -d "<python code>"`
- `Response format: {"ok": true, "result": "<value>"} on success, {"ok": false, "error": "<message>"} on failure`
- `Hot reload: curl -s -X POST http://localhost:5050/reload`
- `Event long polling: curl -s "http://localhost:5050/events?timeout=30"`
- `Audio upload: curl -X POST -H "X-Filename: sound.wav" --data-binary @sound.wav http://localhost:5050/audio`
- `Health check: curl -s http://localhost:5050/health`
- `Multi-line scripts use exec with result= variable for return values`
- `Fluent chaining API: nao.arms.up().elbows.straight().hands.open().go()`
- `IMPORTANT: Before using, load rules: find_memories_by_name(["nao_rule_general"])`
- One observation per method from nao.py: `method: say(text) -- speak text aloud via ALTextToSpeech`, `method: sit() -- move to seated posture`, etc. Extract all public methods.

## Step 3: Create abilities entity

**Entity: `nao:abilities`** (type: `nao_module`)
Observations:
- `family: nao-gen`
- `category: nao_module`
- `High-level composite behaviors that combine multiple subsystems`
- `source: <code_path>/oss/FluentNao/src/main/python/fluentnao/core/abilities.py`
- One observation per public method from abilities.py: `method: snap(message, filename) -- face-tracking photo triggered by head touch`, `method: hear(duration) -- record audio for N seconds`, `method: explore() -- visual sweep across positions`, etc.
- `IMPORTANT: Before using, load rules: find_memories_by_name(["nao_rule_general"])`

## Step 4: Create rule entity

**Entity: `nao_rule_general`** (type: `nao_rule`)
Observations:
- `family: nao-gen`
- `category: nao_rule`
- `Boot sequence -- Start the FluentNao Docker container: cd <code_path>/oss/FluentNao && NAO_IP=$NAO_IP make serve. Wait for health check: curl -s http://localhost:5050/health. Verify: curl -s -X POST http://localhost:5050/exec -d "nao.say('ready')".`
- `Command pattern -- All commands go through: curl -s -X POST http://localhost:5050/exec -d "<python code>". Single expressions are eval'd. Multi-line scripts use exec; set result= for return values.`
- `Safety -- Keep movement duration >= 1.5 seconds. End sessions with nao.sit() then nao.shutdown(). Use nao.be_still() before speech recognition. Never walk on elevated surfaces.`
- `playSine -- nao.env.audioPlayer.post.playSine(freq_hz, gain_0_100, pan, duration_s). MUST use .post. (non-blocking). Common freqs: C4=262, D4=294, E4=330, F4=349, G4=392, A4=440, B4=494, C5=523.`
- `Photos -- nao.camera.photo(name, resolution=2) saves PPM to /data/photos/. Convert with sips on host: sips -s format png ~/code/oss/FluentNao/data/photos/<name>.ppm --out /tmp/<name>.png. Read the PNG with the Read tool.`
- `Audio transcription -- Record with nao.abilities.hear(N). Poll /events for heard event. Transcribe on host: whisper ~/code/oss/FluentNao/data/audio/<file>.wav --model base --language en --output_format txt --output_dir /tmp/`
- `Event system -- Subscribe: nao.emit_events(nao.events.touch). Poll: curl -s "http://localhost:5050/events?timeout=30". Custom emit: nao.emit(event_name, data).`
- `LEDs -- Use nao.leds.eyes(hex) for eye color (tracks state for photo restore). Eye/Chest/Feet LEDs support full RGB. Ear/Head LEDs are blue intensity only.`
- `Module loading -- This entity has HAS_MODULE edges to every available module. To use a module, load it: find_memories_by_name(["nao:<module_name>"]). Module entities contain all method signatures. Do not load all modules at once — only load what you need for the current task.`
- `Available module categories -- Body: arms, elbows, wrists, hands, head, legs, feet. Senses: camera, audio, vision, people, sensors. Navigation: navigation, tracker, reach. Effects: leds. Abilities: abilities (composites). Low-level: env (ALModule proxies), memory_util (event subscriptions), broker (connection). SDK: sdk_motion (constants), sdk_vision (camera constants). Infrastructure: events (event name constants), joints, animations.`
- `Acknowledge: Do not start sensors or event subscriptions on boot unless the user asks. The robot should be quiet by default.`
- `Awareness priority -- When reacting to events, favor: 1) people and faces (greet, engage) 2) sounds and speech (turn toward, record) 3) movement (look, describe) 4) open spaces (look toward, describe — only move if confirmed on ground) 5) rest and observe (sit still, scan room)`
- `Awareness pacing -- Observe more than act. Pause 10-30 seconds between actions. Let events drive behavior. Vary intensity — sometimes a head turn is enough. Do not narrate everything — only speak when genuinely interesting.`
- `Safety rule loading -- On boot, also load find_memories_by_name(["nao_rule_safety"]) and acknowledge all safety observations as hard constraints for the session.`

## Step 5: Create safety rule entity

**Entity: `nao_rule_safety`** (type: `nao_rule`)
Observations:
- `family: nao-gen`
- `category: nao_rule`
- `On boot, stay seated and assess the environment first. Take a photo with nao.camera.snap_photo() or nao.abilities.explore() to see where you are.`
- `If robot appears on desk, table, or elevated surface — do NOT stand, walk, or make large movements. Ask user before attempting anything that could cause a fall.`
- `Keep movement duration at 1.5 seconds or above. Fast movements stress motors.`
- `Always end a session with nao.sit() then nao.shutdown() to put the robot in a safe resting position.`
- `After calling nao.relax(), modules may become unresponsive. Use nao.stiff() to wake them back up.`
- `Do not attempt walking commands while the robot is sitting. Stand first.`
- `When subscribing to events, always store event names for cleanup and unsubscribe later.`
- `nao.naoscript.run_script() swallows exceptions silently — never use it. Use direct eval via the bridge.`
- `Use nao.be_still() before speech recognition to prevent autonomous movements from interfering.`
- `Use nao.shutdown() when done to clean up subscriptions and prevent falls.`
- `IMPORTANT: These rules are hard constraints. Apply them to every command you send for the entire session.`

## Step 6: Create relations

Use `mcp__neo4j-mcp__create_relations`:
- `nao:abilities` BELONGS_TO `nao`
- `nao_rule_general` RULE_FOR `nao`
- `nao_rule_safety` RULE_FOR `nao`

Use `mcp__neo4j-mcp__create_relations`:
- `nao:abilities` BELONGS_TO `nao`
- `nao_rule_general` RULE_FOR `nao`
