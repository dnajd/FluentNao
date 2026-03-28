"""
Vision module for NAO robot red ball tracking, object/picture recognition,
movement detection, and darkness detection.

This module provides the Vision class, accessed via nao.vision, which wraps
several NAOqi proxies: ALRedBallTracker, ALRedBallDetection, ALMovementDetection,
ALDarknessDetection, and ALVisionRecognition.

Event Callback Cooldown:
    All event callbacks (on_ball, on_object, on_movement, on_darkness) enforce
    a 3-second cooldown between firings to prevent callback spam from rapid
    repeated detections.

Key Methods -- Red Ball:
    track_ball()
        Start head-only red ball tracking via ALRedBallTracker.

    track_ball_whole_body()
        Track red ball using head and full body movement.

    stop_tracking_ball()
        Stop ball tracking and release head stiffness.

    ball_position()
        Returns current tracked ball position, or None.

    is_tracking_ball()
        Returns True if ball tracking is active.

    on_ball(callback)
        Subscribe to red ball detection events. Callback receives detection
        data from the 'redBallDetected' event (with 3s cooldown).

    stop_on_ball()
        Unsubscribe from ball detection events.

Key Methods -- Object/Picture Recognition:
    learn_object(name, countdown=True)
        Teach NAO to recognize an object by name. If countdown=True, NAO speaks
        a countdown ("show me the <name>", "3", "2", "1") before capturing a
        VGA photo with the camera module, then pushes it to NAO for learning.

    learn_from_file(filepath, name=None)
        Learn an object from a local image file. If name is not provided, the
        filename (without extension) is used as the object name.

    learn_all(folder='/object_detection')
        Learn all image files in the given folder. Each file becomes a named
        object (using filename as name). NAO announces how many objects it learned.

    forget_all_objects()
        Clear the entire ALVisionRecognition database.

    on_object(callback)
        Subscribe to object/picture detection events via 'PictureDetected'.
        Callback receives detection data (with 3s cooldown).

    stop_on_object()
        Unsubscribe from object detection events.

Key Methods -- Movement Detection:
    on_movement(callback)
        Subscribe to movement detection events. Callback receives data from
        'MovementDetection/MovementDetected' (with 3s cooldown).

    stop_on_movement()
        Unsubscribe from movement detection events.

Key Methods -- Darkness Detection:
    on_darkness(callback)
        Subscribe to darkness detection events. Callback receives data from
        'DarknessDetection/DarknessDetected' (with 3s cooldown).

    stop_on_darkness()
        Unsubscribe from darkness detection events.

    is_dark()
        Returns the current darkness state from ALMemory, or None if unavailable.

Usage Examples:
    # Track a red ball
    nao.vision.track_ball()
    pos = nao.vision.ball_position()
    nao.vision.stop_tracking_ball()

    # React to ball detection
    def ball_seen(data):
        print('Ball detected!')
    nao.vision.on_ball(ball_seen)

    # Teach an object interactively
    nao.vision.learn_object('coffee_mug')

    # Learn all objects from a folder
    nao.vision.learn_all('/object_detection')

    # React to recognized objects
    def obj_found(data):
        print('Object recognized:', data)
    nao.vision.on_object(obj_found)

    # Movement detection
    def moved(data):
        print('Movement detected')
    nao.vision.on_movement(moved)

    # Darkness check
    if nao.vision.is_dark():
        nao.say('It is dark in here')

Important Notes:
    - Object learning uses SCP to push images to /home/nao/vision_learn on NAO.
    - learn_object() captures a VGA photo via nao.camera, so camera must be available.
    - All event callbacks have a 3-second cooldown to prevent rapid-fire invocations.
    - Unavailable proxies are handled gracefully (methods log and return self/None).
    - All chainable methods return self for fluent API usage.
    - This is Python 2.7 code.
"""

import glob
import os
import time

import naoutil.memory as memory
from fluentnao.core.ssh import ssh, scp_to_nao

NAO_LEARN_DIR = '/home/nao/vision_learn'


class Vision():

    def __init__(self, nao):
        self.nao = nao
        self.log = nao.log

        # proxies - gracefully handle unavailable services
        self.ball_tracker = self._try_proxy("ALRedBallTracker")
        self.ball_detect = self._try_proxy("ALRedBallDetection")
        self.movement_detect = self._try_proxy("ALMovementDetection")
        self.darkness_detect = self._try_proxy("ALDarknessDetection")
        self.vision_recog = self._try_proxy("ALVisionRecognition")

        # state
        self._tracking_ball = False
        self._on_ball_callback = None
        self._last_ball_time = 0
        self._on_movement_callback = None
        self._last_movement_time = 0
        self._on_darkness_callback = None
        self._last_darkness_time = 0
        self._on_object_callback = None
        self._last_object_time = 0

    def _try_proxy(self, name):
        try:
            self.nao.env.add_proxy(name)
            return self.nao.env.proxies[name]
        except Exception as e:
            self.log('vision: {} not available: {}'.format(name, e))
            return None

    ###################################
    # red ball tracking
    ###################################

    def track_ball(self):
        if not self.ball_tracker:
            self.log('vision.track_ball: tracker not available')
            return self
        self.nao.env.motion.setStiffnesses("Head", 1.0)
        self.ball_tracker.setWholeBodyOn(False)
        self.ball_tracker.startTracker()
        self._tracking_ball = True
        self.log('vision.track_ball: started')
        return self

    def track_ball_whole_body(self):
        if not self.ball_tracker:
            self.log('vision.track_ball_whole_body: tracker not available')
            return self
        self.nao.env.motion.setStiffnesses("Head", 1.0)
        self.nao.env.motion.setStiffnesses("Body", 1.0)
        self.ball_tracker.setWholeBodyOn(True)
        self.ball_tracker.startTracker()
        self._tracking_ball = True
        self.log('vision.track_ball_whole_body: started')
        return self

    def stop_tracking_ball(self):
        if not self.ball_tracker:
            return self
        self.ball_tracker.stopTracker()
        self.nao.env.motion.setStiffnesses("Head", 0)
        self._tracking_ball = False
        self.log('vision.stop_tracking_ball: stopped')
        return self

    def ball_position(self):
        if not self.ball_tracker:
            return None
        return self.ball_tracker.getPosition()

    def is_tracking_ball(self):
        return self._tracking_ball

    def on_ball(self, callback):
        if not self.ball_detect:
            self.log('vision.on_ball: detection not available')
            return self
        self._on_ball_callback = callback
        self.ball_detect.subscribe("fluentnao_ball")
        memory.subscribeToEvent('redBallDetected', self._ball_event_cb)
        self.log('vision.on_ball: subscribed')
        return self

    def stop_on_ball(self):
        if not self.ball_detect:
            return self
        memory.unsubscribeToEvent('redBallDetected')
        self.ball_detect.unsubscribe("fluentnao_ball")
        self._on_ball_callback = None
        self.log('vision.stop_on_ball: unsubscribed')
        return self

    def _ball_event_cb(self, dataName, value, message):
        if self._on_ball_callback and value:
            now = time.time()
            if now - self._last_ball_time > 3:
                self._last_ball_time = now
                self._on_ball_callback(value)

    ###################################
    # object/picture recognition
    ###################################

    def _push_and_learn(self, local_path, name):
        ssh('mkdir -p {}'.format(NAO_LEARN_DIR))
        remote_path = '{}/{}'.format(NAO_LEARN_DIR, os.path.basename(local_path))
        result = scp_to_nao(local_path, remote_path)

        if result != 0:
            self.log('vision: failed to push {} to NAO'.format(local_path))
            return False

        success = self.vision_recog.learnFromFile(remote_path, name, [], False, True)
        ssh('rm -f {}'.format(remote_path))
        self.log('vision: learned {} (success={})'.format(name, success))
        return success

    def learn_object(self, name, countdown=True):
        if not self.vision_recog:
            self.log('vision.learn_object: not available')
            return self

        if countdown:
            self.nao.say_and_block('show me the {}'.format(name))
            self.nao.say_and_block('3')
            self.nao.say_and_block('2')
            self.nao.say_and_block('1')

        # take photo using camera module (VGA for detail)
        photo_path = self.nao.camera.photo('_learn_{}'.format(name), resolution=2)
        if not photo_path:
            self.log('vision.learn_object: photo capture failed')
            return self

        self._push_and_learn(photo_path, name)

        if countdown:
            self.nao.say('got it, I learned the {}'.format(name))

        return self

    def learn_from_file(self, filepath, name=None):
        if not self.vision_recog:
            self.log('vision.learn_from_file: not available')
            return self

        if not name:
            name = os.path.splitext(os.path.basename(filepath))[0]

        self._push_and_learn(filepath, name)
        return self

    def learn_all(self, folder='/object_detection'):
        if not self.vision_recog:
            self.log('vision.learn_all: not available')
            return self

        files = glob.glob('{}/*'.format(folder))
        count = 0
        for f in files:
            if os.path.isfile(f):
                self.learn_from_file(f)
                count += 1

        self.log('vision.learn_all: learned {} objects from {}'.format(count, folder))
        if count > 0:
            self.nao.say('I learned {} objects'.format(count))
        return self

    def forget_all_objects(self):
        if not self.vision_recog:
            return self
        self.vision_recog.clearCurrentDatabase()
        self.log('vision.forget_all_objects: cleared')
        return self

    def on_object(self, callback):
        if not self.vision_recog:
            self.log('vision.on_object: not available')
            return self
        self._on_object_callback = callback
        self.vision_recog.subscribe("fluentnao_vision")
        memory.subscribeToEvent('PictureDetected', self._object_event_cb)
        self.log('vision.on_object: subscribed')
        return self

    def stop_on_object(self):
        if not self.vision_recog:
            return self
        memory.unsubscribeToEvent('PictureDetected')
        self.vision_recog.unsubscribe("fluentnao_vision")
        self._on_object_callback = None
        self.log('vision.stop_on_object: unsubscribed')
        return self

    def _object_event_cb(self, dataName, value, message):
        if self._on_object_callback and value:
            now = time.time()
            if now - self._last_object_time > 3:
                self._last_object_time = now
                self._on_object_callback(value)

    ###################################
    # movement detection
    ###################################

    def on_movement(self, callback):
        if not self.movement_detect:
            self.log('vision.on_movement: not available')
            return self
        self._on_movement_callback = callback
        self.movement_detect.subscribe("fluentnao_movement")
        memory.subscribeToEvent('MovementDetection/MovementDetected', self._movement_event_cb)
        self.log('vision.on_movement: subscribed')
        return self

    def stop_on_movement(self):
        if not self.movement_detect:
            return self
        memory.unsubscribeToEvent('MovementDetection/MovementDetected')
        self.movement_detect.unsubscribe("fluentnao_movement")
        self._on_movement_callback = None
        self.log('vision.stop_on_movement: unsubscribed')
        return self

    def _movement_event_cb(self, dataName, value, message):
        if self._on_movement_callback and value:
            now = time.time()
            if now - self._last_movement_time > 3:
                self._last_movement_time = now
                self._on_movement_callback(value)

    ###################################
    # darkness detection
    ###################################

    def on_darkness(self, callback):
        if not self.darkness_detect:
            self.log('vision.on_darkness: not available')
            return self
        self._on_darkness_callback = callback
        self.darkness_detect.subscribe("fluentnao_darkness")
        memory.subscribeToEvent('DarknessDetection/DarknessDetected', self._darkness_event_cb)
        self.log('vision.on_darkness: subscribed')
        return self

    def stop_on_darkness(self):
        if not self.darkness_detect:
            return self
        memory.unsubscribeToEvent('DarknessDetection/DarknessDetected')
        self.darkness_detect.unsubscribe("fluentnao_darkness")
        self._on_darkness_callback = None
        self.log('vision.stop_on_darkness: unsubscribed')
        return self

    def is_dark(self):
        if not self.darkness_detect:
            return None
        try:
            return self.nao.env.memory.getData("DarknessDetection/DarknessDetected")
        except Exception:
            return None

    def _darkness_event_cb(self, dataName, value, message):
        if self._on_darkness_callback and value:
            now = time.time()
            if now - self._last_darkness_time > 3:
                self._last_darkness_time = now
                self._on_darkness_callback(value)
