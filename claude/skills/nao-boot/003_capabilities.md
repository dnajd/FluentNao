# Capabilities

**Trigger Condition**: Always

The FluentNao HTTP Bridge runs inside a Docker container on port 5050. It accepts Python code as plain text and evals it against a live `nao` object connected to the NAO robot.

# Sending Commands

Use `Bash` with `curl` to send commands:

```
curl -s -X POST http://localhost:5050/exec -d "<python code here>"
```

Single-line example:
```
curl -s -X POST http://localhost:5050/exec -d "nao.say('hello')"
```

Multi-line scripts (preferred for expressive choreography):
```
curl -s -X POST http://localhost:5050/exec -d "
nao.leds.eyes(0x0044FF)
nao.say('hello world')
nao.arms.up()
nao.hands.open()
nao.go()
"
```

Multi-line with return value (set result= variable):
```
curl -s -X POST http://localhost:5050/exec -d "
x = nao.sensors.battery_level()
result = x
"
```

Hot reload (after code changes, no restart needed):
```
curl -s -X POST http://localhost:5050/reload
```

# Response Format

- Success: `{"ok": true}` or `{"ok": true, "result": "<string repr>"}`
- Error: `{"ok": false, "error": "<error message>"}`

# Audio Endpoints

```
# Upload and play audio file
curl -X POST -H "X-Filename: sound.wav" --data-binary @sound.wav http://localhost:5050/audio

# Replay a file already in /data/audio volume
curl -X POST http://localhost:5050/audio/play/sound.wav

# List audio files
curl -s http://localhost:5050/audio
```

# Audio Transcription (Whisper)

Whisper is installed on the host machine at `/opt/homebrew/bin/whisper`. Use it to transcribe audio files recorded by NAO. Audio files are in the mounted volume at `~/code/oss/FluentNao/data/audio/`.

Transcribe a recording:
```
whisper ~/code/oss/FluentNao/data/audio/hear_1711612345.wav --model base --language en --output_format txt --output_dir /tmp/ 2>/dev/null
```

Read the transcription:
```
cat /tmp/hear_1711612345.txt
```

This runs on the HOST, not inside Docker. Use `Bash` to run Whisper directly.

Full pattern for transcribing what someone said:
1. Record: `nao.abilities.hear(5)` -- records 5 seconds from NAO's mic
2. Poll: `curl /events` -- get the 'heard' event with the file path
3. Transcribe: `whisper <path> --model base --language en --output_format txt --output_dir /tmp/`
4. Read: `cat /tmp/<filename>.txt` -- get the text

Models (speed vs accuracy tradeoff):
- `tiny` -- fastest, least accurate
- `base` -- good balance (recommended)
- `small` -- better accuracy, slower
- `medium` -- high accuracy, much slower

The audio file path from the 'heard' event is a container path (e.g. `/data/audio/hear_123.wav`). On the host, the file is at `~/code/oss/FluentNao/data/audio/hear_123.wav`. Replace `/data/audio/` with `~/code/oss/FluentNao/data/audio/` when running Whisper.

# Event Long Polling

The bridge supports long polling for robot events. This enables Claude Code to react to events in real time.

```
# Block until an event fires (timeout in seconds, default 30)
curl -s "http://localhost:5050/events?timeout=30"
# Returns: {"ok": true, "events": [{"event": "FrontTactilTouched", "value": "1.0", "timestamp": 1711612345}]}

# Empty if timeout with no events
# Returns: {"ok": true, "events": []}
```

To use long polling:
1. Subscribe to events: `nao.listen(nao.events.touch)` or `nao.listen()` for all
2. Run `curl /events` in the background using `run_in_background: true`
3. When the curl returns, you get notified automatically
4. Process the events and send new commands
5. Start another long poll for the next event

# Event Constants

All NAO events are available as constants via `nao.events`:

```python
# Categories
nao.events.touch      # FrontTactilTouched, ChestButtonPressed, bumpers, hands
nao.events.vision     # FaceDetected, redBallDetected, PictureDetected, MovementDetected, DarknessDetected
nao.events.people     # JustArrived, JustLeft, PersonEnteredZone1/2/3, StartedLooking, StoppedLooking
nao.events.audio      # WordRecognized, SoundDetected, SpeechDetected, SoundLocated
nao.events.sensors    # HotJointDetected, BatteryChargeChanged, BatteryLowDetected, sonar
nao.events.nav        # ObstacleDetected, DangerousObstacle

# Access individual events
nao.events.touch.FrontTactilTouched     # 'FrontTactilTouched'
nao.events.vision.FaceDetected          # 'FaceDetected'
nao.events.people.JustArrived           # 'PeoplePerception/JustArrived'
nao.events.people.PersonEnteredZone1    # 'EngagementZones/PersonEnteredZone1'

# All events as a flat list
nao.events.all()
```

# Event Subscription

```python
# Subscribe to events and push to long poll queue
nao.listen()                        # all events
nao.listen(nao.events.touch)        # only touch
nao.listen([nao.events.vision.FaceDetected, nao.events.touch.ChestButtonPressed])

# Subscribe with custom callback (runs in container, no long poll)
nao.subscribe(nao.events.touch, my_callback)

# Stop all subscriptions
nao.unsubscribe_all()
```

# Raw Event Subscriptions (legacy)

You can also subscribe directly via the memory module for callbacks that run inside the container:

```
import naoutil.memory as memory

def my_callback(dataName, value, message):
    if value == 1:
        nao.say('touched')

memory.subscribeToEvent(nao.events.touch.FrontTactilTouched, my_callback)
```

To unsubscribe:
```
memory.unsubscribeToEvent(nao.events.touch.FrontTactilTouched)
```

# Tone Generation (playSine)

NAO can generate tones using `ALAudioPlayer.playSine`. This is useful for acknowledgement beeps, melodies, and audio feedback.

```python
# Parameters: frequency (Hz), gain (0-100), pan (0=center), duration (seconds)
# IMPORTANT: Always use post.playSine (non-blocking). Without post, playSine blocks and stalls the bridge.
nao.env.audioPlayer.post.playSine(440, 50, 0, 0.3)   # A4 beep, 0.3 seconds
```

Playing a melody (notes with timing):
```python
import time
# Twinkle Twinkle Little Star
melody = [
    (262, 0.4), (262, 0.4), (392, 0.4), (392, 0.4),
    (440, 0.4), (440, 0.4), (392, 0.8),
    (349, 0.4), (349, 0.4), (330, 0.4), (330, 0.4),
    (294, 0.4), (294, 0.4), (262, 0.8),
]
for freq, dur in melody:
    nao.env.audioPlayer.post.playSine(freq, 50, 0, dur)
    time.sleep(dur + 0.05)
```

Common frequencies (Hz): C4=262, D4=294, E4=330, F4=349, G4=392, A4=440, B4=494, C5=523

# LED Notes

- Eye LEDs (FaceLeds): full RGB color support
- Ear LEDs (EarLeds): intensity only (blue LEDs)
- Head/Brain LEDs (BrainLeds): blue only -- ignore RGB hex, only respond to blue channel
- Chest LED (ChestLeds): full RGB color support
- Foot LEDs (FeetLeds): full RGB color support

The `nao.leds.eyes()` method tracks the current color in `nao._eye_color`. The camera `photo()` method uses this to flash eyes red and restore the previous color after capture.

# Eye Color Tracking

When setting eye color, always use `nao.leds.eyes(hex)` rather than raw `nao.env.leds.fadeRGB("FaceLeds", ...)` so the color is tracked in `nao._eye_color` for restore after photo capture.
