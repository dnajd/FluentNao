"""
Audio module for NAO robot playback, microphone recording, volume control,
speech recognition, and sound source localization.

This module provides the Audio class, accessed via nao.audio, which wraps
several NAOqi proxies: ALAudioRecorder, ALAudioDevice, ALAudioSourceLocalization,
and ALSpeechRecognition.

Recording Workflow:
    start_recording() records audio on the NAO robot itself (to /home/nao/).
    stop_recording() stops recording, then SCPs the file from NAO to the local
    /audio Docker volume, and deletes the temporary file from NAO.

Storage Directory:
    /audio -- default local directory for audio files (Docker-mounted volume)

Channel Configuration Constants:
    Audio.MONO_LEFT    = [1, 0, 0, 0]
    Audio.MONO_RIGHT   = [0, 1, 0, 0]
    Audio.MONO_FRONT   = [0, 0, 1, 0]
    Audio.MONO_REAR    = [0, 0, 0, 1]
    Audio.ALL_CHANNELS = [1, 1, 1, 1]  (default for recording)

Key Methods:
    play(url, volume=1, pan=0)
        Stream audio from a URL via ALAudioPlayer.post.playWebStream.
        Non-blocking (uses post). Returns self.

    play_file(filename)
        Play a local file from audio_dir. SCPs to NAO, plays via ALAudioPlayer,
        then cleans up the remote copy. Blocking call. Returns self.

    stop_all()
        Stop all audio playback immediately.

    set_volume(volume)
        Set master output volume (0-100 integer). Returns self.

    get_volume()
        Returns current output volume as integer, or None if unavailable.

    mute() / unmute()
        Mute or unmute audio output. Returns self.

    start_recording(filename='recording', channels=None, sample_rate=16000,
                    audio_format='wav')
        Begin recording from NAO microphones. Records to /home/nao/ on the robot.
        Default format is WAV at 16kHz with all 4 channels. Returns self.

    stop_recording()
        Stop recording, SCP file from NAO to local audio_dir, delete from NAO.
        Returns the local file path on success, or None on failure.

    listen_for(words, callback, language='English', word_spotting=False)
        Subscribe to speech recognition for a list of words.
        Callback receives a dict of {word: confidence} when words are detected.
        Set word_spotting=True to detect words within continuous speech.
        Returns self.

    stop_listening()
        Stop speech recognition subscription. Returns self.

    sound_direction(sensitivity=0.5, timeout=3)
        Blocking call to detect sound direction. Polls for up to timeout seconds.
        Returns ALAudioSourceLocalization data or None.

    start_sound_tracking(callback, sensitivity=0.5)
        Subscribe to continuous sound localization events.
        Callback receives raw localization data on each event.

    stop_sound_tracking()
        Unsubscribe from sound localization events.

    clear()
        Delete all files in the audio directory.

Usage Examples:
    # Play a stream
    nao.audio.play('http://example.com/song.mp3')

    # Record audio
    nao.audio.start_recording('greeting', sample_rate=16000)
    # ... wait ...
    path = nao.audio.stop_recording()
    # path is now '/audio/greeting.wav'

    # Volume control
    nao.audio.set_volume(50)
    nao.audio.mute()
    nao.audio.unmute()

    # Speech recognition
    def on_word(words):
        print(words)  # e.g. {'hello': 0.85, 'goodbye': 0.12}

    nao.audio.listen_for(['hello', 'goodbye'], on_word)
    # ... later ...
    nao.audio.stop_listening()

    # Sound direction (blocking)
    direction = nao.audio.sound_direction(sensitivity=0.7, timeout=5)

Important Notes:
    - Recording happens on the NAO robot; files are transferred via SCP.
    - Requires SSH access to NAO (uses fluentnao.core.ssh utilities).
    - Unavailable proxies are handled gracefully (methods log and return self/None).
    - All chainable methods return self for fluent API usage.
    - This is Python 2.7 code.
"""

import glob
import os
import time
import threading

import naoutil.memory as memory
from fluentnao.core.ssh import ssh, scp_to_nao, scp_from_nao, nao_ip


class Audio():

    # channel configs for ALAudioRecorder
    MONO_LEFT = [1, 0, 0, 0]
    MONO_RIGHT = [0, 1, 0, 0]
    MONO_FRONT = [0, 0, 1, 0]
    MONO_REAR = [0, 0, 0, 1]
    ALL_CHANNELS = [1, 1, 1, 1]

    # temp path on NAO for recordings
    NAO_RECORD_DIR = '/home/nao'

    def __init__(self, nao, audio_dir='/audio'):
        self.nao = nao
        self.joints = nao.joints
        self.chains = nao.chains
        self.log = nao.log
        self.audio_dir = audio_dir

        # proxies - gracefully handle unavailable services
        self.recorder = self._try_proxy("ALAudioRecorder")
        self.device = self._try_proxy("ALAudioDevice")
        self.localisation = self._try_proxy("ALAudioSourceLocalization")
        self.speech_recog = self._try_proxy("ALSpeechRecognition")

        # state
        self._recording = False
        self._recording_filename = None
        self._listening = False
        self._word_callback = None
        self._sound_tracking = False
        self._sound_callback = None

    def _try_proxy(self, name):
        try:
            self.nao.env.add_proxy(name)
            return self.nao.env.proxies[name]
        except Exception as e:
            self.log('audio: {} not available: {}'.format(name, e))
            return None

    ###################################
    # cleanup
    ###################################

    def clear(self):
        files = glob.glob('{}/*'.format(self.audio_dir))
        for f in files:
            os.remove(f)
        self.log('audio.clear: removed {} files'.format(len(files)))
        return self

    ###################################
    # playback (original API)
    ###################################

    def play(self, url, volume=1, pan=0):
        self.nao.env.audioPlayer.post.playWebStream(url, volume, pan)
        return self

    def stop_all(self):
        self.nao.env.audioPlayer.stopAll()
        return self

    NAO_PLAYBACK_DIR = '/home/nao/audio_playback'

    def play_file(self, filename):
        local_path = '{}/{}'.format(self.audio_dir, filename)

        if not os.path.exists(local_path):
            self.log('audio.play_file: not found {}'.format(local_path))
            return self

        # ensure remote dir exists
        ssh('mkdir -p {}'.format(self.NAO_PLAYBACK_DIR))

        remote_path = '{}/{}'.format(self.NAO_PLAYBACK_DIR, filename)

        # push to NAO, play, always clean up
        scp_to_nao(local_path, remote_path)
        try:
            self.nao.env.audioPlayer.playFile(remote_path)
        finally:
            ssh('rm -f {}'.format(remote_path))

        self.log('audio.play_file: played and cleaned up {}'.format(filename))
        return self

    ###################################
    # volume & device control
    ###################################

    def set_volume(self, volume):
        if not self.device:
            self.log('audio.set_volume: device not available')
            return self
        self.device.setOutputVolume(volume)
        return self

    def get_volume(self):
        if not self.device:
            return None
        return self.device.getOutputVolume()

    def mute(self):
        if not self.device:
            return self
        self.device.muteAudioOut(True)
        return self

    def unmute(self):
        if not self.device:
            return self
        self.device.muteAudioOut(False)
        return self

    ###################################
    # recording
    ###################################

    def start_recording(self, filename='recording', channels=None, sample_rate=16000, audio_format='wav'):
        if self._recording:
            self.log('audio.start_recording: already recording')
            return self
        if not self.recorder:
            self.log('audio.start_recording: recorder not available')
            return self

        if channels is None:
            channels = self.ALL_CHANNELS

        nao_path = '{}/{}.{}'.format(self.NAO_RECORD_DIR, filename, audio_format)
        self._recording_filename = filename
        self._recording_format = audio_format
        self._recording_nao_path = nao_path

        self.recorder.startMicrophonesRecording(nao_path, audio_format, sample_rate, channels)
        self._recording = True
        self.log('audio.start_recording: started -> {}'.format(nao_path))
        return self

    def stop_recording(self):
        if not self._recording or not self.recorder:
            self.log('audio.stop_recording: not recording')
            return None

        self.recorder.stopMicrophonesRecording()
        self._recording = False
        self.log('audio.stop_recording: stopped')

        # pull from NAO and clean up
        local_path = self._pull_and_cleanup(
            self._recording_nao_path,
            '{}.{}'.format(self._recording_filename, self._recording_format)
        )
        return local_path

    def _pull_and_cleanup(self, nao_path, local_filename):
        local_path = '{}/{}'.format(self.audio_dir, local_filename)

        result = scp_from_nao(nao_path, local_path)

        if result == 0:
            self.log('audio.pull: copied {} to {}'.format(nao_path, local_path))
            ssh('rm -f {}'.format(nao_path))
            self.log('audio.pull: cleaned up {}'.format(nao_path))
        else:
            self.log('audio.pull: failed to copy {} (rc={})'.format(nao_path, result))
            local_path = None

        return local_path

    ###################################
    # sound localisation
    ###################################

    def sound_direction(self, sensitivity=0.5, timeout=3):
        if not self.localisation:
            self.log('audio.sound_direction: localisation not available')
            return None
        self.localisation.setParameter("Sensitivity", sensitivity)
        self.localisation.subscribe("fluentnao_sound_loc")
        try:
            for _ in range(timeout * 2):
                time.sleep(0.5)
                try:
                    value = self.nao.env.memory.getData("ALAudioSourceLocalization/SoundLocated")
                    if value:
                        return value
                except Exception:
                    pass
        finally:
            self.localisation.unsubscribe("fluentnao_sound_loc")
        return None

    def start_sound_tracking(self, callback, sensitivity=0.5):
        if self._sound_tracking:
            self.log('audio.start_sound_tracking: already tracking')
            return self
        if not self.localisation:
            self.log('audio.start_sound_tracking: localisation not available')
            return self

        self._sound_callback = callback
        self._sound_tracking = True
        self.localisation.setParameter("Sensitivity", sensitivity)
        self.localisation.subscribe("fluentnao_sound_track")
        memory.subscribeToMicroEvent(
            'ALAudioSourceLocalization/SoundLocated',
            self._sound_event_cb,
            ''
        )
        self.log('audio.start_sound_tracking: started')
        return self

    def stop_sound_tracking(self):
        if not self._sound_tracking:
            return self

        memory.unsubscribeToMicroEvent('ALAudioSourceLocalization/SoundLocated')
        self.localisation.unsubscribe("fluentnao_sound_track")
        self._sound_tracking = False
        self._sound_callback = None
        self.log('audio.stop_sound_tracking: stopped')
        return self

    def _sound_event_cb(self, dataName, value, message):
        if self._sound_callback and value:
            self._sound_callback(value)

    ###################################
    # speech recognition
    ###################################

    def listen_for(self, words, callback, language='English', word_spotting=False):
        if self._listening:
            self.stop_listening()
        if not self.speech_recog:
            self.log('audio.listen_for: speech recognition not available')
            return self

        self._word_callback = callback
        self.speech_recog.setLanguage(language)
        self.speech_recog.setVocabulary(words, word_spotting)
        memory.subscribeToEvent('WordRecognized', self._word_event_cb)
        self._listening = True
        self.log('audio.listen_for: listening for {}'.format(words))
        return self

    def stop_listening(self):
        if not self._listening:
            return self

        memory.unsubscribeToEvent('WordRecognized')
        self._listening = False
        self._word_callback = None
        self.log('audio.stop_listening: stopped')
        return self

    def _word_event_cb(self, dataName, value, message):
        if self._word_callback and value:
            # value is [word1, confidence1, word2, confidence2, ...]
            words = dict(zip(value[0::2], value[1::2]))
            self._word_callback(words)
