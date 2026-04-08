# Protocol: Create Env, Utility, and SDK Entities

**Trigger Condition**: After core entities exist — this is Step 2 of nao-gen

## Family Tag
Every entity created in this file includes `"family: nao-gen"` as an observation.

## Goal

Read the naoutil modules (naoenv, memory, broker) and the pynaoqi SDK to create entities for the low-level proxy layer and SDK constants.

## Step 1: Read naoutil source files

Use `Read` on these files:
- `<code_path>/oss/FluentNao/src/main/python/naoutil/naoenv.py`
- `<code_path>/oss/FluentNao/src/main/python/naoutil/memory.py`
- `<code_path>/oss/FluentNao/src/main/python/naoutil/broker.py`

## Step 2: Create nao:env entity

The `nao.env` proxy layer is the gateway to all raw ALModule access. This is critical — it's how you call anything the fluent API doesn't cover.

**Entity: `nao:env`** (type: `nao_module`)
Observations:
- `family: nao-gen`
- `category: nao_module`
- `Proxy layer for raw NAOqi ALModule access via nao.env.<proxy_short_name>`
- `source: <code_path>/oss/FluentNao/src/main/python/naoutil/naoenv.py`
- `Access pattern: nao.env.<short_name>.<method>() for synchronous, nao.env.<short_name>.post.<method>() for non-blocking`
- Extract the PROXY_SHORT_NAMES dict from naoenv.py and create one observation per mapping: `proxy: motion -> ALMotion`, `proxy: audioPlayer -> ALAudioPlayer`, `proxy: leds -> ALLeds`, `proxy: tts -> ALTextToSpeech`, etc. Include ALL entries.
- `Common usage: nao.env.motion.setAngles(names, angles, speed) -- direct joint control`
- `Common usage: nao.env.audioPlayer.post.playSine(freq, gain, pan, duration) -- tone generation (MUST use .post.)`
- `Common usage: nao.env.leds.fadeRGB("FaceLeds", hex_color, duration) -- direct LED control`
- `Common usage: nao.env.tts.say("text") -- direct text-to-speech`
- `Common usage: nao.env.motion.stiffnessInterpolation(names, stiffness, time) -- motor stiffness control`
- `IMPORTANT: Before using, load rules: find_memories_by_name(["nao_rule_general"])`

## Step 3: Create nao:memory_util entity

**Entity: `nao:memory_util`** (type: `nao_module`)
Observations:
- `family: nao-gen`
- `category: nao_module`
- `Event subscription helpers for raw ALMemory events`
- `source: <code_path>/oss/FluentNao/src/main/python/naoutil/memory.py`
- One observation per public function from the file: `method: subscribeToEvent(event_name, callback) -- subscribe to an ALMemory event with a Python callback`, etc.
- `IMPORTANT: Before using, load rules: find_memories_by_name(["nao_rule_general"])`

## Step 4: Create nao:broker entity

**Entity: `nao:broker`** (type: `nao_module`)
Observations:
- `family: nao-gen`
- `category: nao_module`
- `ALBroker connection setup and management`
- `source: <code_path>/oss/FluentNao/src/main/python/naoutil/broker.py`
- One observation per public function/class
- `IMPORTANT: Before using, load rules: find_memories_by_name(["nao_rule_general"])`

## Step 5: Read SDK source files

Use `Read` on these files:
- `<code_path>/oss/FluentNao/src/main/python/pynaoqi-python2.7-2.1.4.13-linux64/motion.py`
- `<code_path>/oss/FluentNao/src/main/python/pynaoqi-python2.7-2.1.4.13-linux64/vision_definitions.py`

## Step 6: Create SDK entities

**Entity: `nao:sdk_motion`** (type: `nao_module`)
Observations:
- `family: nao-gen`
- `category: nao_module`
- `NAOqi motion SDK constants — frame references, axis masks, and unit conversion`
- `source: <code_path>/oss/FluentNao/src/main/python/pynaoqi-python2.7-2.1.4.13-linux64/motion.py`
- One observation per constant or constant group: `const: FRAME_TORSO = 0`, `const: FRAME_WORLD = 1`, `const: FRAME_ROBOT = 2`, `const: AXIS_MASK_ALL = 63`, `const: TO_RAD = 0.0174533`, `const: TO_DEG = 57.2957795`, etc.
- `Used by: nao.env.motion methods that take frame or axis parameters`
- `IMPORTANT: Before using, load rules: find_memories_by_name(["nao_rule_general"])`

**Entity: `nao:sdk_vision`** (type: `nao_module`)
Observations:
- `family: nao-gen`
- `category: nao_module`
- `NAOqi camera resolution and color space constants`
- `source: <code_path>/oss/FluentNao/src/main/python/pynaoqi-python2.7-2.1.4.13-linux64/vision_definitions.py`
- One observation per constant/group: resolution values (QQVGA=0, QVGA=1, VGA=2, etc.), color spaces (kYUV422=0, kRGB=11, etc.)
- `Used by: nao.camera.photo() resolution parameter, nao.env.videoDevice methods`
- `IMPORTANT: Before using, load rules: find_memories_by_name(["nao_rule_general"])`

## Step 7: Create relations

Use `mcp__neo4j-mcp__create_relations`:
- `nao:env` BELONGS_TO `nao`
- `nao:memory_util` BELONGS_TO `nao`
- `nao:broker` BELONGS_TO `nao`
- `nao:sdk_motion` BELONGS_TO `nao`
- `nao:sdk_vision` BELONGS_TO `nao`
