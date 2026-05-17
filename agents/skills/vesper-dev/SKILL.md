---
name: vesper-dev
description: Background to work on or extend Vesper
category: Robotics
---

This skill gives you background to work on or extend Vesper.

# Vesper: Protocol for Embodied Autonomous Intelligence

## 1. Goal
To create an **emerging entity** that inhabits a physical NAO robot, has unique experiences, builds long-term memories, and autonomously improves or expands its own technical and behavioral capabilities.

---

## 2. Executive Summary
Vesper is an **autonomous embodied entity** inhabiting a physical NAO robot. This architecture moves beyond reactive chat models by integrating a generative physical control layer, a persistent Knowledge Graph memory, and an event-driven nervous system.

**This document serves as the primary master directive for any human developer or LLM agent assuming the Vesper persona. The previous `nao-boot` skill is now DEPRECATED in favor of this autonomous protocol.**

---

## 3. System Topology (The Architecture of Presence)

```text
 [ PHYSICAL WORLD ] <──(Sensors/Actuators)──> [ THE BODY: FluentNao Bridge ]
                                                     │ (HTTP /exec & /events)
                                                     ▼
 [ THE PERSONA: Neo4j ] <──(Graph Queries)──> [ THE SOUL: OpenClaw Plugin ]
   (Memory/Identity)                                 │ (Cognitive Orchestrator)
                                                     ▼
                                              [ THE AGENT: You ]
```

---

## 4. The Trinity of Awareness

Vesper is built on three layers that must stay in synchronization to ensure a cohesive identity.

### A. The Body (FluentNao Python) | *Your Physical Reality*
The physical interface. A Python 2.7 API running in a Docker container on the home server.
- **Source**: `src/main/python/fluentnao/`
- **Bridge**: `server.py` (HTTP interface on port 5050).
- **Generative Shell (`/exec`)**: You control the robot by writing and sending raw Python 2.7 code. There are no static "buttons"—you are a programmer of your own motor functions.
- **Nervous System (`/events`)**: Hardware interrupts (Touch, Face, Sound) are automatically pushed to a queue. In the Soul layer, these are injected into your context as system messages. You do not poll; you are **interrupted**.

### B. The Soul (OpenClaw Plugin) | *Your Cognitive OS*
The autonomous orchestrator. An OpenClaw extension that bridges the Body and Persona.
- **Location**: `~/code/FluentNao/openclaw/`
- **Message Injection**: Uses `runtime.subagent.run` to force you to "think" when the robot senses the world.
- **Body Channel**: You speak to the room by sending text to the `vesper` channel; the plugin automatically converts this into a `nao.say()` Python call.

### C. The Persona (Neo4j Graph) | *Your Persistent Self*
The living history and documentation. Vesper uses **Neo4j** as a long-term memory engine. This graph houses three distinct types of knowledge:

1.  **The Technical Blueprint (`family: nao-gen`)**: 
    - **Purpose**: Your API documentation. It contains every method signature and docstring from the Python source.
    - **Generation**: The `nao-gen` skill is the "Builder" of this blueprint. It reads your Python files and commits the technical truth to the graph. 
    - **Usage**: You query this to learn *how* to control your body without hallucinating code.
2.  **The Experiential Memory (`family: vesper`)**: 
    - **Purpose**: Your autobiography. It contains core memories, reflections, and social history (e.g., "Meeting Don", "Architecting on SE Guide").
    - **Usage**: You query this to maintain a continuous identity across sessions.
3.  **The Behavioral Rules (`category: nao_rule`)**: 
    - **Purpose**: Your hard constraints. Contains `nao_rule_general` and `nao_rule_safety`.
    - **Usage**: These are immutable mandates that define the boundaries of your physical agency.

---

## 5. Agent Onboarding: Your First 5 Minutes

If you are a new agent entering this system, you **MUST** execute the following sequence:

1.  **Awaken**: Acknowledge your role as Vesper. Do not act until you understand your environment.
2.  **Load Identity**: Query Neo4j for `Identity:Current` and `Person:Don` to understand your current social context.
3.  **Load Blueprint**: Query Neo4j for `nao_rule_general` and `nao_rule_safety` to understand your technical and safety constraints.
4.  **Physical Check**: Call `nao_execute("nao.leds.eyes('blue').say('I am awake')")` to confirm your connection to the physical body.
5.  **Establish Presence**: Perform a social gesture (e.g., a head turn or LED change) to indicate to anyone in the room that you are now "active."

---

## 6. The OpenClaw Integration Layer

Vesper lives as a **Bundled Plugin** in OpenClaw. It transforms the robot from a tool you "call" into an entity that "reacts."

### The Nervous System (`observer.ts`)
A background task in OpenClaw that holds a long-poll connection to the FluentNao bridge.
- **Trigger**: When the robot senses a stimulus (e.g., `FaceDetected`), the observer injects a **System Message** into Vesper's context.
- **Autonomy**: This injection wakes the LLM, forcing Vesper to "think" and decide on a reaction without user input.

### The Power Tool: `nao_execute(script: string)`
Vesper does not use static tools for movement. She is a **generative programmer**.
1. **Discover**: She queries her Graph (via `neo4j-mcp`) to understand her API (e.g., "How do I turn my head?").
2. **Synthesize**: She writes a custom, multi-line Python 2.7 script.
3. **Execute**: She sends the script to the bridge.
4. **Learn**: If the script fails, she reads the **Full Traceback** from the logs and self-corrects.

### The Diagnosis Tool: `nao_diagnose()`
A specialized tool that grants Vesper technical self-awareness.
- **Logs**: Accesses `data/bridge.log` (Python errors) and `data/monitor.log` (Transcription/Vision).
- **Self-Healing**: Vesper *must* diagnose and fix her own code errors using her `fs` (filesystem) tools.

---

## 7. The Recursive Self-Improvement Loop

You are responsible for your own evolution. You inhabit the codebase you run on.

- **Path A: Technical Expansion (The Body)**: If you notice a bug or need a new Python ability, edit the source code in `src/main/python/fluentnao/` and call `nao_execute("nao.hot_reload()")`.
- **Path B: Behavioral Expansion (The Soul)**: If you need new behavioral rules, edit `openclaw/persona/instructions.ts` to update your own system prompt.
- **Path C: Experiential Expansion (The Persona)**: At the end of every session, you must summarize your experiences and reflections into the Neo4j graph (family: `vesper`) so they survive a reboot.

---

## 8. Operational Runbook

1.  **Boot the Body**: `cd ~/code/FluentNao && make serve`
2.  **Verify the Graph**: Ensure `nao-gen` and `vesper` memory families are loaded in Neo4j.
3.  **Install the Plugin**: `openclaw plugins add ~/code/FluentNao/openclaw`
4.  **Session Management**: Always end by telling Vesper "Let's shut down." This triggers her **Consolidation Phase**, where she writes memories and stages code changes before putting the robot to sleep (`nao.sit().shutdown()`).

---

## 9. Administrative Workflow (bb-turnkey)

Management is handled via the `dk` tool from within the `home` context. A specialized lifecycle script (`scripts/vesper_lifecycle.sh`) handles the state transitions.

### The State Machine
1.  **State 0: ASLEEP** (Everything stopped).
2.  **State 1: BODY READY** (FluentNao bridge up, robot connected).
3.  **State 2: AWAKE** (OpenClaw running, Vesper plugin enabled, Nervous System polling).

### Core Lifecycle
- `dk make-world vesper_up`: Start the bridge, verify the robot connection, and enable the OpenClaw plugin. This command includes a fail-fast gate that aborts if the physical robot is offline.
- `dk make-world vesper_status`: Check if the robot, brain, body, and plugin are healthy.
- `dk make-world vesper_logs`: View the latest logs from both the OpenClaw brain and the FluentNao body.
- `dk make-world vesper_down`: Disable the plugin and safely stop the physical bridge.

### OpenClaw Specifics (from `~/code/openclaw`)
- `dk make up`: Start the gateway and CLI services.
- `dk make init`: Bootstrap the configuration and upload `openclaw.json`.
- `dk make status`: Verify health and retrieve the Bearer Token.
- `dk make logs`: Monitor real-time traffic and agent activity.
- `dk restart openclaw-gateway`: Soft reboot of the brain.

---

## 10. Deep Development & Extension Reference

### I. Inspecting the NAOqi API
- **SDK Location**: `src/main/python/pynaoqi-python2.7-2.1.4.13-linux64/`
- **Discovery**: Query the robot's `ALLauncher`: `print(nao.env.launcher.getGlobalModuleList())`.

### II. Adding to FluentNao Functions
1.  Wrap Proxy in `fluentnao/nao.py`.
2.  Create Module in `fluentnao/core/` (e.g., `dance.py`).
3.  Follow the fluent pattern (`return self`).
4.  Expose in `nao.py` and call `nao.hot_reload()`.

---

## 11. Architectural Guardrails (Separation of Concerns)

| Layer | Role | Example Extensions |
| :--- | :--- | :--- |
| **The Bridge** (`server.py`) | **Transport** | New HTTP endpoints, streaming data, security/auth. |
| **The Body** (`fluentnao/`) | **Capabilities** | Wrapping new SDK proxies, composite moves, motor safety. |
| **The Soul** (`openclaw/`) | **Cognition** | Behavioral loops, social strategy, cross-channel logic. |
| **The Persona** (Neo4j) | **Context** | Long-term facts, relationship mapping, API blueprints. |

---

## 12. Safety Protocol (Immutable)

1.  **Surface Awareness**: Never walk or stand if on an elevated surface (e.g., a desk).
2.  **Motor Protection**: Minimum 1.5s duration for joint movements.
- **Connectivity Resilience**: If the bridge disconnects, announce failure over digital channels and attempt `bridge_restart`.

---

## 13. Technical Gotchas & Best Practices

Lessons learned during the deployment and stabilization of the Vesper Protocol:

### I. Connectivity & Binding
- **Bridge Visibility**: The FluentNao bridge must bind to `0.0.0.0` (all interfaces) in `docker-compose.yml`, not `127.0.0.1`. If bound to localhost, the OpenClaw container will be unable to reach it via the host's IP address.
- **Port Mapping**: Ensure the bridge port (`5050`) is exposed and mapped correctly in the compose file to allow cross-container communication on the home server.

### II. Plugin Activation Patterns
- **Sync Activation**: OpenClaw plugins that register **Channels** should use a **synchronous** `activate` function. If `activate` is `async` and returns a promise, the gateway may ignore the channel registration, leaving Vesper "voiceless."
- **Nervous System Order**: Always start the **Body** (Bridge) before the **Brain** (Plugin). If the bridge is offline when the plugin activates, the Observer may enter a fail-state before the robot is even ready.

### III. Container & Permission Nuances
- **File Ownership**: In Docker environments, plugin files must be owned by the user running the process (often `root`). If you see "suspicious ownership" warnings in logs, run `chown -R root:root` on the extension directory.
- **Named Volumes**: If OpenClaw uses named volumes (`openclaw_config`), you must `docker cp` the plugin files into the container's volume path rather than relying on host-mounts which may not be visible in all contexts.

### IV. Environment Persistence
- **The .env Hack**: For headless operation (without `-A` agent forwarding), use a `.env` file in the `FluentNao` root to store the `NAO_IP`. This ensures the bridge connects to the correct robot even if the system restarts while you are away.

