# FluentNao

Control Nao using fluent stanza of python code.

# Requirements

All you need is docker and a nao robot connected to the same network as your computer.

# Setup

Push the button on Nao's chest to get it's IP address and set it in your terminal

```
export NAO_IP=###.###.###.###
```

## SSH Setup (required for audio recording and file transfer)

NAO runs OpenSSH 5.9, which requires special handling for modern SSH clients. The quickest path is `make ssh-setup`, which handles steps 1-3 below automatically. If you prefer to do it manually, or if something goes wrong, follow these steps:

### Step 1: Generate a dedicated NAO key

```bash
ssh-keygen -t rsa -m pem -f ~/.ssh/id_nao -N "" -C "fluentnao-docker"
```

Why these flags:
- `-m pem` — NAO's old OpenSSL (inside the Docker container) cannot read the newer OpenSSH private key format (`-----BEGIN OPENSSH PRIVATE KEY-----`). The PEM format (`-----BEGIN RSA PRIVATE KEY-----`) is required.
- `-N ""` — no passphrase, because the Docker container uses this key non-interactively via SCP.

### Step 2: Copy the public key to NAO

```bash
ssh-copy-id -i ~/.ssh/id_nao nao@$NAO_IP
```

You will be prompted for NAO's SSH password. This adds your public key to `/home/nao/.ssh/authorized_keys` on the robot.

### Step 3: Fix permissions on NAO

```bash
ssh -o PubkeyAcceptedAlgorithms=+ssh-rsa -o HostkeyAlgorithms=+ssh-rsa -i ~/.ssh/id_nao nao@$NAO_IP "chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
```

NAO's OpenSSH 5.9 is strict about file permissions. If `~/.ssh` is not 700 or `authorized_keys` is not 600, key auth will silently fail.

### Step 4: Add NAO to your SSH config

Add this block to `~/.ssh/config`:

```
Host nao
    HostName <your NAO's IP>
    User nao
    IdentityFile ~/.ssh/id_nao
    PubkeyAcceptedAlgorithms +ssh-rsa
    HostkeyAlgorithms +ssh-rsa
```

Why the algorithm flags: modern SSH clients (OpenSSH 8.8+) disable the `ssh-rsa` signature algorithm by default, but NAO's OpenSSH 5.9 only supports `ssh-rsa`. These flags re-enable it. They are only needed on the host — the Docker container runs OpenSSH 6.6 which still defaults to `ssh-rsa`.

### Step 5: Test

```bash
ssh nao echo hello
```

Should print `hello` with no password prompt.

### Automated setup

Steps 1-3 are handled by:

```bash
make ssh-setup
```

It will generate the key (if it doesn't exist), copy it to NAO, fix permissions, and print the SSH config block to add to `~/.ssh/config`.

### How the Docker container uses SSH

- `~/.ssh` is mounted read-only at `/root/.ssh` inside the container
- SSH commands use `-i /root/.ssh/id_nao` to authenticate with NAO
- `LD_LIBRARY_PATH` is overridden before SSH calls to prevent NAO's bundled `libcrypto.so` (in the pynaoqi SDK) from conflicting with the system SSH libraries
- Audio recordings and playback files are SCP'd between NAO and the container's `/audio` volume, then immediately deleted from NAO to avoid filling its limited storage

# Get Started

`make`   - see all make targets

| Target | Description |
|--------|-------------|
| `init` | Build the docker image |
| `ssh-setup` | Copy SSH key to NAO for passwordless auth |
| `up` | Run interactive python shell |
| `serve` | Run HTTP bridge server on port 5050 |
| `bash` | Run bash prompt in container |

## HTTP Bridge

Start the bridge server:

```
make serve
```

Send commands via curl:

```bash
# health check
curl -s http://localhost:5050/health

# single command
curl -s -X POST http://localhost:5050/exec -d "nao.say('hello')"

# multi-line script (set result= to get return values)
curl -s -X POST http://localhost:5050/exec -d "
x = nao.audio.get_volume()
result = x
"

# upload and play audio file
curl -X POST -H "X-Filename: sound.wav" --data-binary @sound.wav http://localhost:5050/audio

# replay a file already in the audio volume
curl -X POST http://localhost:5050/audio/play/sound.wav

# list audio files
curl -s http://localhost:5050/audio
```

## Docker Volumes

The container mounts these directories for media capture:

| Host Path | Container Path | Purpose |
|-----------|---------------|---------|
| `./photos` | `/photos` | Photo captures |
| `./video` | `/video` | Video frame captures |
| `./audio` | `/audio` | Audio recordings |
| `~/.ssh` | `/root/.ssh` (read-only) | SSH keys for NAO file transfer |

# Example Code

Example code using Fluent Nao

    # zero out joints
    nao.zero().go()

    # arms up
    nao.say("raising my hands")
    nao.arms.up()
    nao.go()

    # hands open
    nao.say("opening my hands")
    nao.hands.open()
    nao.go()

## Camera

```python
# take a photo (saved to /photos/)
nao.camera.photo('snapshot')

# high-res photo
nao.camera.photo('hires', resolution=2)  # VGA 640x480

# switch to bottom camera
nao.camera.bottom().photo('floor')

# record video frames (saved to /video/)
nao.camera.start_recording('clip', fps=10)
nao.camera.stop_recording()

# face tracking - head follows a face
nao.camera.track_face()
nao.camera.stop_tracking()

# whole body tracks a face
nao.camera.track_face_whole_body()
```

## Audio

```python
# playback
nao.audio.play('http://example.com/sound.mp3')
nao.audio.play_file('recording.wav')  # from /audio/ volume
nao.audio.stop_all()

# volume
nao.audio.set_volume(50)
nao.audio.get_volume()
nao.audio.mute()
nao.audio.unmute()

# record from NAO's microphones (pulled to /audio/, cleaned from NAO)
nao.audio.start_recording('meeting')
nao.audio.stop_recording()  # returns local path

# speech recognition
def on_word(words):
    print(words)  # {'hello': 0.85, 'goodbye': 0.12}

nao.audio.listen_for(['hello', 'goodbye', 'stop'], on_word)
nao.audio.stop_listening()

# sound direction
nao.audio.sound_direction()
nao.audio.start_sound_tracking(callback)
nao.audio.stop_sound_tracking()
```

## Duration of Movement

You can specify a number of seconds to take for each command or stanza. We use the setDuration() to set the duration globally for every function that follows

    # sets duration to half a second
    nao.set_duration(.5)

We can override the default duration in each motion function

    # open hands in half a second
    nao.hands.open()

    # put arms out in 4 seconds
    nao.arms.out(4)
    nao.go()

NOTE: passing in a duration of 0 will be ignored

## Offsets

You can offset any motion, adding more or less degrees of movement.  For example

    # zero out joints
    nao.zero().go()

    # put arms up minus 30 degrees
    nao.arms.up(0, -30)

NOTE: the zero is duration telling the api to ignore that argument;
