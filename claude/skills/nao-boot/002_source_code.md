# Source Code

**Trigger Condition**: Always

Use the `Read` tool on ALL of these files. Every file has comprehensive docstrings explaining the full API.

# FluentNao Core (read all of these -- they ARE the API)

~/code/oss/FluentNao/src/main/python/fluentnao
  |- nao.py                     # Main Nao class -- speech, postures, walking, balance, video recording, shutdown
  +- core
      |- arms.py                # Arm movements (up, down, forward, out, back) with left/right variants
      |- elbows.py              # Elbow control (bent, straight, turn_up, turn_down, turn_in)
      |- wrists.py              # Wrist rotation (center, turn_out, turn_in)
      |- hands.py               # Hand open/close
      |- head.py                # Head yaw (left, right, forward) and pitch (up, down, center)
      |- legs.py                # Leg movements with balance support
      |- feet.py                # Ankle control and plane constraints
      |- leds.py                # LED color control (eyes, head, ears, chest, feet)
      |- camera.py              # Photo capture, video frame recording, face tracking
      |- audio.py               # Playback, mic recording, volume, speech recognition, sound localization
      |- vision.py              # Red ball tracking, object recognition, movement/darkness detection
      |- people.py              # People perception, engagement zones, gaze analysis, sitting detection
      |- sensors.py             # Touch events (head, bumpers, hands, chest), battery, motor temperature
      |- navigation.py          # Walking (move_to), localization (learn_home/go_home), visual compass
      |- tracker.py             # Unified tracker (face, ball, landmark, people, sound) with head/body/walk modes
      |- reach.py               # Cartesian 3D position control, trajectories, gestures (point_at, wave)
      |- events.py              # All event name constants grouped by category (touch, vision, people, audio, sensors, nav)
      |- abilities.py           # High-level composites: ask, snap, scan, watch, wait_for, survey, alert, patrol, hear, explore
      |- ssh.py                 # Shared SSH utility for file transfer to/from NAO
      |- joints.py              # Joint names, chain names, event enums
      |- animations.py          # Animation preset dictionaries (POD, STAND, SIT)
      |- naoscript.py           # Script execution (deprecated -- use bridge instead)
      +- recorder
          |- recorder.py        # Keyframe capture
          +- translator.py      # Joint angles to FluentNao commands

# HTTP Bridge and Infrastructure

~/code/oss/FluentNao
  |- server.py                  # HTTP bridge (/exec, /reload, /audio, /events, /health endpoints)
  |- bootstrap_server.py        # Server-mode initialization with atexit shutdown
  |- Makefile                   # Docker commands (make serve, make ssh-setup, make init)
  |- docker-compose.yml         # Volumes: data/{photos,video,audio,object_detection}, ~/.ssh
  +- README.md                  # Full usage docs, API reference, and SSH setup guide

# NAO Utilities

~/code/oss/FluentNao/src/main/python/naoutil
  |- naoenv.py                  # Environment/proxy management, ALModule short names (PROXY_SHORT_NAMES dict)
  |- broker.py                  # ALBroker connection setup
  +- memory.py                  # Event subscription helpers (subscribeToEvent, unsubscribeToEvent)

# SDK Reference

~/code/oss/FluentNao/src/main/python/pynaoqi-python2.7-2.1.4.13-linux64
  |- naoqi.py                   # ALProxy, ALBroker, ALModule bindings
  |- motion.py                  # Motion constants (FRAME_TORSO=0, FRAME_WORLD=1, AXIS_MASK_ALL=63, TO_RAD, TO_DEG)
  +- vision_definitions.py      # Camera resolution and color space constants

Confirm you have read every file and acknowledge it.