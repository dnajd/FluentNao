import time
import os
from naoutil import memory
from fluentnao.core.ssh import ssh, scp_to_nao

NAO_LEARN_DIR = '/home/nao/learn'

class Vision:
    def __init__(self, nao):
        self.nao = nao
        self.log = nao.log
        self.env = nao.env
        
        # vision proxies
        try:
            self.env.add_proxy("ALFaceDetection")
            self.face_detect = self.env.proxies["ALFaceDetection"]
        except Exception:
            self.face_detect = None

        try:
            self.env.add_proxy("ALRedBallDetection")
            self.ball_detect = self.env.proxies["ALRedBallDetection"]
        except Exception:
            self.ball_detect = None

        try:
            self.env.add_proxy("ALVisionRecognition")
            self.vision_recog = self.env.proxies["ALVisionRecognition"]
        except Exception:
            self.vision_recog = None

        try:
            self.env.add_proxy("ALMovementDetection")
            self.movement_detect = self.env.proxies["ALMovementDetection"]
        except Exception:
            self.movement_detect = None

        try:
            self.env.add_proxy("ALDarknessDetection")
            self.darkness_detect = self.env.proxies["ALDarknessDetection"]
        except Exception:
            self.darkness_detect = None

        self._on_ball_callback = None
        self._last_ball_time = 0
        self._on_picture_callback = None
        self._last_picture_time = 0
        self._on_movement_callback = None
        self._last_movement_time = 0
        self._on_darkness_callback = None
        self._last_darkness_time = 0

    ###################################
    # face detection
    ###################################

    def on_face(self, callback):
        if not self.face_detect:
            self.log('vision.on_face: not available')
            return self
        self.face_detect.subscribe("fluentnao_face")
        memory.subscribeToEvent(self.nao.events.vision.faceDetected, callback)
        self.log('vision.on_face: subscribed')
        return self

    def stop_on_face(self):
        if not self.face_detect:
            return self
        memory.unsubscribeToEvent(self.nao.events.vision.faceDetected)
        try:
            self.face_detect.unsubscribe("fluentnao_face")
        except Exception:
            pass
        self.log('vision.stop_on_face: unsubscribed')
        return self

    ###################################
    # red ball detection
    ###################################

    def on_ball(self, callback):
        if not self.ball_detect:
            self.log('vision.on_ball: not available')
            return self
        self._on_ball_callback = callback
        self.ball_detect.subscribe("fluentnao_ball")
        memory.subscribeToEvent(self.nao.events.vision.redBallDetected, self._ball_event_cb)
        self.log('vision.on_ball: subscribed')
        return self

    def stop_on_ball(self):
        if not self.ball_detect:
            return self
        try:
            memory.unsubscribeToEvent(self.nao.events.vision.redBallDetected)
        except Exception:
            pass
        try:
            self.ball_detect.unsubscribe("fluentnao_ball")
        except Exception:
            pass
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
            self.nao.say("Ready in three, two, one. Snap!")
            
        local_path = self.nao.camera.photo('learn_{}'.format(name))
        self._push_and_learn(local_path, name)
        return self

    def on_object(self, callback):
        if not self.vision_recog:
            self.log('vision.on_object: not available')
            return self
        self._on_picture_callback = callback
        self.vision_recog.subscribe("fluentnao_vision")
        memory.subscribeToEvent(self.nao.events.vision.pictureDetected, self._picture_event_cb)
        self.log('vision.on_object: subscribed')
        return self

    def stop_on_object(self):
        if not self.vision_recog:
            return self
        try:
            memory.unsubscribeToEvent(self.nao.events.vision.pictureDetected)
        except Exception:
            pass
        try:
            self.vision_recog.unsubscribe("fluentnao_vision")
        except Exception:
            pass
        self._on_picture_callback = None
        self.log('vision.stop_on_object: unsubscribed')
        return self

    def _picture_event_cb(self, dataName, value, message):
        if self._on_picture_callback and value:
            now = time.time()
            if now - self._last_picture_time > 3:
                self._last_picture_time = now
                self._on_picture_callback(value)

    ###################################
    # movement detection
    ###################################

    def on_movement(self, callback):
        if not self.movement_detect:
            self.log('vision.on_movement: not available')
            return self
        self._on_movement_callback = callback
        self.movement_detect.subscribe("fluentnao_movement")
        memory.subscribeToEvent(self.nao.events.vision.movementDetected, self._movement_event_cb)
        self.log('vision.on_movement: subscribed')
        return self

    def stop_on_movement(self):
        if not self.movement_detect:
            return self
        try:
            memory.unsubscribeToEvent(self.nao.events.vision.movementDetected)
        except Exception:
            pass
        try:
            self.movement_detect.unsubscribe("fluentnao_movement")
        except Exception:
            pass
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
        memory.subscribeToEvent(self.nao.events.vision.darknessDetected, self._darkness_event_cb)
        self.log('vision.on_darkness: subscribed')
        return self

    def stop_on_darkness(self):
        if not self.darkness_detect:
            return self
        try:
            memory.unsubscribeToEvent(self.nao.events.vision.darknessDetected)
        except Exception:
            pass
        try:
            self.darkness_detect.unsubscribe("fluentnao_darkness")
        except Exception:
            pass
        self._on_darkness_callback = None
        self.log('vision.stop_on_darkness: unsubscribed')
        return self

    def _darkness_event_cb(self, dataName, value, message):
        if self._on_darkness_callback and value:
            now = time.time()
            if now - self._last_darkness_time > 3:
                self._last_darkness_time = now
                self._on_darkness_callback(value)
