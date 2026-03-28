'''Central class for controlling a NAO robot. @author: Don Najd'''
import logging

from naoutil.naoenv import NaoEnvironment, make_environment
from fluentnao.core.arms import Arms
from fluentnao.core.elbows import Elbows
from fluentnao.core.feet import Feet
from fluentnao.core.hands import Hands
from fluentnao.core.head import Head
from fluentnao.core.joints import Joints
from fluentnao.core.legs import Legs
from fluentnao.core.wrists import Wrists
from fluentnao.core.leds import Leds
from fluentnao.core.audio import Audio
from fluentnao.core.naoscript import NaoScript
from fluentnao.core.camera import Camera
from fluentnao.core.vision import Vision
from fluentnao.core.people import People
from fluentnao.core.sensors import Sensors
from fluentnao.core.navigation import Navigation
from fluentnao.core.tracker import Tracker
from fluentnao.core.reach import Reach
from fluentnao.core.animations import POD, STAND, SIT
from fluentnao.core.recorder.recorder import Recorder

import almath
import math
import time

from datetime import datetime, timedelta

class Nao(object):
    """Fluent API for controlling a NAO robot.

    Created once at server startup. Holds references to all sub-modules.
    Most methods return self for chaining: nao.say('hi').arms.up().go()

    Sub-modules:
        Body:     nao.arms, nao.elbows, nao.wrists, nao.hands, nao.head, nao.legs, nao.feet
        Media:    nao.camera, nao.audio, nao.leds
        Vision:   nao.vision, nao.tracker
        People:   nao.people
        Sensors:  nao.sensors
        Movement: nao.navigation, nao.reach
        Other:    nao.recorder, nao.naoscript

    Key concepts:
        Duration:  nao.set_duration(1.5) sets default movement time
        Blocking:  nao.go() waits for all queued movements
        Stiffness: nao.stiff() enables motors, nao.relax() disables
        Postures:  nao.stand_init(), nao.sit(), nao.crouch()
        Safety:    always end with nao.sit() to prevent falls

    Chaining:
        nao.arms.up().go().say('done').hands.open().go()
        nao.video('clip').say_and_block('hi').stop_video()

    Raw SDK access (nao.env):
        For anything not wrapped by FluentNao, use nao.env to access NAOqi
        proxies directly. The env object provides every ALModule on the robot.

        Common proxies already available:
            nao.env.motion        -- ALMotion (joint control, walking, cartesian)
            nao.env.memory        -- ALMemory (sensor data, event subscription)
            nao.env.tts           -- ALTextToSpeech
            nao.env.robotPosture  -- ALRobotPosture
            nao.env.audioPlayer   -- ALAudioPlayer
            nao.env.leds          -- ALLeds
            nao.env.sonar         -- ALSonar

        Adding new proxies on the fly:
            nao.env.add_proxy('ALBehaviorManager')
            mgr = nao.env.proxies['ALBehaviorManager']
            mgr.runBehavior('animations/Stand/Gestures/Hey_1')

        Useful raw SDK examples:
            # Simultaneous multi-chain cartesian movement
            nao.env.motion.positionInterpolations(
                ['LArm', 'RArm'], 0, [left_path, right_path],
                [7, 7], [times, times], True)

            # Read any sensor value from ALMemory
            nao.env.memory.getData('Device/SubDeviceList/Battery/Charge/Sensor/Value')

            # Get robot system info
            nao.env.add_proxy('ALSystem')
            nao.env.proxies['ALSystem'].robotName()

            # List all running behaviors
            nao.env.add_proxy('ALBehaviorManager')
            nao.env.proxies['ALBehaviorManager'].getRunningBehaviors()

        Available NAOqi modules (confirmed on this robot):
            ALAutonomousLife, ALBehaviorManager, ALSystem, ALConnectionManager,
            ALNotificationManager, ALPreferences, ALResourceManager,
            ALBacklightingDetection, ALPhotoCapture, ALVideoRecorder,
            ALLandMarkDetection, ALTracker, ALInfrared, ALRobotModel,
            ALWorldRepresentation, ALChestButton, ALDiagnosis
    """

    def __init__(self, env, log_function=None):
        super(Nao, self).__init__()
        
        # jobs for threading
        self.jobs = []

        # env & log
        self.env = env
        self.log_function = log_function
        if not log_function:
            self.logger = logging.getLogger("fluentnao.nao.Nao")

        # facetracker
        try:
            self.env.add_proxy("ALFaceDetection")
            self.face_detect = self.env.proxies["ALFaceDetection"]
        except Exception:
            self.face_detect = None

        # animated speech proxy
        try:
            self.env.add_proxy("ALAnimatedSpeech")
            self.animated_speech = self.env.proxies["ALAnimatedSpeech"]
        except Exception:
            self.animated_speech = None

        # dialog
        try:
            self.env.add_proxy("ALDialog")
            self.dialog = self.env.proxies["ALDialog"]
            self.dialog.setLanguage("English")
            self.dialog.setASRConfidenceThreshold(.3)
        except Exception:
            self.dialog = None
    
        # joints
        self.joints = Joints()
        self.chains = self.joints.Chains

        # other
        self.naoscript = NaoScript(self)
        self.leds = Leds(self)
        self.audio = Audio(self)
        self.camera = Camera(self)
        self.vision = Vision(self)
        self.people = People(self)
        self.sensors = Sensors(self)
        self.navigation = Navigation(self)
        self.tracker = Tracker(self)
        self.reach = Reach(self)

        # head
        self.head = Head(self)
        
        # arms
        self.hands = Hands(self) 
        self.wrists = Wrists(self, self.hands) 
        self.elbows = Elbows(self, self.wrists, self.hands) 
        self.arms = Arms(self, self.elbows, self.wrists, self.hands) 
        
        # legs
        self.feet = Feet(self)
        self.legs = Legs(self, self.feet)

        # recorder
        self.recorder = Recorder(self)

        # global duration
        self.set_duration(1.5)

    def hot_reload(self):
        import fluentnao.core.ssh
        import fluentnao.core.arms
        import fluentnao.core.elbows
        import fluentnao.core.feet
        import fluentnao.core.hands
        import fluentnao.core.head
        import fluentnao.core.joints
        import fluentnao.core.legs
        import fluentnao.core.wrists
        import fluentnao.core.leds
        import fluentnao.core.audio
        import fluentnao.core.naoscript
        import fluentnao.core.camera
        import fluentnao.core.vision
        import fluentnao.core.people
        import fluentnao.core.sensors
        import fluentnao.core.navigation
        import fluentnao.core.tracker
        import fluentnao.core.reach
        import fluentnao.core.animations

        reload(fluentnao.core.ssh)
        reload(fluentnao.core.arms)
        reload(fluentnao.core.elbows)
        reload(fluentnao.core.feet)
        reload(fluentnao.core.hands)
        reload(fluentnao.core.head)
        reload(fluentnao.core.joints)
        reload(fluentnao.core.legs)
        reload(fluentnao.core.wrists)
        reload(fluentnao.core.leds)
        reload(fluentnao.core.audio)
        reload(fluentnao.core.naoscript)
        reload(fluentnao.core.camera)
        reload(fluentnao.core.vision)
        reload(fluentnao.core.people)
        reload(fluentnao.core.sensors)
        reload(fluentnao.core.navigation)
        reload(fluentnao.core.tracker)
        reload(fluentnao.core.reach)
        reload(fluentnao.core.animations)

        from fluentnao.core.joints import Joints
        from fluentnao.core.arms import Arms
        from fluentnao.core.elbows import Elbows
        from fluentnao.core.feet import Feet
        from fluentnao.core.hands import Hands
        from fluentnao.core.head import Head
        from fluentnao.core.legs import Legs
        from fluentnao.core.wrists import Wrists
        from fluentnao.core.leds import Leds
        from fluentnao.core.audio import Audio
        from fluentnao.core.naoscript import NaoScript
        from fluentnao.core.camera import Camera
        from fluentnao.core.vision import Vision
        from fluentnao.core.people import People
        from fluentnao.core.sensors import Sensors
        from fluentnao.core.navigation import Navigation
        from fluentnao.core.tracker import Tracker
        from fluentnao.core.reach import Reach
        from fluentnao.core.recorder.recorder import Recorder

        # refresh proxies created in __init__
        try:
            self.env.add_proxy("ALFaceDetection")
            self.face_detect = self.env.proxies["ALFaceDetection"]
        except Exception:
            self.face_detect = None
        try:
            self.env.add_proxy("ALAnimatedSpeech")
            self.animated_speech = self.env.proxies["ALAnimatedSpeech"]
        except Exception:
            self.animated_speech = None
        try:
            self.env.add_proxy("ALDialog")
            self.dialog = self.env.proxies["ALDialog"]
        except Exception:
            self.dialog = None

        self.joints = Joints()
        self.chains = self.joints.Chains
        self.naoscript = NaoScript(self)
        self.leds = Leds(self)
        self.audio = Audio(self)
        self.camera = Camera(self)
        self.vision = Vision(self)
        self.people = People(self)
        self.sensors = Sensors(self)
        self.navigation = Navigation(self)
        self.tracker = Tracker(self)
        self.reach = Reach(self)
        self.head = Head(self)
        self.hands = Hands(self)
        self.wrists = Wrists(self, self.hands)
        self.elbows = Elbows(self, self.wrists, self.hands)
        self.arms = Arms(self, self.elbows, self.wrists, self.hands)
        self.feet = Feet(self)
        self.legs = Legs(self, self.feet)
        self.recorder = Recorder(self)

        self.log('hot_reload: complete')
        return self

    def shutdown(self):
        self.camera.stop_tracking()
        self.camera.stop_recording()
        self.vision.stop_on_ball()
        self.vision.stop_on_object()
        self.vision.stop_on_movement()
        self.vision.stop_on_darkness()
        self.people.stop_all()
        self.tracker.stop()
        self.audio.stop_listening()
        self.audio.stop_sound_tracking()
        self.sensors.stop_all_touch()
        self.sit()
        self.log('shutdown: complete')
        return self

    def log(self, msg):
        if (self.log_function):
            self.log_function(str(datetime.now()) + "|" + msg)
        else:
            self.logger.debug(str(datetime.now()) + "|" + msg)

    def print_keyframe(self):
        print(self.recorder.keyframe())

    ###################################
    # video recording (audio + video)
    ###################################
    def video(self, name='clip', fps=15, resolution=None):
        self._video_name = name
        if resolution is not None:
            self.camera.set_resolution(resolution)
        self.camera.start_recording(name, fps=fps)
        self.audio.start_recording(name, channels=[0, 0, 1, 0], sample_rate=48000)
        self.log('video: started recording {}'.format(name))
        return self

    def stop_video(self):
        import os
        import subprocess

        self.camera.stop_recording()
        audio_path = self.audio.stop_recording()

        real_fps = getattr(self.camera, '_actual_fps', None) or self.camera._record_fps or 10
        self.log('stop_video: using {:.1f} fps'.format(real_fps))

        video_path = self.camera.to_video(fps=real_fps)

        if video_path and audio_path:
            merged = video_path.replace('.mp4', '_av.mp4')
            cmd = 'avconv -y -i {} -i {} -c:v copy -c:a aac -strict experimental -ab 128k {}'.format(
                video_path, audio_path, merged)
            result = subprocess.call(cmd, shell=True)

            if result == 0:
                os.remove(video_path)
                os.remove(audio_path)
                final = video_path
                os.rename(merged, final)
                self.log('stop_video: created {}'.format(final))
                return final
            else:
                self.log('stop_video: merge failed, keeping separate files')
                return video_path
        elif video_path:
            self.log('stop_video: no audio, video only at {}'.format(video_path))
            return video_path
        else:
            self.log('stop_video: failed')
            return None

    ###################################
    # text to speech
    ###################################
    def say(self, text):
        self.env.tts.post.say(text)
        return self;

    def say_and_block(self, text):
        self.env.tts.say(text)
        return self;

    def wait(self, seconds):
        time.sleep(seconds)
        return self;

    def pod_say(self, key, text):
        s = "^start(" + POD[key] + ") " + text
        self.animate_say(s)

    def stand_say(self, key, text):
        s = "^start(" + STAND[key] + ") " + text
        self.animate_say(s)

    def sit_say(self, key, text):
        s = "^start(" + SIT[key] + ") " + text
        self.animate_say(s)

    def animate_say(self, text):
        if self.animated_speech:
            self.animated_speech.say(text)

    ###################################
    # Autonomous behavior
    ###################################
    def expressive_listening(self, enabled):
        try:
            self.env.add_proxy("ALAutonomousMoves")
            self.env.proxies["ALAutonomousMoves"].setExpressiveListeningEnabled(enabled)
        except Exception as e:
            self.log('expressive_listening: {}'.format(e))
        return self

    def audio_expression(self, enabled):
        try:
            self.env.speechRecognition.setAudioExpression(enabled)
        except Exception as e:
            self.log('audio_expression: {}'.format(e))
        return self

    def visual_expression(self, enabled):
        try:
            self.env.speechRecognition.setVisualExpression(enabled)
        except Exception as e:
            self.log('visual_expression: {}'.format(e))
        return self

    def be_still(self):
        self.expressive_listening(False)
        self.audio_expression(False)
        self.visual_expression(False)
        return self

    ###################################
    # Postures
    ###################################
    def stand_init(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("StandInit", speed))
        taskId = self.env.robotPosture.post.goToPosture("StandInit", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def sit_relax(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("SitRelax", speed))
        taskId = self.env.robotPosture.post.goToPosture("SitRelax", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def stand_zero(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("StandZero", speed))
        taskId = self.env.robotPosture.post.goToPosture("StandZero", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def lying_belly(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("LyingBelly", speed))
        taskId = self.env.robotPosture.post.goToPosture("LyingBelly", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def lying_back(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("LyingBack", speed))
        taskId = self.env.robotPosture.post.goToPosture("LyingBack", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def stand(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("Stand", speed))
        self.env.robotPosture.goToPosture("Stand", speed)
        self.env.motion.waitUntilMoveIsFinished();
        return self;
    
    def crouch(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("Crouch", speed))
        taskId = self.env.robotPosture.post.goToPosture("Crouch", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def sit(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("Sit", speed))
        self.env.robotPosture.post.goToPosture("Sit", speed)
        self.env.motion.waitUntilMoveIsFinished();
        return self;


    ###################################
    # stiffness
    ###################################
    def stiff(self):
        pNames = self.joints.Chains.Body
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    def rest(self):
        self.env.motion.rest()
        return self;

    def relax(self):
        pNames = self.joints.Chains.Body
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    ###################################
    # Whole Body Motion & Balance
    ###################################
    def whole_body_disable(self):
        self.log("wbDisable")
        isEnabled  = False
        self.env.motion.wbEnable(isEnabled)
        return self

    def whole_body_enable(self):
        self.log("wbEnable")
        isEnabled  = True
        self.env.motion.wbEnable(isEnabled)
        return self

    def foot_state(self, supportLeg="Legs", stateName="Fixed"):
        # Legs are constrained fixed
        # supportLeg: Legs, LLeg or RLeg
        # stateName: Fixed, Plane or Free
        self.log("supportLeg=%s|stateName=%s" % (supportLeg, stateName))
        self.env.motion.wbFootState(stateName, supportLeg)

    def constrain_motion(self, supportLeg="Legs"):
        # Constraint Balance Motion / Support Polygon
        # supportLeg: Legs, LLeg or RLeg
        isEnable   = True
        self.env.motion.wbEnableBalanceConstraint(isEnable, supportLeg)

    def balance(self, leg, duration):

        duration = self.determine_duration(duration)  

        # stiffen body
        self.stiff()
        self.whole_body_enable()

        self.foot_state()
        self.constrain_motion()

        # Com go to LLeg
        supportLeg = leg
        self.env.motion.wbGoToBalance(supportLeg, duration)

        self.whole_body_disable()
        return self


    ###################################
    # Duration 
    ###################################
    def set_duration(self, durationInSeconds):
        self.globalDuration = durationInSeconds
        return self;

    def determine_duration(self, durationInSeconds):
        if durationInSeconds > 0:
            return durationInSeconds

        return self.globalDuration

    ###################################
    # blocking
    ###################################
    
    def go(self):
        for taskId in self.jobs:

            self.log("taskId=%s|action=wait" % (taskId))
            d1 = datetime.now()
            self.env.motion.wait(taskId, 8000)   
            d2 = datetime.now()
            r = d2 - d1
            self.log("taskId=%s|action=done|seconds=%s" % (taskId, r.total_seconds()))

        self.jobs[:] = []
        self.log("done")
        
        return self         
            
    ###################################
    # movement
    ###################################

    def move(self, chain, angleListInRadians, timeListInSeconds):
        
        # motion w/ blocking call
        taskId = self.env.motion.post.angleInterpolation(chain, angleListInRadians, timeListInSeconds, True)    

        # log
        self.log("|taskId=%s|chain=%s|angleList=%s" % (taskId, chain, angleListInRadians))
        self.jobs.append(taskId)

    def move_with_degrees_and_duration(self, jointName, angleInDegrees, durationInSeconds):

        # convert to radians
        angleInRadians = angleInDegrees * almath.TO_RAD

        # move
        self.move(jointName, [angleInRadians], durationInSeconds)

    ###################################
    # joint info
    ###################################

    def joint_limits(self, chain='Body'):
        joints = self.env.motion.getJointNames(chain)
        limits = {}
        for j in joints:
            lim = self.env.motion.getLimits(j)
            limits[j] = {
                'min': round(math.degrees(lim[0][0]), 1),
                'max': round(math.degrees(lim[0][1]), 1),
                'max_speed': round(math.degrees(lim[0][2]), 1)
            }
        return limits

    def joint_angles(self, chain='Body', use_sensors=False):
        joints = self.env.motion.getJointNames(chain)
        angles = self.env.motion.getAngles(chain, use_sensors)
        return dict(zip(joints, [round(math.degrees(a), 1) for a in angles]))

    ###################################
    # helpers
    ###################################

    def get_target_angles_for_chain(self, chain, angle):
        # Get the Number of Joints
        numBodies = len(self.env.motion.getJointNames(chain))
    
        # We prepare a collection of floats
        return [angle] * numBodies

    def get_max_degrees_per_second(self, jointName):
        limits = self.env.motion.getLimits(jointName);
        minAngle = limits[0][0]
        maxAngle = limits[0][1]
        maxChange = limits[0][2]  # in rad.s-1

        #self.log("maxChange: " + str(maxChange) + " for " + jointName)
        return math.degrees(maxChange)

    def get_fraction_max_speed(self, jointName, desiredPositionInDegrees, executionTimeInSeconds):
        # current position in degrees
        useSensors = False;
        currentPositionInDegrees = math.degrees(self.env.motion.getAngles(jointName, useSensors)[0]);
        #self.log("pos in deg: " + str(currentPositionInDegrees))

        # distance
        distanceInDegrees = abs(currentPositionInDegrees - desiredPositionInDegrees)
        #self.log("distance: " + str(distanceInDegrees))

        # max speed
        maxDegreesPerSecond = self.get_max_degrees_per_second(jointName)

        # fractionOfMaxSpeed = (distanceInDegrees) / (maxDegreesPerSecond * executionTimeInSeconds)
        fractionOfMaxSpeed = (distanceInDegrees) / (maxDegreesPerSecond * executionTimeInSeconds)

        if fractionOfMaxSpeed > 1.0:
            return 1.0
        return fractionOfMaxSpeed

    ###################################
    # Misc
    ###################################
    
    def learn_face(self, name):
        if self.face_detect:
            self.face_detect.learnFace(name)

    def prep_sonar(self):
        self.env.sonar.subscribe("nao")

    def read_sonar(self):
        left = self.env.memory.getData('Device/SubDeviceList/US/Left/Sensor/Value')
        right = self.env.memory.getData('Device/SubDeviceList/US/Right/Sensor/Value')
        return [left, right]
    
    def is_something_close(self):
        r = self.read_sonar()
        if r[0] < 0.3 or r[1] < 0.3:
            return True
        return False

    ###################################
    # walking
    ###################################

    def walk_and_avoid(self):
        while True:
            self.walk_until_something_close()
            self.turn_away()

    def turn_away(self):
        self.walk_back(1,4)
        self.turn_left(1,2)
        while self.is_something_close():
            self.walk_back(1,4)
            self.turn_left(1,2)

    def walk_until_something_close(self):
        self.prep_sonar()
        self.walk(1,0,0,1)
        while not self.is_something_close():
            self.wait(0.2)
        self.stop_walking()

    def prep_walk(self, with_arms=False):
        self.env.motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
        if with_arms:
            self.env.motion.setWalkArmsEnabled(True, True)
    
    def unprep_walk(self):
        self.env.motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])

    def walk(self, x, y, theta, speed):
        self.env.motion.setWalkTargetVelocity(x, y, theta, speed)

    def stop_walking(self):
        self.env.motion.setWalkTargetVelocity(0,0,0,0)

    def walk_then_stop(self, x, y, theta, speed, duration):
        self.prep_walk()    
        self.walk(x, y, theta, speed)
        self.wait(duration)
        self.stop_walking()
        self.unprep_walk()

    def walk_back(self, speed=1, duration=1):
        self.walk_then_stop(-1, 0, 0, speed, duration)

    def walk_forward(self, speed=1, duration=1):
        self.walk_then_stop(1, 0, 0, speed, duration)

    def turn_left(self, speed=1, duration=1):
        self.walk_then_stop(1, 0, 1, speed, duration)

    def turn_right(self, speed=1, duration=1):
        self.walk_then_stop(1, 0, -1, speed, duration)



