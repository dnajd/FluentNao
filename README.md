# FluentNao

A fluent Python API for controlling a NAO robot. Send commands through an HTTP bridge running in Docker -- no SDK installation required on the host.

## Requirements

- Docker
- A NAO robot on the same network

## Quick Start

```bash
# Set your NAO's IP (press chest button to hear it)
export NAO_IP=192.168.68.96

# Build the Docker image
make init

# Set up SSH keys for audio/file transfer (one-time)
make ssh-setup

# Start the HTTP bridge server
make serve

# Send a command
curl -s -X POST http://localhost:5050/exec -d "nao.say('hello world')"
```

## Make Targets

| Target | Description |
|--------|-------------|
| `init` | Build the Docker image |
| `ssh-setup` | Generate PEM key and copy to NAO for passwordless SSH |
| `serve` | Run HTTP bridge server on port 5050 |
| `up` | Run interactive Python shell |
| `bash` | Run bash prompt in container |

## HTTP Bridge

The bridge accepts Python code as text and executes it with a live `nao` object.

```bash
# Health check
curl -s http://localhost:5050/health

# Single command
curl -s -X POST http://localhost:5050/exec -d "nao.say('hello')"

# Multi-line script
curl -s -X POST http://localhost:5050/exec -d "
nao.stiff()
nao.stand_init()
nao.arms.up()
nao.go()
"

# Get return values (set result= variable)
curl -s -X POST http://localhost:5050/exec -d "
x = nao.sensors.battery_level()
result = x
"

# Hot reload all modules (no restart needed)
curl -s -X POST http://localhost:5050/reload

# Upload and play audio
curl -X POST -H "X-Filename: sound.wav" --data-binary @sound.wav http://localhost:5050/audio

# Play existing audio file
curl -X POST http://localhost:5050/audio/play/sound.wav

# List audio files
curl -s http://localhost:5050/audio
```

## Docker Volumes

| Host Path | Container Path | Purpose |
|-----------|---------------|---------|
| `./photos` | `/photos` | Photo captures (PPM format) |
| `./video` | `/video` | Video frames and MP4 output |
| `./audio` | `/audio` | Audio recordings (WAV) |
| `./object_detection` | `/object_detection` | Images for object recognition learning |
| `~/.ssh` | `/root/.ssh` (read-only) | SSH keys for NAO file transfer |

## API Reference

### Speech

```python
nao.say('hello')                    # non-blocking
nao.say_and_block('hello')          # waits until speech finishes
nao.animate_say('^start(animations/Stand/Gestures/Hey_1) hello')
```

### Postures

```python
nao.stiff()                         # enable motors (required before movement)
nao.stand_init()                    # standing ready position
nao.sit()                           # sit down (safe resting position)
nao.crouch()                        # crouch position
nao.relax()                         # disable all motors
nao.rest()                          # rest mode
```

### Body Movement

All body part methods queue movements. Call `go()` to execute and return to `nao` for chaining.

```python
# Arms: up, down, forward, out, back (left_/right_ variants)
nao.arms.up().go()
nao.arms.left_forward(2, 15).right_out().go()

# Chain across body parts
nao.arms.up().elbows.bent().hands.open().go()

# Elbows: bent, straight, turn_up, turn_down, turn_in
nao.elbows.bent().go()

# Wrists: center, turn_out, turn_in
nao.wrists.turn_out().go()

# Hands: open, close
nao.hands.open().go()

# Head: left, right, forward (yaw), up, down, center (pitch)
nao.head.left().go()

# Legs: out, in, forward, back, up, down, knee_up, knee_bent
nao.legs.left_out().go()

# Feet: point_toes, raise_toes, turn_out, turn_in, center
nao.feet.point_toes().go()
```

### Duration and Offsets

```python
nao.set_duration(1.5)               # default time for all movements
nao.arms.out(4)                     # override: 4 seconds for this move
nao.arms.up(0, -30)                 # offset: subtract 30 degrees from target
```

### LEDs

```python
nao.leds.eyes(0xFF0000)             # red eyes
nao.leds.chest(0x00FF00)            # green chest
nao.leds.ears(0x0000FF)             # blue ears
nao.leds.head(0xFFFFFF)             # white head
nao.leds.feet(0xFF00FF)             # purple feet
nao.leds.off()                      # all off
```

### Camera

```python
nao.camera.photo('snapshot')                        # save to /photos/
nao.camera.photo('hires', resolution=2)             # VGA 640x480
nao.camera.bottom().photo('floor')                  # bottom camera

# Video recording (burst frames -> stitch to MP4)
nao.camera.start_recording('clip', fps=15)
nao.camera.stop_recording()
nao.camera.to_video()                               # -> /video/clip.mp4

# Combined audio + video recording (fluent chain)
nao.video('demo').say_and_block('hello').arms.up().go().stop_video()

# Face tracking
nao.camera.track_face()                             # head follows face
nao.camera.track_face_whole_body()                  # head + torso
nao.camera.stop_tracking()

# Cleanup
nao.camera.clear_photos()
nao.camera.clear_video()
```

### Audio

```python
# Playback
nao.audio.play('http://example.com/sound.mp3')
nao.audio.play_file('recording.wav')               # from /audio/ volume

# Volume
nao.audio.set_volume(50)
nao.audio.get_volume()
nao.audio.mute()
nao.audio.unmute()

# Record from NAO's microphones (pulled to /audio/, deleted from NAO)
nao.audio.start_recording('meeting')
path = nao.audio.stop_recording()                   # returns '/audio/meeting.wav'

# Speech recognition
def on_word(words):
    print(words)                                    # {'hello': 0.85}
nao.audio.listen_for(['hello', 'goodbye'], on_word)
nao.audio.stop_listening()

# Sound direction
nao.audio.sound_direction(sensitivity=0.5, timeout=3)

# Cleanup
nao.audio.clear()
```

### Vision

```python
# Red ball tracking
nao.vision.track_ball()
pos = nao.vision.ball_position()
nao.vision.stop_tracking_ball()

# Object recognition (NAO takes photo with countdown)
nao.vision.learn_object('coffee_mug')

# Learn from files in /object_detection/ folder
nao.vision.learn_all()

# React to recognized objects
def spotted(data):
    nao.say('I see it')
nao.vision.on_object(spotted)
nao.vision.stop_on_object()

# Movement and darkness detection
nao.vision.on_movement(callback)
nao.vision.on_darkness(callback)
nao.vision.is_dark()

# Forget learned objects
nao.vision.forget_all_objects()
```

### People Perception

```python
# Engagement zones: zone1 (0-1.5m), zone2 (1.5-2.5m), zone3 (2.5m+)
nao.people.on_zone1(lambda v: nao.say('you are close'))
nao.people.on_zone2(lambda v: nao.say('conversation distance'))
nao.people.on_approached(callback)
nao.people.on_moved_away(callback)

# Gaze detection
nao.people.on_looking(lambda v: nao.say('I see you'))
nao.people.on_not_looking(callback)

# Arrival/departure
nao.people.on_person_arrived(callback)
nao.people.on_person_left(callback)
nao.people.people_count()

# Sitting detection
nao.people.on_sat_down(callback)
nao.people.on_stood_up(callback)

# Stop everything
nao.people.stop_all()
```

### Sensors

```python
# Touch events
nao.sensors.on_head(lambda e: nao.say('touched my head'))
nao.sensors.on_bumper(lambda e: nao.say('ouch'))
nao.sensors.on_chest_button(callback)
nao.sensors.on_hand(callback)
nao.sensors.stop_all_touch()

# Battery
nao.sensors.battery_level()                         # 0-100
nao.sensors.is_charging()                           # True/False
nao.sensors.battery_temperature()

# Motor temperature
nao.sensors.temperatures()                          # all 26 joints
nao.sensors.hottest_joint()                         # ('LShoulderRoll', 64.0)
```

### Navigation

```python
# Precise movement (meters and radians)
nao.navigation.move_to(1.0, 0, 0)                  # forward 1 meter
nao.navigation.move_to(0, 0, 1.5708)               # turn 90 degrees left

# Obstacle-avoiding navigation
nao.navigation.navigate_to(2.0, 1.0)

# Learn and return to home position
nao.navigation.learn_home()                         # panoramic scan
nao.navigation.go_home()
nao.navigation.is_home()

# Map persistence
nao.navigation.save_map('office')
nao.navigation.load_map('office')
```

### Tracker (unified tracking)

```python
# Track with head only
nao.tracker.face()
nao.tracker.red_ball()
nao.tracker.people()

# Track with whole body
nao.tracker.face(nao.tracker.WHOLE_BODY)

# Follow (walk toward target)
nao.tracker.follow_face()
nao.tracker.follow_people()

# Point and look
nao.tracker.look_at(1.0, 0.0, 0.5)
nao.tracker.point_at(1.0, 0.0, 0.3)

nao.tracker.stop()
```

### Reach (3D cartesian control)

```python
# Get hand position in 3D space
pos = nao.reach.position('RArm')                    # [x, y, z, wx, wy, wz]

# Move to absolute position (meters)
nao.reach.to('RArm', 0.2, -0.1, 0.1)

# Relative movement
nao.reach.forward('RArm', 0.1)
nao.reach.up('RArm', 0.05)
nao.reach.left('LArm', 0.05)

# Trace a path through waypoints
nao.reach.trace('RArm', [
    (0.2, -0.1, 0.1),
    (0.2, -0.1, 0.2),
    (0.2, -0.2, 0.2),
    (0.2, -0.2, 0.1),
], duration=6.0)

# Gestures
nao.reach.point_at(1.0, 0.0, 0.3)
nao.reach.wave('RArm', cycles=3)
```

### Joint Info

```python
nao.joint_limits('Head')                            # min/max angles, max speed (degrees)
nao.joint_angles('RArm')                            # current angles (degrees)
```

### Autonomous Behavior

```python
nao.be_still()                                      # disable all autonomous movement
nao.expressive_listening(False)                      # disable idle breathing/swaying
nao.audio_expression(False)                          # disable sound reactions
nao.visual_expression(False)                         # disable eye LED animations
```

### Lifecycle

```python
nao.hot_reload()                                    # reload all modules without restart
nao.shutdown()                                      # stop all subscriptions, sit, clean up
```

### Raw SDK Access

For anything not wrapped by FluentNao, access NAOqi proxies directly via `nao.env`:

```python
# Use existing proxies
nao.env.motion.getJointNames('Body')
nao.env.memory.getData('Device/SubDeviceList/Battery/Charge/Sensor/Value')

# Add new proxies on the fly
nao.env.add_proxy('ALBehaviorManager')
nao.env.proxies['ALBehaviorManager'].getInstalledBehaviors()
```

## SSH Setup

Audio recording and file transfer require SSH access from the Docker container to NAO. NAO runs OpenSSH 5.9 which needs a PEM-format key and legacy algorithm support.

### Quick Setup

```bash
make ssh-setup
```

This generates a PEM key (`~/.ssh/id_nao`), copies it to NAO, and fixes permissions.

### Manual Setup

1. Generate key: `ssh-keygen -t rsa -m pem -f ~/.ssh/id_nao -N "" -C "fluentnao-docker"`
2. Copy to NAO: `ssh-copy-id -i ~/.ssh/id_nao nao@$NAO_IP`
3. Fix permissions: `ssh nao "chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"`

### Host SSH Config

Add to `~/.ssh/config`:

```
Host nao
    HostName <NAO IP>
    User nao
    IdentityFile ~/.ssh/id_nao
    PubkeyAcceptedAlgorithms +ssh-rsa
    HostkeyAlgorithms +ssh-rsa
```

The `PubkeyAcceptedAlgorithms` and `HostkeyAlgorithms` flags re-enable the legacy `ssh-rsa` algorithm that modern SSH clients disable by default.

## Architecture

```
Host Machine                    Docker Container              NAO Robot
                                (Ubuntu 14.04, Python 2.7)    (OpenSSH 5.9)

curl POST /exec  ------>  server.py (port 5050)
  "nao.say('hi')"         eval/exec with nao object
                                  |
                           nao.env ----NAOqi protocol----> ALTextToSpeech
                           nao.camera --NAOqi protocol---> ALVideoDevice
                           nao.audio ---SCP over SSH-----> /home/nao/ (temp)
                                  |                              |
                           /photos, /video, /audio <--- volume mounts
```

## Project Structure

```
FluentNao/
  server.py                      # HTTP bridge (/exec, /reload, /audio, /health)
  bootstrap_server.py            # Server startup with atexit shutdown
  Dockerfile                     # Ubuntu 14.04 + Python 2.7 + openssh + libav-tools
  docker-compose.yml             # Port mapping, volumes, SSH mount
  Makefile                       # Build, serve, ssh-setup targets
  src/main/python/
    fluentnao/
      nao.py                     # Main Nao class (speech, postures, walking, video, shutdown)
      core/
        arms.py                  # Arm movements (up, down, forward, out, back)
        elbows.py                # Elbow flex and rotation
        wrists.py                # Wrist rotation
        hands.py                 # Hand open/close
        head.py                  # Head yaw and pitch
        legs.py                  # Leg movements with balance
        feet.py                  # Ankle control and plane constraints
        leds.py                  # LED color control
        camera.py                # Photo, video, face tracking
        audio.py                 # Playback, recording, speech recognition, sound localization
        vision.py                # Ball tracking, object recognition, movement/darkness detection
        people.py                # People perception, engagement zones, gaze, sitting detection
        sensors.py               # Touch, battery, motor temperature
        navigation.py            # Walking, localization, visual compass
        tracker.py               # Unified tracking (face, ball, landmark, people, sound)
        reach.py                 # Cartesian 3D control, trajectories, gestures
        ssh.py                   # Shared SSH/SCP utility for NAO file transfer
        joints.py                # Joint/chain name constants, event enums
        animations.py            # Animation path dictionaries (POD, STAND, SIT)
        naoscript.py             # Script execution (deprecated)
        recorder/                # Keyframe recording and translation
    naoutil/                     # NAO environment, broker, memory event helpers
    pynaoqi-.../                 # NAOqi Python 2.7 SDK bindings
    nao-conscious/               # Event-driven personality system (providers/subscribers)
```
