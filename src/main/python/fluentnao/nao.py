'''
Created on 31st October , 2012

@author: Don Najd

'''
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
from fluentnao.core.animations import POD, STAND, SIT

import almath
import math
import time

from datetime import datetime, timedelta

class Nao(object):

    # init method
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
        self.env.add_proxy("ALFaceDetection")   
        self.face_detect = self.env.proxies["ALFaceDetection"] 
    
        # animated speech proxy
        self.env.add_proxy("ALAnimatedSpeech")   
        self.animated_speech = self.env.proxies["ALAnimatedSpeech"] 
    
        # joints
        self.joints = Joints()
        self.chains = self.joints.Chains

        # other
        self.naoscript = NaoScript(self)
        self.leds = Leds(self)
        self.audio = Audio(self)

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

        # global duration
        self.set_duration(1.5)

    def log(self, msg):
        if (self.log_function):
            self.log_function(str(datetime.now()) + "|" + msg)
        else:
            self.logger.debug(str(datetime.now()) + "|" + msg)

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
        self.animated_speech.say(text) 

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

    def whole_body_enable(self):
        self.log("wbEnable")
        isEnabled  = True
        self.env.motion.wbEnable(isEnabled)

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

        if fractionOfMaxSpeed > maxDegreesPerSecond:
            return maxDegreesPerSecond
        return fractionOfMaxSpeed

    ###################################
    # Misc
    ###################################
    
    def learn_face(name):
        self.face_detect.learnFace(name)


###################################
# development
###################################
def init_modules_for_development(pathToCore):

    import sys
    sys.path.append(pathToCore)
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

    reload(fluentnao.core.arms)
    reload(fluentnao.core.joints)
    reload(fluentnao.core.hands)
    reload(fluentnao.core.elbows)
    reload(fluentnao.core.wrists)
    reload(fluentnao.core.legs)
    reload(fluentnao.core.head)
    reload(fluentnao.core.feet)
    reload(fluentnao.core.leds)
    reload(fluentnao.core.audio)
    reload(fluentnao.core.naoscript)

