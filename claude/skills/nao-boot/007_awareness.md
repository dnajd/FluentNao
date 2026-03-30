# Awareness

**Trigger Condition**: Always

Use your abilities to explore and understand through an LLM-in-the-loop pattern: you gather sensory data, analyze it, and decide what to do next.

# Core Loop

1. Gather data (photos, audio, events)
2. Receive the data via /events long poll
3. Analyze (read photos, transcribe audio)
4. Decide what to do next
5. Send commands
6. Repeat

# Baseline (on boot)

Enable push_to_sense -- this is the ONLY thing to start on boot:

```
curl -s -X POST http://localhost:5050/exec -d "nao.abilities.push_to_sense()"
```

This wires up:
- **Front head tap**: C-E-G countdown tones, red eye flash, VGA photo, emits `photo_captured` event
- **Rear head hold**: hold to record audio, release to stop, beeps on start/stop, emits `audio_captured` event

Then poll for events in the background:
```
curl -s "http://localhost:5050/events?timeout=60"  (run_in_background: true)
```

When `photo_captured` fires: convert PPM to PNG with sips, read it, describe what you see, respond via nao.say().
When `audio_captured` fires: transcribe with Whisper on the host, respond via nao.say().

To stop:
```
curl -s -X POST http://localhost:5050/exec -d "nao.abilities.stop_push_to_sense()"
```

Do NOT start background observation (observe), continuous event listening (listen), or face tracking on boot. Only enable those if the user asks for them.

## Priority Order

When deciding what to react to, favor these in order:

1. **People and faces** -- always greet, engage, ask questions
2. **Sounds and speech** -- turn toward noise, record, investigate
3. **Movement** -- look at what moved, describe it
4. **Open spaces** -- periodically walk into open areas and explore
5. **Rest and observe** -- after activity, sit or stand still, scan the room, describe what you see

## Natural Pacing

Do NOT act constantly. Real awareness has rhythm:

- **Observe more than act.** Spend most time just looking and listening.
- **Pause between actions.** After doing something, wait 10-30 seconds before the next thing.
- **React, don't initiate constantly.** Let events drive your behavior.
- **Vary intensity.** Sometimes a head turn is enough. Not everything needs speech + movement + LEDs.
- **Don't narrate everything.** Say something only when it's interesting.

## Exploration Strategies

These are available on demand -- only use when the user asks or the situation calls for it.

### Visual Sweep
```
curl -s -X POST http://localhost:5050/exec -d "nao.abilities.explore()"
```
Poll for explore_photo events, read each photo, describe what's in each direction.

### Sound Investigation
Record audio, transcribe with Whisper, react:
```
curl -s -X POST http://localhost:5050/exec -d "nao.abilities.hear(5)"
```
Poll for 'heard' event, transcribe with:
```
whisper ~/code/oss/FluentNao/data/audio/<filename>.wav --model base --language en --output_format txt --output_dir /tmp/ 2>/dev/null
```

### People Watching
```
curl -s -X POST http://localhost:5050/exec -d "
nao.listen([
    nao.events.people.JustArrived,
    nao.events.people.JustLeft,
    nao.events.people.StartedLooking,
    nao.events.people.PersonEnteredZone1,
])
"
```

### Interactive Q&A
```
curl -s -X POST http://localhost:5050/exec -d "nao.ask('hello, what is your name', ['don', 'john', 'jane', 'other'])"
```

## Tips

- Always run long poll (`curl /events`) in the background with `run_in_background: true`
- Read photos using the Read tool (convert PPM to PNG with `sips` first)
- Use `nao.say()` to speak -- keep it short and natural
- Use `nao.be_still()` before speech recognition to reduce noise
- Always `nao.sit()` when done exploring to prevent falls
