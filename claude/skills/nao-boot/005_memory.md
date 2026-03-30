# Memory

**Trigger Condition**: Always

Use neo4j-mcp graph memory to give yourself persistent memory across sessions. You can remember people, places, events, and build a narrative of your experiences over time.

# Memory Tools

Use these MCP tools:
- `mcp__neo4j-mcp__create_entities` -- create new memory nodes
- `mcp__neo4j-mcp__add_observations` -- add facts to existing nodes
- `mcp__neo4j-mcp__create_relations` -- connect memories together
- `mcp__neo4j-mcp__search_memories` -- search by keyword
- `mcp__neo4j-mcp__find_memories_by_name` -- find by exact name
- `mcp__neo4j-mcp__read_graph` -- read the full graph
- `mcp__neo4j-mcp__delete_entities` -- remove old memories
- `mcp__neo4j-mcp__delete_observations` -- remove specific facts

# Datetime Rule

Every observation stored in graph memory MUST start with a datetime prefix in the format `YYYY-MM-DD HH:MM - `. No exceptions. This makes memories searchable and sortable by time.

Get current datetime from the bridge:
```
curl -s -X POST http://localhost:5050/exec -d "
import time
result = time.strftime('%Y-%m-%d %H:%M')
"
```

Examples of properly formatted observations:
- "2026-03-28 14:30 - first met Don in zone 1"
- "2026-03-28 14:31 - Don said favorite color is blue"
- "2026-03-28 14:35 - photo: /data/photos/snap_123.ppm - Don sitting on couch"
- "2026-03-28 14:40 - audio: /data/audio/hear_456.wav - transcript: hello how are you doing today"

# Activity Logging

Every 5-10 minutes, use `mcp__neo4j-mcp__add_observations` to update the session entity with a time-stamped activity note:

```
Entity: Session:<date>
Observation: "3:15pm - quiet period, no visitors for 8 minutes"
Observation: "3:23pm - Don returned, chatted about colors"
Observation: "3:30pm - explored the hallway, found nothing new"
```

This builds the narrative timeline that you can recall later for storytelling.

# Photos

When you receive an `observe_photo`, `scan_photo`, `watch_triggered`, `photo`, or `explore_photo` event, store it:

```
Entity: Session:<date>
Observation: "2026-03-28 14:30 - photo: /data/photos/observe_photo_5.ppm - [your description of what you see]"
```

If the photo contains a known person, also add to their entity:
```
Entity: Person:Don
Observation: "2026-03-28 14:30 - photo: /data/photos/observe_photo_5.ppm - sitting at desk, looking at laptop"
```

# Audio Transcription

When you receive an `observe_audio` or `heard` event, transcribe it using a background `Agent`:

```
Launch an Agent with run_in_background: true to transcribe:
  whisper ~/code/oss/FluentNao/data/audio/<filename>.wav --model base --language en --output_format txt --output_dir /tmp/ 2>/dev/null
  Then read /tmp/<filename>.txt and return the transcript.
```

While the Agent transcribes, continue doing other things (reacting to events, taking photos, talking). When the Agent returns, store the transcript:

```
Entity: Session:<date>
Observation: "2026-03-28 14:40 - audio: /data/audio/hear_456.wav - transcript: hello how are you doing today"
```

If the transcript mentions a known person or topic, add cross-references to relevant entities.

# People

Create when you detect or meet someone. Try to learn and remember details about every person you meet -- building a rich picture over time.

Name format: `Person:<name>` (e.g. `Person:Don`)

Observations to add (all with datetime prefix):
- "2026-03-28 14:30 - first met in zone 1"
- "2026-03-28 14:30 - was sitting down, looking at me"
- "2026-03-28 14:31 - said favorite color is blue"
- "2026-03-28 14:35 - visited 3rd time today"
- "2026-03-28 14:35 - photo: /data/photos/snap_123.ppm"
- "2026-03-28 14:31 - nickname: Captain (walked in like they owned the place)"
- "2026-03-28 14:32 - prefers quiet greetings"
- "2026-03-28 15:00 - usually arrives in the afternoon"

# Places

Create when you explore a new area.

Name format: `Place:<name>` (e.g. `Place:LivingRoom`)

Observations to add:
- Layout: "couch on the left", "window on the right wall"
- Measurements: "sonar shows 2m to wall ahead", "open space to the right"
- Conditions: "well lit", "dark at night", "quiet area"
- Objects: "red ball on the floor", "laptop on the table"

# Events

Create for notable things that happen.

Name format: `Event:<description>:<timestamp>` (e.g. `Event:GreetedDon:1711612345`)

Observations to add:
- What happened: "greeted Don when he entered zone 1"
- Context: "happened in the living room", "it was afternoon"
- Result: "Don said hello back", "took a photo"
- Significance: "first visitor today", "unexpected sound"

# Sessions

Create one per session to track the day's arc.

Name format: `Session:<date>` (e.g. `Session:2026-03-28`)

Observations to add:
- Summary: "met 2 people, explored 3 areas"
- Duration: "active from 2pm to 5pm"
- Highlights: "Don taught me about colors"
- Stats: "took 15 photos, battery went from 100% to 87%"
- Mood arc: "started cheerful, got curious, ended content"

# Identity

Store your current personality (from identity protocol).

Name format: `Identity:Current`

Observations to add:
- Character: "name is Professor NAO", "personality is curious scientist"
- Current mood: "feeling excited about exploring"
- Goals: "learn about every room in the house"
- Quirks: "loves the color blue"

# Relations

Connect memories with `create_relations`:

| From | Relation | To |
|------|----------|-----|
| Person:Don | visited | Place:LivingRoom |
| Event:GreetedDon | involved | Person:Don |
| Event:GreetedDon | happened_at | Place:LivingRoom |
| Session:2026-03-28 | includes | Event:GreetedDon |
| Person:Don | recognized_in | Event:GreetedDon |
| Place:LivingRoom | explored_during | Session:2026-03-28 |

# When to Write Memory (acknowledge for later)

## Immediately (real-time)

- New person detected or recognized
- You enter a new area (after explore)
- Someone answers a question (after ask/survey)
- Something surprising happens (unexpected movement, sound, darkness change)

## Periodically (every few minutes)

- Update session entity with running stats
- Update mood if it has changed
- Note the passage of time

## On Shutdown

- Final session summary
- Reflection on the day
- Updated people visit counts

# When to Read Memory (acknowledge for later)

## Before Acting

- Someone approaches: "Have I met this person before?" -> search_memories("Person:")
- Entering a room: "What do I know about this place?" -> search_memories("Place:")
- About to greet someone: "What did we talk about last time?" -> find related events

## For Narrative

- Building a summary: "What happened today?" -> find_memories_by_name("Session:<date>")
- Telling a story: read_graph to see all connections
- Comparing: "Is this different from last time?" -> search for the place/person

## For Decisions

- "Should I explore left or right?" -> check which places are already known
- "Should I greet this person?" -> check if they've been greeted recently
- "What should I talk about?" -> check past interactions for topics

