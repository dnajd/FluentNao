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

    def animate_say(self, key, text):
        s = "^start(" + animations[key] + ") " + text
        self.animated_speech.say(s) 


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


###################################
# Animations
###################################

animations = {'Listening_6': 'animations/SitOnPod/BodyTalk/Listening/Listening_6',
'Listening_2': 'animations/SitOnPod/BodyTalk/Listening/Listening_2',
'Listening_3': 'animations/SitOnPod/BodyTalk/Listening/Listening_3',
'Listening_7': 'animations/SitOnPod/BodyTalk/Listening/Listening_7',
'Listening_5': 'animations/SitOnPod/BodyTalk/Listening/Listening_5',
'Listening_4': 'animations/SitOnPod/BodyTalk/Listening/Listening_4',
'Listening_1': 'animations/SitOnPod/BodyTalk/Listening/Listening_1',
'Listening_8': 'animations/SitOnPod/BodyTalk/Listening/Listening_8',
'Remember_3': 'animations/SitOnPod/BodyTalk/Thinking/Remember_3',
'ThinkingLoop_2': 'animations/SitOnPod/BodyTalk/Thinking/ThinkingLoop_2',
'Remember_2': 'animations/SitOnPod/BodyTalk/Thinking/Remember_2',
'Remember_1': 'animations/SitOnPod/BodyTalk/Thinking/Remember_1',
'ThinkingLoop_1': 'animations/SitOnPod/BodyTalk/Thinking/ThinkingLoop_1',
'BodyTalk_12': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_12',
'BodyTalk_4': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_4',
'BodyTalk_9': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_9',
'BodyTalk_10': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_10',
'BodyTalk_6': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_6',
'BodyTalk_5': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_5',
'BodyTalk_7': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_7',
'BodyTalk_11': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_11',
'BodyTalk_1': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_1',
'BodyTalk_8': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_8',
'BodyTalk_2': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_2',
'BodyTalk_3': 'animations/SitOnPod/BodyTalk/Speaking/BodyTalk_3',
'Hello_1': 'animations/SitOnPod/Emotions/Neutral/Hello_1',
'Yes_1': 'animations/SitOnPod/Gestures/Yes_1',
'Me_7': 'animations/SitOnPod/Gestures/Me_7',
'Yes_2': 'animations/SitOnPod/Gestures/Yes_2',
'WhatSThis_6': 'animations/SitOnPod/Gestures/WhatSThis_6',
'Everything_4': 'animations/SitOnPod/Gestures/Everything_4',
'Me_1': 'animations/SitOnPod/Gestures/Me_1',
'WhatSThis_14': 'animations/SitOnPod/Gestures/WhatSThis_14',
'No_2': 'animations/SitOnPod/Gestures/No_2',
'This_7': 'animations/SitOnPod/Gestures/This_7',
'This_6': 'animations/SitOnPod/Gestures/This_6',
'Me_8': 'animations/SitOnPod/Gestures/Me_8',
'Hey_3': 'animations/SitOnPod/Gestures/Hey_3',
'WhatSThis_15': 'animations/SitOnPod/Gestures/WhatSThis_15',
'This_1': 'animations/SitOnPod/Gestures/This_1',
'CountTwo_1': 'animations/SitOnPod/Gestures/CountTwo_1',
'Hey_7': 'animations/SitOnPod/Gestures/Hey_7',
'This_9': 'animations/SitOnPod/Gestures/This_9',
'Me_2': 'animations/SitOnPod/Gestures/Me_2',
'No_5': 'animations/SitOnPod/Gestures/No_5',
'This_15': 'animations/SitOnPod/Gestures/This_15',
'No_1': 'animations/SitOnPod/Gestures/No_1',
'Hey_1': 'animations/SitOnPod/Gestures/Hey_1',
'This_12': 'animations/SitOnPod/Gestures/This_12',
'This_4': 'animations/SitOnPod/Gestures/This_4',
'This_2': 'animations/SitOnPod/Gestures/This_2',
'You_5': 'animations/SitOnPod/Gestures/You_5',
'This_5': 'animations/SitOnPod/Gestures/This_5',
'WhatSThis_4': 'animations/SitOnPod/Gestures/WhatSThis_4',
'WhatSThis_3': 'animations/SitOnPod/Gestures/WhatSThis_3',
'This_13': 'animations/SitOnPod/Gestures/This_13',
'Yes_3': 'animations/SitOnPod/Gestures/Yes_3',
'WhatSThis_2': 'animations/SitOnPod/Gestures/WhatSThis_2',
'No_3': 'animations/SitOnPod/Gestures/No_3',
'This_3': 'animations/SitOnPod/Gestures/This_3',
'Hey_6': 'animations/SitOnPod/Gestures/Hey_6',
'Hey_2': 'animations/SitOnPod/Gestures/Hey_2',
'You_1': 'animations/SitOnPod/Gestures/You_1',
'WhatSThis_11': 'animations/SitOnPod/Gestures/WhatSThis_11',
'Choice_1': 'animations/SitOnPod/Gestures/Choice_1',
'You_2': 'animations/SitOnPod/Gestures/You_2',
'Everything_6': 'animations/SitOnPod/Gestures/Everything_6',
'WhatSThis_5': 'animations/SitOnPod/Gestures/WhatSThis_5',
'HeSays_2': 'animations/SitOnPod/Gestures/HeSays_2',
'WhatSThis_7': 'animations/SitOnPod/Gestures/WhatSThis_7',
'No_9': 'animations/SitOnPod/Gestures/No_9',
'WhatSThis_9': 'animations/SitOnPod/Gestures/WhatSThis_9',
'This_8': 'animations/SitOnPod/Gestures/This_8',
'WhatSThis_1': 'animations/SitOnPod/Gestures/WhatSThis_1',
'CountThree_1': 'animations/SitOnPod/Gestures/CountThree_1',
'WhatSThis_12': 'animations/SitOnPod/Gestures/WhatSThis_12',
'HeSays_1': 'animations/SitOnPod/Gestures/HeSays_1',
'You_3': 'animations/SitOnPod/Gestures/You_3',
'This_14': 'animations/SitOnPod/Gestures/This_14',
'Me_4': 'animations/SitOnPod/Gestures/Me_4',
'You_4': 'animations/SitOnPod/Gestures/You_4',
'No_7': 'animations/SitOnPod/Gestures/No_7',
'Everything_1': 'animations/SitOnPod/Gestures/Everything_1',
'HeSays_3': 'animations/SitOnPod/Gestures/HeSays_3',
'WhatSThis_8': 'animations/SitOnPod/Gestures/WhatSThis_8',
'No_4': 'animations/SitOnPod/Gestures/No_4',
'This_10': 'animations/SitOnPod/Gestures/This_10',
'No_8': 'animations/SitOnPod/Gestures/No_8',
'WhatSThis_10': 'animations/SitOnPod/Gestures/WhatSThis_10',
'No_6': 'animations/SitOnPod/Gestures/No_6',
'WhatSThis_13': 'animations/SitOnPod/Gestures/WhatSThis_13',
'WhatSThis_16': 'animations/SitOnPod/Gestures/WhatSThis_16',
'This_11': 'animations/SitOnPod/Gestures/This_11',
'CountTwo_2': 'animations/SitOnPod/Gestures/CountTwo_2',
'Everything_2': 'animations/SitOnPod/Gestures/Everything_2',
'Everything_3': 'animations/SitOnPod/Gestures/Everything_3',
'CountThree_2': 'animations/SitOnPod/Gestures/CountThree_2',
'Hey_4': 'animations/SitOnPod/Gestures/Hey_4',
'Listening_2': 'animations/Stand/BodyTalk/Listening/Listening_2',
'ListeningLeft_1': 'animations/Stand/BodyTalk/Listening/ListeningLeft_1',
'ListeningRight_3': 'animations/Stand/BodyTalk/Listening/ListeningRight_3',
'ListeningRight_1': 'animations/Stand/BodyTalk/Listening/ListeningRight_1',
'ListeningLeft_3': 'animations/Stand/BodyTalk/Listening/ListeningLeft_3',
'Remember_3': 'animations/Stand/BodyTalk/Thinking/Remember_3',
'ThinkingLoop_2': 'animations/Stand/BodyTalk/Thinking/ThinkingLoop_2',
'Remember_2': 'animations/Stand/BodyTalk/Thinking/Remember_2',
'Remember_1': 'animations/Stand/BodyTalk/Thinking/Remember_1',
'ThinkingLoop_1': 'animations/Stand/BodyTalk/Thinking/ThinkingLoop_1',
'BodyTalk_19': 'animations/Stand/BodyTalk/Speaking/BodyTalk_19',
'BodyTalk_17': 'animations/Stand/BodyTalk/Speaking/BodyTalk_17',
'BodyTalk_22': 'animations/Stand/BodyTalk/Speaking/BodyTalk_22',
'BodyTalk_12': 'animations/Stand/BodyTalk/Speaking/BodyTalk_12',
'BodyTalk_4': 'animations/Stand/BodyTalk/Speaking/BodyTalk_4',
'BodyTalk_16': 'animations/Stand/BodyTalk/Speaking/BodyTalk_16',
'BodyTalk_18': 'animations/Stand/BodyTalk/Speaking/BodyTalk_18',
'BodyTalk_9': 'animations/Stand/BodyTalk/Speaking/BodyTalk_9',
'BodyTalk_10': 'animations/Stand/BodyTalk/Speaking/BodyTalk_10',
'BodyTalk_15': 'animations/Stand/BodyTalk/Speaking/BodyTalk_15',
'BodyTalk_6': 'animations/Stand/BodyTalk/Speaking/BodyTalk_6',
'BodyTalk_13': 'animations/Stand/BodyTalk/Speaking/BodyTalk_13',
'BodyTalk_21': 'animations/Stand/BodyTalk/Speaking/BodyTalk_21',
'BodyTalk_5': 'animations/Stand/BodyTalk/Speaking/BodyTalk_5',
'BodyTalk_7': 'animations/Stand/BodyTalk/Speaking/BodyTalk_7',
'BodyTalk_11': 'animations/Stand/BodyTalk/Speaking/BodyTalk_11',
'BodyTalk_1': 'animations/Stand/BodyTalk/Speaking/BodyTalk_1',
'BodyTalk_14': 'animations/Stand/BodyTalk/Speaking/BodyTalk_14',
'BodyTalk_8': 'animations/Stand/BodyTalk/Speaking/BodyTalk_8',
'BodyTalk_2': 'animations/Stand/BodyTalk/Speaking/BodyTalk_2',
'BodyTalk_3': 'animations/Stand/BodyTalk/Speaking/BodyTalk_3',
'BodyTalk_20': 'animations/Stand/BodyTalk/Speaking/BodyTalk_20',
'SeeSomething_5': 'animations/Stand/Reactions/SeeSomething_5',
'LightShine_2': 'animations/Stand/Reactions/LightShine_2',
'SeeSomething_1': 'animations/Stand/Reactions/SeeSomething_1',
'TouchHead_3': 'animations/Stand/Reactions/TouchHead_3',
'SeeSomething_8': 'animations/Stand/Reactions/SeeSomething_8',
'BumperRight_1': 'animations/Stand/Reactions/BumperRight_1',
'TouchHead_2': 'animations/Stand/Reactions/TouchHead_2',
'EthernetOff_1': 'animations/Stand/Reactions/EthernetOff_1',
'SeeSomething_3': 'animations/Stand/Reactions/SeeSomething_3',
'LightShine_3': 'animations/Stand/Reactions/LightShine_3',
'SeeSomething_7': 'animations/Stand/Reactions/SeeSomething_7',
'SeeSomething_4': 'animations/Stand/Reactions/SeeSomething_4',
'LightShine_1': 'animations/Stand/Reactions/LightShine_1',
'SeeColor_1': 'animations/Stand/Reactions/SeeColor_1',
'SeeSomething_6': 'animations/Stand/Reactions/SeeSomething_6',
'BumperLeft_1': 'animations/Stand/Reactions/BumperLeft_1',
'TouchHead_1': 'animations/Stand/Reactions/TouchHead_1',
'Bumpers_1': 'animations/Stand/Reactions/Bumpers_1',
'ShakeBody_3': 'animations/Stand/Reactions/ShakeBody_3',
'EthernetOn_1': 'animations/Stand/Reactions/EthernetOn_1',
'SeeColor_2': 'animations/Stand/Reactions/SeeColor_2',
'Heat_2': 'animations/Stand/Reactions/Heat_2',
'ShakeBody_2': 'animations/Stand/Reactions/ShakeBody_2',
'SeeColor_3': 'animations/Stand/Reactions/SeeColor_3',
'Bumpers_3': 'animations/Stand/Reactions/Bumpers_3',
'LightShine_4': 'animations/Stand/Reactions/LightShine_4',
'ShakeBody_1': 'animations/Stand/Reactions/ShakeBody_1',
'Heat_1': 'animations/Stand/Reactions/Heat_1',
'Bumpers_2': 'animations/Stand/Reactions/Bumpers_2',
'TouchHead_4': 'animations/Stand/Reactions/TouchHead_4',
'Fear_2': 'animations/Stand/Emotions/Negative/Fear_2',
'Late_1': 'animations/Stand/Emotions/Negative/Late_1',
'Fearful_1': 'animations/Stand/Emotions/Negative/Fearful_1',
'Sorry_1': 'animations/Stand/Emotions/Negative/Sorry_1',
'Angry_3': 'animations/Stand/Emotions/Negative/Angry_3',
'Bored_1': 'animations/Stand/Emotions/Negative/Bored_1',
'Sad_2': 'animations/Stand/Emotions/Negative/Sad_2',
'Shocked_1': 'animations/Stand/Emotions/Negative/Shocked_1',
'Disappointed_1': 'animations/Stand/Emotions/Negative/Disappointed_1',
'Surprise_1': 'animations/Stand/Emotions/Negative/Surprise_1',
'Sad_1': 'animations/Stand/Emotions/Negative/Sad_1',
'Fear_1': 'animations/Stand/Emotions/Negative/Fear_1',
'Surprise_3': 'animations/Stand/Emotions/Negative/Surprise_3',
'Angry_2': 'animations/Stand/Emotions/Negative/Angry_2',
'Angry_4': 'animations/Stand/Emotions/Negative/Angry_4',
'Humiliated_1': 'animations/Stand/Emotions/Negative/Humiliated_1',
'Hurt_1': 'animations/Stand/Emotions/Negative/Hurt_1',
'Bored_2': 'animations/Stand/Emotions/Negative/Bored_2',
'Surprise_2': 'animations/Stand/Emotions/Negative/Surprise_2',
'Exhausted_2': 'animations/Stand/Emotions/Negative/Exhausted_2',
'Exhausted_1': 'animations/Stand/Emotions/Negative/Exhausted_1',
'Hurt_2': 'animations/Stand/Emotions/Negative/Hurt_2',
'Frustrated_1': 'animations/Stand/Emotions/Negative/Frustrated_1',
'Anxious_1': 'animations/Stand/Emotions/Negative/Anxious_1',
'Angry_1': 'animations/Stand/Emotions/Negative/Angry_1',
'Peaceful_1': 'animations/Stand/Emotions/Positive/Peaceful_1',
'Interested_1': 'animations/Stand/Emotions/Positive/Interested_1',
'Enthusiastic_1': 'animations/Stand/Emotions/Positive/Enthusiastic_1',
'Proud_2': 'animations/Stand/Emotions/Positive/Proud_2',
'Proud_1': 'animations/Stand/Emotions/Positive/Proud_1',
'Hungry_1': 'animations/Stand/Emotions/Positive/Hungry_1',
'Happy_4': 'animations/Stand/Emotions/Positive/Happy_4',
'Relieved_1': 'animations/Stand/Emotions/Positive/Relieved_1',
'Laugh_2': 'animations/Stand/Emotions/Positive/Laugh_2',
'Excited_2': 'animations/Stand/Emotions/Positive/Excited_2',
'Mocker_1': 'animations/Stand/Emotions/Positive/Mocker_1',
'Ecstatic_1': 'animations/Stand/Emotions/Positive/Ecstatic_1',
'Happy_1': 'animations/Stand/Emotions/Positive/Happy_1',
'Amused_1': 'animations/Stand/Emotions/Positive/Amused_1',
'Confident_1': 'animations/Stand/Emotions/Positive/Confident_1',
'Excited_3': 'animations/Stand/Emotions/Positive/Excited_3',
'Hysterical_1': 'animations/Stand/Emotions/Positive/Hysterical_1',
'Optimistic_1': 'animations/Stand/Emotions/Positive/Optimistic_1',
'Shy_1': 'animations/Stand/Emotions/Positive/Shy_1',
'Laugh_1': 'animations/Stand/Emotions/Positive/Laugh_1',
'Winner_2': 'animations/Stand/Emotions/Positive/Winner_2',
'Proud_3': 'animations/Stand/Emotions/Positive/Proud_3',
'Interested_2': 'animations/Stand/Emotions/Positive/Interested_2',
'Excited_1': 'animations/Stand/Emotions/Positive/Excited_1',
'Happy_2': 'animations/Stand/Emotions/Positive/Happy_2',
'Shy_2': 'animations/Stand/Emotions/Positive/Shy_2',
'Laugh_3': 'animations/Stand/Emotions/Positive/Laugh_3',
'Happy_3': 'animations/Stand/Emotions/Positive/Happy_3',
'Sure_1': 'animations/Stand/Emotions/Positive/Sure_1',
'Winner_1': 'animations/Stand/Emotions/Positive/Winner_1',
'Hello_1': 'animations/Stand/Emotions/Neutral/Hello_1',
'AskForAttention_3': 'animations/Stand/Emotions/Neutral/AskForAttention_3',
'Innocent_1': 'animations/Stand/Emotions/Neutral/Innocent_1',
'Hesitation_1': 'animations/Stand/Emotions/Neutral/Hesitation_1',
'AskForAttention_1': 'animations/Stand/Emotions/Neutral/AskForAttention_1',
'Confused_1': 'animations/Stand/Emotions/Neutral/Confused_1',
'Sneeze': 'animations/Stand/Emotions/Neutral/Sneeze',
'Cautious_1': 'animations/Stand/Emotions/Neutral/Cautious_1',
'Determined_1': 'animations/Stand/Emotions/Neutral/Determined_1',
'Annoyed_1': 'animations/Stand/Emotions/Neutral/Annoyed_1',
'Lonely_1': 'animations/Stand/Emotions/Neutral/Lonely_1',
'AskForAttention_2': 'animations/Stand/Emotions/Neutral/AskForAttention_2',
'Stubborn_1': 'animations/Stand/Emotions/Neutral/Stubborn_1',
'Suspicious_1': 'animations/Stand/Emotions/Neutral/Suspicious_1',
'Mischievous_1': 'animations/Stand/Emotions/Neutral/Mischievous_1',
'Puzzled_1': 'animations/Stand/Emotions/Neutral/Puzzled_1',
'Alienated_1': 'animations/Stand/Emotions/Neutral/Alienated_1',
'Embarrassed_1': 'animations/Stand/Emotions/Neutral/Embarrassed_1',
'Relaxation_3': 'animations/Stand/Waiting/Relaxation_3',
'ScratchTorso_1': 'animations/Stand/Waiting/ScratchTorso_1',
'LookHand_1': 'animations/Stand/Waiting/LookHand_1',
'CallSomeone_1': 'animations/Stand/Waiting/CallSomeone_1',
'WakeUp_1': 'animations/Stand/Waiting/WakeUp_1',
'Innocent_1': 'animations/Stand/Waiting/Innocent_1',
'ShowMuscles_5': 'animations/Stand/Waiting/ShowMuscles_5',
'Relaxation_2': 'animations/Stand/Waiting/Relaxation_2',
'Waddle_1': 'animations/Stand/Waiting/Waddle_1',
'Binoculars_1': 'animations/Stand/Waiting/Binoculars_1',
'ScratchBack_1': 'animations/Stand/Waiting/ScratchBack_1',
'TakePicture_1': 'animations/Stand/Waiting/TakePicture_1',
'ShowMuscles_4': 'animations/Stand/Waiting/ShowMuscles_4',
'FunnyDancer_1': 'animations/Stand/Waiting/FunnyDancer_1',
'ShowMuscles_1': 'animations/Stand/Waiting/ShowMuscles_1',
'Fitness_3': 'animations/Stand/Waiting/Fitness_3',
'Think_4': 'animations/Stand/Waiting/Think_4',
'DriveCar_1': 'animations/Stand/Waiting/DriveCar_1',
'Stretch_1': 'animations/Stand/Waiting/Stretch_1',
'LookHand_2': 'animations/Stand/Waiting/LookHand_2',
'ShowSky_2': 'animations/Stand/Waiting/ShowSky_2',
'Think_1': 'animations/Stand/Waiting/Think_1',
'Knight_1': 'animations/Stand/Waiting/Knight_1',
'FunnySlide_1': 'animations/Stand/Waiting/FunnySlide_1',
'Headbang_1': 'animations/Stand/Waiting/Headbang_1',
'HideHands_1': 'animations/Stand/Waiting/HideHands_1',
'Fitness_2': 'animations/Stand/Waiting/Fitness_2',
'MysticalPower_1': 'animations/Stand/Waiting/MysticalPower_1',
'ScratchHand_1': 'animations/Stand/Waiting/ScratchHand_1',
'ShowMuscles_2': 'animations/Stand/Waiting/ShowMuscles_2',
'Fitness_1': 'animations/Stand/Waiting/Fitness_1',
'BackRubs_1': 'animations/Stand/Waiting/BackRubs_1',
'ShowMuscles_3': 'animations/Stand/Waiting/ShowMuscles_3',
'Stretch_3': 'animations/Stand/Waiting/Stretch_3',
'Monster_1': 'animations/Stand/Waiting/Monster_1',
'Think_3': 'animations/Stand/Waiting/Think_3',
'Think_2': 'animations/Stand/Waiting/Think_2',
'Waddle_2': 'animations/Stand/Waiting/Waddle_2',
'WalkInTheShit_1': 'animations/Stand/Waiting/WalkInTheShit_1',
'Helicopter_1': 'animations/Stand/Waiting/Helicopter_1',
'Zombie_1': 'animations/Stand/Waiting/Zombie_1',
'LoveYou_1': 'animations/Stand/Waiting/LoveYou_1',
'Bandmaster_1': 'animations/Stand/Waiting/Bandmaster_1',
'KnockEye_1': 'animations/Stand/Waiting/KnockEye_1',
'AirJuggle_1': 'animations/Stand/Waiting/AirJuggle_1',
'Vacuum_1': 'animations/Stand/Waiting/Vacuum_1',
'ScratchHead_1': 'animations/Stand/Waiting/ScratchHead_1',
'Drink_1': 'animations/Stand/Waiting/Drink_1',
'Relaxation_1': 'animations/Stand/Waiting/Relaxation_1',
'Stretch_2': 'animations/Stand/Waiting/Stretch_2',
'HideEyes_1': 'animations/Stand/Waiting/HideEyes_1',
'ScratchEye_1': 'animations/Stand/Waiting/ScratchEye_1',
'Robot_1': 'animations/Stand/Waiting/Robot_1',
'ScratchLeg_1': 'animations/Stand/Waiting/ScratchLeg_1',
'AirGuitar_1': 'animations/Stand/Waiting/AirGuitar_1',
'PlayHands_1': 'animations/Stand/Waiting/PlayHands_1',
'KungFu_1': 'animations/Stand/Waiting/KungFu_1',
'ScratchBottom_1': 'animations/Stand/Waiting/ScratchBottom_1',
'PlayHands_3': 'animations/Stand/Waiting/PlayHands_3',
'SpaceShuttle_1': 'animations/Stand/Waiting/SpaceShuttle_1',
'PlayHands_2': 'animations/Stand/Waiting/PlayHands_2',
'Relaxation_4': 'animations/Stand/Waiting/Relaxation_4',
'ShowSky_1': 'animations/Stand/Waiting/ShowSky_1',
'Rest_1': 'animations/Stand/Waiting/Rest_1',
'HappyBirthday_1': 'animations/Stand/Waiting/HappyBirthday_1',
'Taxi_1': 'animations/Stand/Waiting/Taxi_1',
'Yes_1': 'animations/Stand/Gestures/Yes_1',
'Me_7': 'animations/Stand/Gestures/Me_7',
'But_1': 'animations/Stand/Gestures/But_1',
'Yes_2': 'animations/Stand/Gestures/Yes_2',
'JointHands_3': 'animations/Stand/Gestures/JointHands_3',
'Thinking_6': 'animations/Stand/Gestures/Thinking_6',
'WhatSThis_6': 'animations/Stand/Gestures/WhatSThis_6',
'ShowSky_12': 'animations/Stand/Gestures/ShowSky_12',
'Enthusiastic_1': 'animations/Stand/Gestures/Enthusiastic_1',
'Everything_4': 'animations/Stand/Gestures/Everything_4',
'Explain_11': 'animations/Stand/Gestures/Explain_11',
'Thinking_5': 'animations/Stand/Gestures/Thinking_5',
'Thinking_8': 'animations/Stand/Gestures/Thinking_8',
'Yum_1': 'animations/Stand/Gestures/Yum_1',
'Me_1': 'animations/Stand/Gestures/Me_1',
'Far_3': 'animations/Stand/Gestures/Far_3',
'Explain_8': 'animations/Stand/Gestures/Explain_8',
'WhatSThis_14': 'animations/Stand/Gestures/WhatSThis_14',
'Reject_5': 'animations/Stand/Gestures/Reject_5',
'CalmDown_6': 'animations/Stand/Gestures/CalmDown_6',
'IDontKnow_6': 'animations/Stand/Gestures/IDontKnow_6',
'Salute_3': 'animations/Stand/Gestures/Salute_3',
'No_2': 'animations/Stand/Gestures/No_2',
'This_7': 'animations/Stand/Gestures/This_7',
'Thinking_7': 'animations/Stand/Gestures/Thinking_7',
'ShowSky_8': 'animations/Stand/Gestures/ShowSky_8',
'Hungry_1': 'animations/Stand/Gestures/Hungry_1',
'This_6': 'animations/Stand/Gestures/This_6',
'Kisses_1': 'animations/Stand/Gestures/Kisses_1',
'Please_3': 'animations/Stand/Gestures/Please_3',
'Me_8': 'animations/Stand/Gestures/Me_8',
'CatchFly_2': 'animations/Stand/Gestures/CatchFly_2',
'Next_1': 'animations/Stand/Gestures/Next_1',
'Far_1': 'animations/Stand/Gestures/Far_1',
'Surprised_1': 'animations/Stand/Gestures/Surprised_1',
'Give_4': 'animations/Stand/Gestures/Give_4',
'Wings_4': 'animations/Stand/Gestures/Wings_4',
'Mime_1': 'animations/Stand/Gestures/Mime_1',
'Hey_3': 'animations/Stand/Gestures/Hey_3',
'Explain_4': 'animations/Stand/Gestures/Explain_4',
'Enthusiastic_3': 'animations/Stand/Gestures/Enthusiastic_3',
'Maybe_1': 'animations/Stand/Gestures/Maybe_1',
'ShowSky_3': 'animations/Stand/Gestures/ShowSky_3',
'Angry_3': 'animations/Stand/Gestures/Angry_3',
'Wings_1': 'animations/Stand/Gestures/Wings_1',
'WhatSThis_15': 'animations/Stand/Gestures/WhatSThis_15',
'OnTheEvening_1': 'animations/Stand/Gestures/OnTheEvening_1',
'This_1': 'animations/Stand/Gestures/This_1',
'CountTwo_1': 'animations/Stand/Gestures/CountTwo_1',
'Hey_7': 'animations/Stand/Gestures/Hey_7',
'Coaxing_1': 'animations/Stand/Gestures/Coaxing_1',
'Give_3': 'animations/Stand/Gestures/Give_3',
'This_9': 'animations/Stand/Gestures/This_9',
'CountOne_1': 'animations/Stand/Gestures/CountOne_1',
'Desperate_2': 'animations/Stand/Gestures/Desperate_2',
'CountFive_1': 'animations/Stand/Gestures/CountFive_1',
'Far_2': 'animations/Stand/Gestures/Far_2',
'Explain_9': 'animations/Stand/Gestures/Explain_9',
'Me_2': 'animations/Stand/Gestures/Me_2',
'Please_1': 'animations/Stand/Gestures/Please_1',
'No_5': 'animations/Stand/Gestures/No_5',
'Caress_2': 'animations/Stand/Gestures/Caress_2',
'Stretch_1': 'animations/Stand/Gestures/Stretch_1',
'Claw_2': 'animations/Stand/Gestures/Claw_2',
'ShowSky_2': 'animations/Stand/Gestures/ShowSky_2',
'Desperate_4': 'animations/Stand/Gestures/Desperate_4',
'YouKnowWhat_1': 'animations/Stand/Gestures/YouKnowWhat_1',
'Take_1': 'animations/Stand/Gestures/Take_1',
'Explain_10': 'animations/Stand/Gestures/Explain_10',
'Thinking_3': 'animations/Stand/Gestures/Thinking_3',
'Hide_1': 'animations/Stand/Gestures/Hide_1',
'This_15': 'animations/Stand/Gestures/This_15',
'Wings_3': 'animations/Stand/Gestures/Wings_3',
'Thinking_2': 'animations/Stand/Gestures/Thinking_2',
'Explain_3': 'animations/Stand/Gestures/Explain_3',
'No_1': 'animations/Stand/Gestures/No_1',
'Explain_6': 'animations/Stand/Gestures/Explain_6',
'Caress_1': 'animations/Stand/Gestures/Caress_1',
'OnTheEvening_4': 'animations/Stand/Gestures/OnTheEvening_4',
'OnTheEvening_2': 'animations/Stand/Gestures/OnTheEvening_2',
'Hey_1': 'animations/Stand/Gestures/Hey_1',
'Wings_2': 'animations/Stand/Gestures/Wings_2',
'CalmDown_2': 'animations/Stand/Gestures/CalmDown_2',
'IDontKnow_5': 'animations/Stand/Gestures/IDontKnow_5',
'This_12': 'animations/Stand/Gestures/This_12',
'Wings_5': 'animations/Stand/Gestures/Wings_5',
'This_4': 'animations/Stand/Gestures/This_4',
'This_2': 'animations/Stand/Gestures/This_2',
'You_5': 'animations/Stand/Gestures/You_5',
'ShowFloor_2': 'animations/Stand/Gestures/ShowFloor_2',
'This_5': 'animations/Stand/Gestures/This_5',
'CalmDown_5': 'animations/Stand/Gestures/CalmDown_5',
'Reject_1': 'animations/Stand/Gestures/Reject_1',
'ShowSky_7': 'animations/Stand/Gestures/ShowSky_7',
'Confused_1': 'animations/Stand/Gestures/Confused_1',
'IDontKnow_2': 'animations/Stand/Gestures/IDontKnow_2',
'Shy_1': 'animations/Stand/Gestures/Shy_1',
'WhatSThis_4': 'animations/Stand/Gestures/WhatSThis_4',
'Mime_2': 'animations/Stand/Gestures/Mime_2',
'OnTheEvening_5': 'animations/Stand/Gestures/OnTheEvening_5',
'WhatSThis_3': 'animations/Stand/Gestures/WhatSThis_3',
'This_13': 'animations/Stand/Gestures/This_13',
'Enthusiastic_5': 'animations/Stand/Gestures/Enthusiastic_5',
'Hey_5': 'animations/Stand/Gestures/Hey_5',
'Yes_3': 'animations/Stand/Gestures/Yes_3',
'CalmDown_4': 'animations/Stand/Gestures/CalmDown_4',
'CatchFly_1': 'animations/Stand/Gestures/CatchFly_1',
'WhatSThis_2': 'animations/Stand/Gestures/WhatSThis_2',
'Angry_2': 'animations/Stand/Gestures/Angry_2',
'CountFour_2': 'animations/Stand/Gestures/CountFour_2',
'YouKnowWhat_5': 'animations/Stand/Gestures/YouKnowWhat_5',
'Explain_1': 'animations/Stand/Gestures/Explain_1',
'No_3': 'animations/Stand/Gestures/No_3',
'This_3': 'animations/Stand/Gestures/This_3',
'Hey_6': 'animations/Stand/Gestures/Hey_6',
'Give_1': 'animations/Stand/Gestures/Give_1',
'Joy_1': 'animations/Stand/Gestures/Joy_1',
'ShowFloor_3': 'animations/Stand/Gestures/ShowFloor_3',
'CalmDown_1': 'animations/Stand/Gestures/CalmDown_1',
'Follow_1': 'animations/Stand/Gestures/Follow_1',
'Explain_7': 'animations/Stand/Gestures/Explain_7',
'Hey_2': 'animations/Stand/Gestures/Hey_2',
'Me_6': 'animations/Stand/Gestures/Me_6',
'You_1': 'animations/Stand/Gestures/You_1',
'Excited_1': 'animations/Stand/Gestures/Excited_1',
'ShowSky_9': 'animations/Stand/Gestures/ShowSky_9',
'ShowFloor_4': 'animations/Stand/Gestures/ShowFloor_4',
'JointHands_2': 'animations/Stand/Gestures/JointHands_2',
'ShowSky_5': 'animations/Stand/Gestures/ShowSky_5',
'CountMore_1': 'animations/Stand/Gestures/CountMore_1',
'Give_2': 'animations/Stand/Gestures/Give_2',
'WhatSThis_11': 'animations/Stand/Gestures/WhatSThis_11',
'Choice_1': 'animations/Stand/Gestures/Choice_1',
'Thinking_4': 'animations/Stand/Gestures/Thinking_4',
'You_2': 'animations/Stand/Gestures/You_2',
'Everything_6': 'animations/Stand/Gestures/Everything_6',
'Enthusiastic_2': 'animations/Stand/Gestures/Enthusiastic_2',
'WhatSThis_5': 'animations/Stand/Gestures/WhatSThis_5',
'Enthusiastic_4': 'animations/Stand/Gestures/Enthusiastic_4',
'Salute_1': 'animations/Stand/Gestures/Salute_1',
'HeSays_2': 'animations/Stand/Gestures/HeSays_2',
'WhatSThis_7': 'animations/Stand/Gestures/WhatSThis_7',
'No_9': 'animations/Stand/Gestures/No_9',
'Freeze_1': 'animations/Stand/Gestures/Freeze_1',
'Reject_3': 'animations/Stand/Gestures/Reject_3',
'Reject_4': 'animations/Stand/Gestures/Reject_4',
'WhatSThis_9': 'animations/Stand/Gestures/WhatSThis_9',
'Give_6': 'animations/Stand/Gestures/Give_6',
'This_8': 'animations/Stand/Gestures/This_8',
'WhatSThis_1': 'animations/Stand/Gestures/WhatSThis_1',
'CalmDown_3': 'animations/Stand/Gestures/CalmDown_3',
'Give_5': 'animations/Stand/Gestures/Give_5',
'Stretch_2': 'animations/Stand/Gestures/Stretch_2',
'ShowSky_4': 'animations/Stand/Gestures/ShowSky_4',
'Nothing_1': 'animations/Stand/Gestures/Nothing_1',
'Explain_2': 'animations/Stand/Gestures/Explain_2',
'CountThree_1': 'animations/Stand/Gestures/CountThree_1',
'WhatSThis_12': 'animations/Stand/Gestures/WhatSThis_12',
'Look_1': 'animations/Stand/Gestures/Look_1',
'CountFour_1': 'animations/Stand/Gestures/CountFour_1',
'HeSays_1': 'animations/Stand/Gestures/HeSays_1',
'Me_5': 'animations/Stand/Gestures/Me_5',
'BowShort_1': 'animations/Stand/Gestures/BowShort_1',
'You_3': 'animations/Stand/Gestures/You_3',
'CountFive_2': 'animations/Stand/Gestures/CountFive_2',
'CountMore_2': 'animations/Stand/Gestures/CountMore_2',
'This_14': 'animations/Stand/Gestures/This_14',
'Choice_2': 'animations/Stand/Gestures/Choice_2',
'Nothing_2': 'animations/Stand/Gestures/Nothing_2',
'Applause_1': 'animations/Stand/Gestures/Applause_1',
'Me_4': 'animations/Stand/Gestures/Me_4',
'Please_2': 'animations/Stand/Gestures/Please_2',
'You_4': 'animations/Stand/Gestures/You_4',
'No_7': 'animations/Stand/Gestures/No_7',
'Thinking_1': 'animations/Stand/Gestures/Thinking_1',
'Everything_1': 'animations/Stand/Gestures/Everything_1',
'HeSays_3': 'animations/Stand/Gestures/HeSays_3',
'WhatSThis_8': 'animations/Stand/Gestures/WhatSThis_8',
'YouKnowWhat_2': 'animations/Stand/Gestures/YouKnowWhat_2',
'ShowSky_6': 'animations/Stand/Gestures/ShowSky_6',
'Confused_2': 'animations/Stand/Gestures/Confused_2',
'No_4': 'animations/Stand/Gestures/No_4',
'This_10': 'animations/Stand/Gestures/This_10',
'YouKnowWhat_3': 'animations/Stand/Gestures/YouKnowWhat_3',
'No_8': 'animations/Stand/Gestures/No_8',
'WhatSThis_10': 'animations/Stand/Gestures/WhatSThis_10',
'ShowFloor_5': 'animations/Stand/Gestures/ShowFloor_5',
'Claw_1': 'animations/Stand/Gestures/Claw_1',
'Everything_5': 'animations/Stand/Gestures/Everything_5',
'No_6': 'animations/Stand/Gestures/No_6',
'ShowSky_11': 'animations/Stand/Gestures/ShowSky_11',
'CountOne_2': 'animations/Stand/Gestures/CountOne_2',
'WhatSThis_13': 'animations/Stand/Gestures/WhatSThis_13',
'JointHands_1': 'animations/Stand/Gestures/JointHands_1',
'OnTheEvening_3': 'animations/Stand/Gestures/OnTheEvening_3',
'ComeOn_1': 'animations/Stand/Gestures/ComeOn_1',
'Great_1': 'animations/Stand/Gestures/Great_1',
'ShowSky_1': 'animations/Stand/Gestures/ShowSky_1',
'Coaxing_2': 'animations/Stand/Gestures/Coaxing_2',
'WhatSThis_16': 'animations/Stand/Gestures/WhatSThis_16',
'Reject_2': 'animations/Stand/Gestures/Reject_2',
'This_11': 'animations/Stand/Gestures/This_11',
'CountTwo_2': 'animations/Stand/Gestures/CountTwo_2',
'Explain_5': 'animations/Stand/Gestures/Explain_5',
'Reject_6': 'animations/Stand/Gestures/Reject_6',
'YouKnowWhat_4': 'animations/Stand/Gestures/YouKnowWhat_4',
'Shoot_1': 'animations/Stand/Gestures/Shoot_1',
'IDontKnow_4': 'animations/Stand/Gestures/IDontKnow_4',
'Everything_2': 'animations/Stand/Gestures/Everything_2',
'Everything_3': 'animations/Stand/Gestures/Everything_3',
'IDontKnow_3': 'animations/Stand/Gestures/IDontKnow_3',
'IDontKnow_1': 'animations/Stand/Gestures/IDontKnow_1',
'CountThree_2': 'animations/Stand/Gestures/CountThree_2',
'Me_3': 'animations/Stand/Gestures/Me_3',
'Desperate_5': 'animations/Stand/Gestures/Desperate_5',
'Look_2': 'animations/Stand/Gestures/Look_2',
'ShowSky_10': 'animations/Stand/Gestures/ShowSky_10',
'Salute_2': 'animations/Stand/Gestures/Salute_2',
'Desperate_1': 'animations/Stand/Gestures/Desperate_1',
'YouKnowWhat_6': 'animations/Stand/Gestures/YouKnowWhat_6',
'Angry_1': 'animations/Stand/Gestures/Angry_1',
'ShowFloor_1': 'animations/Stand/Gestures/ShowFloor_1',
'Hey_4': 'animations/Stand/Gestures/Hey_4',
'Desperate_3': 'animations/Stand/Gestures/Desperate_3',
'Listening_2': 'animations/Sit/BodyTalk/Listening/Listening_2',
'Listening_3': 'animations/Sit/BodyTalk/Listening/Listening_3',
'Listening_4': 'animations/Sit/BodyTalk/Listening/Listening_4',
'Listening_1': 'animations/Sit/BodyTalk/Listening/Listening_1',
'Remember_3': 'animations/Sit/BodyTalk/Thinking/Remember_3',
'ThinkingLoop_2': 'animations/Sit/BodyTalk/Thinking/ThinkingLoop_2',
'Remember_2': 'animations/Sit/BodyTalk/Thinking/Remember_2',
'Remember_1': 'animations/Sit/BodyTalk/Thinking/Remember_1',
'ThinkingLoop_1': 'animations/Sit/BodyTalk/Thinking/ThinkingLoop_1',
'BodyTalk_12': 'animations/Sit/BodyTalk/Speaking/BodyTalk_12',
'BodyTalk_4': 'animations/Sit/BodyTalk/Speaking/BodyTalk_4',
'BodyTalk_9': 'animations/Sit/BodyTalk/Speaking/BodyTalk_9',
'BodyTalk_10': 'animations/Sit/BodyTalk/Speaking/BodyTalk_10',
'BodyTalk_6': 'animations/Sit/BodyTalk/Speaking/BodyTalk_6',
'BodyTalk_5': 'animations/Sit/BodyTalk/Speaking/BodyTalk_5',
'BodyTalk_7': 'animations/Sit/BodyTalk/Speaking/BodyTalk_7',
'BodyTalk_11': 'animations/Sit/BodyTalk/Speaking/BodyTalk_11',
'BodyTalk_1': 'animations/Sit/BodyTalk/Speaking/BodyTalk_1',
'BodyTalk_8': 'animations/Sit/BodyTalk/Speaking/BodyTalk_8',
'BodyTalk_2': 'animations/Sit/BodyTalk/Speaking/BodyTalk_2',
'BodyTalk_3': 'animations/Sit/BodyTalk/Speaking/BodyTalk_3',
'LightShine_2': 'animations/Sit/Reactions/LightShine_2',
'TouchHead_3': 'animations/Sit/Reactions/TouchHead_3',
'BumperRight_1': 'animations/Sit/Reactions/BumperRight_1',
'TouchHead_2': 'animations/Sit/Reactions/TouchHead_2',
'EthernetOff_1': 'animations/Sit/Reactions/EthernetOff_1',
'LightShine_3': 'animations/Sit/Reactions/LightShine_3',
'LightShine_1': 'animations/Sit/Reactions/LightShine_1',
'SeeColor_1': 'animations/Sit/Reactions/SeeColor_1',
'BumperLeft_1': 'animations/Sit/Reactions/BumperLeft_1',
'TouchHead_1': 'animations/Sit/Reactions/TouchHead_1',
'Bumpers_1': 'animations/Sit/Reactions/Bumpers_1',
'ShakeBody_3': 'animations/Sit/Reactions/ShakeBody_3',
'EthernetOn_1': 'animations/Sit/Reactions/EthernetOn_1',
'SeeColor_2': 'animations/Sit/Reactions/SeeColor_2',
'ShakeBody_2': 'animations/Sit/Reactions/ShakeBody_2',
'SeeColor_3': 'animations/Sit/Reactions/SeeColor_3',
'Bumpers_3': 'animations/Sit/Reactions/Bumpers_3',
'LightShine_4': 'animations/Sit/Reactions/LightShine_4',
'ShakeBody_1': 'animations/Sit/Reactions/ShakeBody_1',
'Heat_1': 'animations/Sit/Reactions/Heat_1',
'Bumpers_2': 'animations/Sit/Reactions/Bumpers_2',
'TouchHead_4': 'animations/Sit/Reactions/TouchHead_4',
'Late_1': 'animations/Sit/Emotions/Negative/Late_1',
'Surprise_1': 'animations/Sit/Emotions/Negative/Surprise_1',
'Sad_1': 'animations/Sit/Emotions/Negative/Sad_1',
'Fear_1': 'animations/Sit/Emotions/Negative/Fear_1',
'Hurt_1': 'animations/Sit/Emotions/Negative/Hurt_1',
'Frustrated_1': 'animations/Sit/Emotions/Negative/Frustrated_1',
'Angry_1': 'animations/Sit/Emotions/Negative/Angry_1',
'Hungry_1': 'animations/Sit/Emotions/Positive/Hungry_1',
'Happy_4': 'animations/Sit/Emotions/Positive/Happy_4',
'Laugh_2': 'animations/Sit/Emotions/Positive/Laugh_2',
'Mocker_1': 'animations/Sit/Emotions/Positive/Mocker_1',
'Happy_1': 'animations/Sit/Emotions/Positive/Happy_1',
'Shy_1': 'animations/Sit/Emotions/Positive/Shy_1',
'Laugh_1': 'animations/Sit/Emotions/Positive/Laugh_1',
'Happy_2': 'animations/Sit/Emotions/Positive/Happy_2',
'Happy_3': 'animations/Sit/Emotions/Positive/Happy_3',
'Winner_1': 'animations/Sit/Emotions/Positive/Winner_1',
'AskForAttention_3': 'animations/Sit/Emotions/Neutral/AskForAttention_3',
'AskForAttention_1': 'animations/Sit/Emotions/Neutral/AskForAttention_1',
'Sneeze_1': 'animations/Sit/Emotions/Neutral/Sneeze_1',
'AskForAttention_2': 'animations/Sit/Emotions/Neutral/AskForAttention_2',
'GeoTriangle_1': 'animations/Sit/Waiting/GeoTriangle_1',
'Relaxation_3': 'animations/Sit/Waiting/Relaxation_3',
'ScratchTorso_1': 'animations/Sit/Waiting/ScratchTorso_1',
'LookHand_1': 'animations/Sit/Waiting/LookHand_1',
'Yawn_1': 'animations/Sit/Waiting/Yawn_1',
'CallSomeone_1': 'animations/Sit/Waiting/CallSomeone_1',
'FalseStop_1': 'animations/Sit/Waiting/FalseStop_1',
'WakeUp_1': 'animations/Sit/Waiting/WakeUp_1',
'Relaxation_2': 'animations/Sit/Waiting/Relaxation_2',
'KnockKnee_1': 'animations/Sit/Waiting/KnockKnee_1',
'Puppet_1': 'animations/Sit/Waiting/Puppet_1',
'Binoculars_1': 'animations/Sit/Waiting/Binoculars_1',
'ScratchBack_1': 'animations/Sit/Waiting/ScratchBack_1',
'TakePicture_1': 'animations/Sit/Waiting/TakePicture_1',
'Bored_1': 'animations/Sit/Waiting/Bored_1',
'GeoCircle_1': 'animations/Sit/Waiting/GeoCircle_1',
'FalseStop_2': 'animations/Sit/Waiting/FalseStop_2',
'DriveCar_1': 'animations/Sit/Waiting/DriveCar_1',
'Music_HighwayToHell_1': 'animations/Sit/Waiting/Music_HighwayToHell_1',
'LookHand_2': 'animations/Sit/Waiting/LookHand_2',
'Think_1': 'animations/Sit/Waiting/Think_1',
'GeoSquare_1': 'animations/Sit/Waiting/GeoSquare_1',
'MysticalPower_1': 'animations/Sit/Waiting/MysticalPower_1',
'ScratchHand_1': 'animations/Sit/Waiting/ScratchHand_1',
'Fitness_1': 'animations/Sit/Waiting/Fitness_1',
'Think_3': 'animations/Sit/Waiting/Think_3',
'Think_2': 'animations/Sit/Waiting/Think_2',
'CatchFly_1': 'animations/Sit/Waiting/CatchFly_1',
'Pong_1': 'animations/Sit/Waiting/Pong_1',
'Oar_1': 'animations/Sit/Waiting/Oar_1',
'KnockEye_1': 'animations/Sit/Waiting/KnockEye_1',
'Music_VieEnRose_1': 'animations/Sit/Waiting/Music_VieEnRose_1',
'ScratchHead_1': 'animations/Sit/Waiting/ScratchHead_1',
'Relaxation_1': 'animations/Sit/Waiting/Relaxation_1',
'ZenCircles_1': 'animations/Sit/Waiting/ZenCircles_1',
'Phone_1': 'animations/Sit/Waiting/Phone_1',
'ScratchEye_1': 'animations/Sit/Waiting/ScratchEye_1',
'Robot_1': 'animations/Sit/Waiting/Robot_1',
'ScratchLeg_1': 'animations/Sit/Waiting/ScratchLeg_1',
'PlayHands_1': 'animations/Sit/Waiting/PlayHands_1',
'KnockKnee_2': 'animations/Sit/Waiting/KnockKnee_2',
'AutoFormat_1': 'animations/Sit/Waiting/AutoFormat_1',
'PlayHands_3': 'animations/Sit/Waiting/PlayHands_3',
'PlayHands_2': 'animations/Sit/Waiting/PlayHands_2',
'PoorlySeated_1': 'animations/Sit/Waiting/PoorlySeated_1',
'Cramp_1': 'animations/Sit/Waiting/Cramp_1',
'Rest_1': 'animations/Sit/Waiting/Rest_1',
'Me_7': 'animations/Sit/Gestures/Me_7',
'Hey_3': 'animations/Sit/Gestures/Hey_3',
'You_4': 'animations/Sit/Gestures/You_4',
'ComeOn_1': 'animations/Sit/Gestures/ComeOn_1',
'CircleEyes': 'animations/LED/CircleEyes'}