"""High-level reusable abilities that combine multiple FluentNao capabilities.

Accessed via nao.abilities. Each method combines events, sensors, camera,
speech, movement, and/or LEDs into a single reusable primitive.
"""
import time
import threading


class Abilities():
    """Composite behaviors built from FluentNao primitives.

    Each ability subscribes to events, performs actions, and emits
    results to the /events long poll endpoint for Claude Code to consume.

    Methods:
        scan()      -- sweep head and capture photos at each position
        watch()     -- monitor events and auto-capture photos when triggered
        wait_for()  -- block until a specific event fires
        survey()    -- ask multiple questions and collect answers
        alert()     -- flash LEDs, speak urgently, emit event
        patrol()    -- navigate waypoints and run action at each stop
    """

    def __init__(self, nao):
        self.nao = nao
        self.log = nao.log

    def observe(self, photo_interval=10, audio_interval=30, audio_duration=5):
        """Start continuous background observation with photos and audio.

        Runs two background threads that capture photos and audio at
        regular intervals while NAO does other things. Emits events
        for each capture so Claude Code can process them.

        Args:
            photo_interval: seconds between photo captures (default 10)
            audio_interval: seconds between audio recordings (default 30)
            audio_duration: length of each audio recording (default 5)

        Emits 'observe_photo' with {path, index, timestamp} for each photo.
        Emits 'observe_audio' with {path, index, timestamp} for each recording.

        Call stop_observing() to stop.

        Examples:
            nao.abilities.observe()                   # default intervals
            nao.abilities.observe(5, 20, 3)           # photos every 5s, audio every 20s for 3s
            nao.abilities.observe(photo_interval=3)   # fast photos, default audio
        """
        self._observing = True
        self._observe_photo_count = 0
        self._observe_audio_count = 0

        def photo_loop():
            while self._observing:
                try:
                    name = 'observe_photo_{}'.format(self._observe_photo_count)
                    path = self.nao.camera.photo(name)
                    if path:
                        self.nao.emit('observe_photo', {
                            'path': path,
                            'index': self._observe_photo_count,
                            'timestamp': time.time(),
                        })
                        self._observe_photo_count += 1
                except Exception:
                    pass
                time.sleep(photo_interval)

        def audio_loop():
            while self._observing:
                try:
                    name = 'observe_audio_{}'.format(self._observe_audio_count)
                    self.nao.audio.start_recording(name, channels=[0, 0, 1, 0])
                    time.sleep(audio_duration)
                    path = self.nao.audio.stop_recording()
                    if path:
                        self.nao.emit('observe_audio', {
                            'path': path,
                            'index': self._observe_audio_count,
                            'timestamp': time.time(),
                        })
                        self._observe_audio_count += 1
                except Exception:
                    pass
                time.sleep(audio_interval - audio_duration)

        pt = threading.Thread(target=photo_loop)
        pt.daemon = True
        pt.start()

        at = threading.Thread(target=audio_loop)
        at.daemon = True
        at.start()

        self._observe_threads = [pt, at]
        self.log('observe: started (photos every {}s, audio every {}s for {}s)'.format(
            photo_interval, audio_interval, audio_duration))
        return self.nao

    def stop_observing(self):
        """Stop continuous background observation."""
        self._observing = False
        self.log('observe: stopped after {} photos, {} audio clips'.format(
            getattr(self, '_observe_photo_count', 0),
            getattr(self, '_observe_audio_count', 0),
        ))
        return self.nao

    def ask(self, message, answers, confidence=0.15):
        """Ask a question and wait for one of the expected answers.

        NAO speaks the message, listens for one of the answers, then
        stops listening and emits an 'answer' event.

        Args:
            message: text for NAO to speak
            answers: list of words/phrases to listen for
            confidence: minimum confidence threshold (0.0-1.0)

        Emits 'answer' event with {question, answer}.

        Examples:
            nao.ask('is it raining', ['yes', 'no'])
            nao.ask('what color', ['red', 'blue', 'green'])
        """
        self.nao.be_still()
        self.nao.say_and_block(message)
        answered = [False]

        def on_word(words):
            if answered[0]:
                return
            best = max(words, key=words.get)
            if words[best] >= confidence:
                answered[0] = True
                threading.Timer(0.5, self.nao.audio.stop_listening).start()
                self.nao.emit('answer', {'question': message, 'answer': best})

        self.nao.audio.listen_for(answers, on_word)
        return self.nao

    def snap(self, message='touch my head to take a photo', filename=None):
        """Face-tracking photo capture triggered by head touch.

        NAO speaks, tracks your face, waits for head tap, takes VGA photo,
        and emits a 'photo' event with the file path.

        Args:
            message: what NAO says before waiting
            filename: photo name (without extension). Defaults to 'snap_<timestamp>'

        Emits 'photo' event with the file path.

        Examples:
            nao.snap()
            nao.snap('smile for the camera', 'portrait')
        """
        if not filename:
            filename = 'snap_{}'.format(int(time.time()))

        self.nao.camera.track_face()
        self.nao.say_and_block(message)

        snapped = [False]

        def on_touch(event):
            if snapped[0]:
                return
            snapped[0] = True
            self.nao.camera.stop_tracking()
            path = self.nao.camera.photo(filename, resolution=2)
            self.nao.say('got it')
            self.nao.emit('photo', path)
            self.nao.sensors.stop_all_touch()

        self.nao.sensors.on_head(on_touch)
        return self.nao

    def scan(self, positions=None, name='scan'):
        """Sweep head across positions and capture a photo at each.

        Args:
            positions: list of (yaw, pitch) tuples in degrees.
                Defaults to 5 positions sweeping left to right.
            name: prefix for photo filenames.

        Emits 'scan_photo' event for each photo with the file path.
        Emits 'scan_complete' when done with the count.

        Returns:
            self
        """
        if positions is None:
            positions = [
                (-60, 0), (-30, 0), (0, 0), (30, 0), (60, 0),
            ]

        self.nao.head.stiff()
        photos = []

        for i, (yaw, pitch) in enumerate(positions):
            self.nao.move_with_degrees_and_duration('HeadYaw', yaw, 1.5)
            self.nao.move_with_degrees_and_duration('HeadPitch', pitch, 1.5)
            self.nao.go()
            time.sleep(0.5)
            path = self.nao.camera.photo('{}_{}'.format(name, i), resolution=2)
            if path:
                photos.append(path)
                self.nao.emit('scan_photo', {'index': i, 'path': path})

        self.nao.head.forward()
        self.nao.head.center()
        self.nao.head.go()
        self.nao.emit('scan_complete', {'count': len(photos), 'photos': photos})
        self.log('scan: captured {} photos'.format(len(photos)))
        return self

    def hear(self, duration=5, name=None):
        """Record audio from NAO's microphones and emit the file path.

        Turns head toward the loudest sound source first, then records
        for the specified duration using the front microphone.

        Args:
            duration: recording length in seconds (default 5)
            name: filename without extension. Defaults to 'hear_<timestamp>'

        Emits 'heard' event with the local file path.

        Examples:
            nao.abilities.hear()           # 5 seconds
            nao.abilities.hear(10)         # 10 seconds
            nao.abilities.hear(3, 'clip')  # 3 seconds, named 'clip'
        """
        if not name:
            name = 'hear_{}'.format(int(time.time()))

        # try to detect sound direction and look toward it
        direction = self.nao.audio.sound_direction(sensitivity=0.8, timeout=2)
        if direction:
            try:
                azimuth = direction[1][0]
                import math
                yaw_deg = math.degrees(azimuth)
                self.nao.head.stiff()
                self.nao.move_with_degrees_and_duration('HeadYaw', yaw_deg, 1.0)
                self.nao.go()
            except Exception:
                pass

        # record
        self.nao.audio.start_recording(name, channels=[0, 0, 1, 0])
        time.sleep(duration)
        path = self.nao.audio.stop_recording()

        self.nao.emit('heard', {'path': path, 'duration': duration})
        self.log('hear: recorded {}s to {}'.format(duration, path))
        return self.nao

    def explore(self, photo_count=7, sonar=True):
        """Scan surroundings and emit a full environment report.

        NAO sweeps its head across positions, captures a photo at each,
        reads sonar distances, and reports its current position. Emits
        everything Claude Code needs to plan a path.

        Args:
            photo_count: number of photos to take (evenly spaced across
                ~120 degree sweep). Default 7.
            sonar: if True, read sonar at each position. Default True.

        Emits 'explore_photo' for each photo with:
            {index, yaw, pitch, path, sonar_left, sonar_right}

        Emits 'explore_complete' with:
            {count, photos, position, orientation}

        Examples:
            nao.abilities.explore()          # 7 photos with sonar
            nao.abilities.explore(5, False)  # 5 photos, no sonar
        """
        # calculate evenly spaced yaw positions
        sweep = 120.0
        start = -sweep / 2
        step = sweep / (photo_count - 1) if photo_count > 1 else 0
        positions = [(start + i * step, 0) for i in range(photo_count)]

        self.nao.head.stiff()
        if sonar:
            self.nao.prep_sonar()

        photos = []
        for i, (yaw, pitch) in enumerate(positions):
            self.nao.move_with_degrees_and_duration('HeadYaw', yaw, 1.0)
            self.nao.move_with_degrees_and_duration('HeadPitch', pitch, 1.0)
            self.nao.go()
            time.sleep(0.3)

            path = self.nao.camera.photo('explore_{}'.format(i), resolution=2)

            data = {
                'index': i,
                'yaw': yaw,
                'pitch': pitch,
                'path': path,
            }

            if sonar:
                sonar_vals = self.nao.read_sonar()
                data['sonar_left'] = sonar_vals[0]
                data['sonar_right'] = sonar_vals[1]

            photos.append(data)
            self.nao.emit('explore_photo', data)

        # return head to center
        self.nao.head.forward()
        self.nao.head.center()
        self.nao.head.go()

        # get robot position if localization is available
        position = self.nao.navigation.position()
        orientation = self.nao.navigation.orientation()

        self.nao.emit('explore_complete', {
            'count': len(photos),
            'photos': photos,
            'position': position,
            'orientation': orientation,
        })
        self.log('explore: captured {} photos'.format(len(photos)))
        return self.nao

    def watch(self, event_names=None, duration=30):
        """Monitor events and auto-capture a photo when any fires.

        Subscribes to the given events. When one fires, takes a VGA photo
        and emits a 'watch_triggered' event with both the trigger event
        name and the photo path.

        Args:
            event_names: events to watch. Defaults to vision + people events.
            duration: how long to watch in seconds. 0 = until unsubscribe_all().

        Emits 'watch_triggered' with {event, value, photo} on each trigger.
        Emits 'watch_ended' when duration expires.

        Returns:
            self
        """
        if event_names is None:
            event_names = list(self.nao.events.vision) + list(self.nao.events.people)

        last_trigger = [0]

        def on_event(event, value):
            now = time.time()
            if now - last_trigger[0] < 3:
                return
            last_trigger[0] = now
            path = self.nao.camera.photo('watch_{}'.format(int(now)), resolution=2)
            self.nao.emit('watch_triggered', {
                'event': event,
                'value': str(value),
                'photo': path,
            })

        self.nao.subscribe(event_names, on_event)

        if duration > 0:
            def stop_after():
                time.sleep(duration)
                self.nao.unsubscribe_all()
                self.nao.emit('watch_ended', {'duration': duration})

            t = threading.Thread(target=stop_after)
            t.daemon = True
            t.start()

        self.log('watch: monitoring {} events for {}s'.format(len(event_names), duration))
        return self

    def wait_for(self, event_names, timeout=30):
        """Block until one of the specified events fires.

        Args:
            event_names: list of event strings or a category set.
            timeout: max seconds to wait.

        Returns:
            dict with {event, value} on success, None on timeout.

        Examples:
            result = nao.abilities.wait_for(nao.events.touch)
            if result:
                print(result['event'])  # 'FrontTactilTouched'
        """
        result = [None]
        done = threading.Event()

        def on_event(event, value):
            result[0] = {'event': event, 'value': value}
            done.set()

        self.nao.subscribe(event_names, on_event)
        done.wait(timeout)
        self.nao.unsubscribe_all()
        return result[0]

    def survey(self, questions, confidence=0.15):
        """Ask multiple questions in sequence and collect answers.

        Args:
            questions: list of (message, [answers]) tuples.
            confidence: speech recognition confidence threshold.

        Emits 'survey_answer' for each answer as it comes in.
        Emits 'survey_complete' with all Q&A pairs when done.

        Returns:
            self

        Examples:
            nao.abilities.survey([
                ('what is your name', ['don', 'john', 'jane']),
                ('how are you', ['good', 'bad', 'okay']),
                ('do you like robots', ['yes', 'no']),
            ])
        """
        results = []

        for message, answers in questions:
            collected = threading.Event()
            answer = [None]

            def make_handler(msg, ans_list, evt, ans_ref):
                def on_word(words):
                    best = max(words, key=words.get)
                    if words[best] >= confidence:
                        ans_ref[0] = best
                        evt.set()
                        import threading as _t
                        _t.Timer(0.5, self.nao.audio.stop_listening).start()
                return on_word

            self.nao.be_still()
            self.nao.say_and_block(message)
            handler = make_handler(message, answers, collected, answer)
            self.nao.audio.listen_for(answers, handler)
            collected.wait(15)

            if answer[0]:
                pair = {'question': message, 'answer': answer[0]}
                results.append(pair)
                self.nao.emit('survey_answer', pair)
            else:
                results.append({'question': message, 'answer': None})

        self.nao.emit('survey_complete', results)
        self.log('survey: collected {} answers'.format(len(results)))
        return self

    def alert(self, message='alert', color=0xFF0000):
        """Flash LEDs, speak urgently, and emit an alert event.

        Args:
            message: what NAO says.
            color: LED color as hex (default red).

        Emits 'alert' event with the message.

        Returns:
            self
        """
        self.nao.leds.eyes(color)
        self.nao.leds.chest(color)
        self.nao.leds.ears(color)
        self.nao.say_and_block(message)
        time.sleep(0.3)
        self.nao.leds.off()
        time.sleep(0.2)
        self.nao.leds.eyes(color)
        self.nao.leds.chest(color)
        time.sleep(0.3)
        self.nao.leds.off()
        self.nao.emit('alert', message)
        self.log('alert: {}'.format(message))
        return self

    def patrol(self, waypoints, action=None):
        """Navigate through waypoints, run action at each, emit progress.

        Args:
            waypoints: list of (x, y, theta) tuples in meters/radians.
            action: optional callback(waypoint_index, waypoint) at each stop.
                If None, takes a photo at each waypoint.

        Emits 'patrol_waypoint' at each stop with index and position.
        Emits 'patrol_complete' when all waypoints visited.

        Returns:
            self

        Examples:
            # Simple patrol with auto-photos
            nao.abilities.patrol([(1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0)])

            # Custom action at each stop
            def check(i, wp):
                nao.say('waypoint {}'.format(i))
            nao.abilities.patrol([(1, 0, 0), (0, 0, 1.57)], action=check)
        """
        self.nao.stiff()
        self.nao.stand_init()

        for i, wp in enumerate(waypoints):
            x, y, theta = wp[0], wp[1], wp[2] if len(wp) > 2 else 0
            self.nao.navigation.move_to(x, y, theta)

            data = {'index': i, 'waypoint': wp}

            if action:
                action(i, wp)
            else:
                path = self.nao.camera.photo('patrol_{}'.format(i), resolution=2)
                data['photo'] = path

            self.nao.emit('patrol_waypoint', data)
            self.log('patrol: waypoint {} of {}'.format(i + 1, len(waypoints)))

        self.nao.emit('patrol_complete', {'count': len(waypoints)})
        self.log('patrol: complete')
        return self

    def push_to_sense(self):
        """Enable front head button for snap photo and rear head button for hold-to-record.

        Front tap: countdown tones (C-E-G), red eye flash, VGA photo capture,
            emits 'photo_captured' event.
        Rear hold: hold to record audio, release to stop,
            emits 'audio_captured' event.

        Call stop_push_to_sense() to disable both.

        Examples:
            nao.abilities.push_to_sense()
            nao.abilities.stop_push_to_sense()
        """
        import time as _time

        def on_front_tap(event):
            self.log('[push_to_sense] front tap detected, starting snap_photo')
            t0 = _time.time()
            self.nao.camera.snap_photo('tap_' + str(int(t0)), resolution=2)
            self.log('[push_to_sense] snap_photo complete ({:.3f}s total)'.format(_time.time() - t0))

        self.nao.sensors.on_head_front(on_front_tap)
        self.nao.audio.hold_to_record('RearTactilTouched')
        self.log('push_to_sense: front=snap_photo, rear=hold_to_record')
        return self.nao

    def stop_push_to_sense(self):
        """Disable push_to_sense bindings."""
        self.nao.sensors.stop_on_touch('FrontTactilTouched')
        self.nao.audio.stop_hold_to_record()
        self.log('stop_push_to_sense: disabled')
        return self.nao
