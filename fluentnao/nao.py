from fluentnao.core.arms import Arms
from fluentnao.core.elbows import Elbows
from fluentnao.core.feet import Feet
from fluentnao.core.hands import Hands
from fluentnao.core.head import Head
from fluentnao.core.joints import Joints
from fluentnao.core.legs import Legs
from fluentnao.core.wrists import Wrists
from fluentnao.core.leds import Leds
from fluentnao.memory.eventModule import EventModule
from fluentnao.memory.sense import Sense
import almath
import math
import time

class Nao():

    # init method
    def __init__(self, alProxy, log):
        
        # jobs for threading
        self.jobs = []
        
        # set motion proxy & log
        self.postureProxy = alProxy("ALRobotPosture")
        
        self.ledsProxy = alProxy("ALLeds");
        self.motionProxy = alProxy("ALMotion")
        self.textToSpeechProxy = alProxy("ALTextToSpeech")
        self.log = log

        # joints
        self.joints = Joints()
        self.chains = self.joints.Chains

        # leds
        self.leds = Leds(self)

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

        self.sense = Sense(self)

        # global duration
        self.set_duration(2)

    ###################################
    # text to speech
    ###################################        
    def say(self, text):
        self.textToSpeechProxy.post.say(text)
        return self;

    def wait(self, seconds):
        time.sleep(seconds)
        return self;


    ###################################
    # Postures
    ###################################
    def stand_init(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("StandInit", speed))
        taskId = self.postureProxy.post.goToPosture("StandInit", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def sit_relax(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("SitRelax", speed))
        taskId = self.postureProxy.post.goToPosture("SitRelax", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def stand_zero(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("StandZero", speed))
        taskId = self.postureProxy.post.goToPosture("StandZero", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def lying_belly(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("LyingBelly", speed))
        taskId = self.postureProxy.post.goToPosture("LyingBelly", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def lying_back(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("LyingBack", speed))
        taskId = self.postureProxy.post.goToPosture("LyingBack", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def stand(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("Stand", speed))
        self.postureProxy.goToPosture("Stand", speed)
        self.motionProxy.waitUntilMoveIsFinished();
        return self;
    
    def crouch(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("Crouch", speed))
        taskId = self.postureProxy.post.goToPosture("Crouch", speed)
        self.jobs.append(taskId)
        self.go()
        return self;
    
    def sit(self, speed=.5):
        self.log("goToPosture=%s|speed=%s" % ("Sit", speed))
        self.postureProxy.post.goToPosture("Sit", speed)
        self.motionProxy.waitUntilMoveIsFinished();
        return self;


    ###################################
    # stiffness
    ###################################
    def stiff(self):
        pNames = self.joints.Chains.Body
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

    def relax(self):
        pNames = self.joints.Chains.Body
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

    ###################################
    # Whole Body Motion & Balance
    ###################################
    def whole_body_disable(self):
        self.log("wbDisable")
        isEnabled  = False
        self.motionProxy.wbEnable(isEnabled)

    def whole_body_endable(self):
        self.log("wbEnable")
        isEnabled  = True
        self.motionProxy.wbEnable(isEnabled)

    def foot_state(self, supportLeg="Legs", stateName="Fixed"):
        # Legs are constrained fixed
        # supportLeg: Legs, LLeg or RLeg
        # stateName: Fixed, Plane or Free
        self.log("supportLeg=%s|stateName=%s" % (supportLeg, stateName))
        self.motionProxy.wbFootState(stateName, supportLeg)

    def constrain_motion(self, supportLeg="Legs"):
        # Constraint Balance Motion / Support Polygon
        # supportLeg: Legs, LLeg or RLeg
        isEnable   = True
        self.motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)

    def balance(self, leg, duration):

        duration = self.determine_duration(duration)  

        # stiffen body
        self.stiff()
        self.whole_body_endable()

        self.foot_state()
        self.constrain_motion()

        # Com go to LLeg
        supportLeg = leg
        self.motionProxy.wbGoToBalance(supportLeg, duration)

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
            #self.log("trying: %s" % (taskId))
            self.motionProxy.wait(taskId, 15000)   
            #self.log("released: %s" % (taskId))

        self.jobs[:] = []
        #self.log("done")
        
        return self         
            
    ###################################
    # movement
    ###################################

    def zero(self):
        # MoveChain(chain, angle, speed)
        chain = self.chains.Body
        angleInDegrees = 0.0
        self.move_with_degrees(chain, self.get_target_angles_for_chain(chain, angleInDegrees))
        return self;

    def move(self, chain, angleListInRadians, fractionMaxSpeed = 0.3):
        
        self.log("setting %s to %s" % (chain, angleListInRadians))

        # motion w/ blocking call
        taskId = self.motionProxy.post.angleInterpolationWithSpeed(chain, angleListInRadians, fractionMaxSpeed)    

        # save task id
        self.jobs.append(taskId)
        

    def move_with_degrees(self, chain, angleListInDegrees, fractionMaxSpeed = 0.3):
        # convert to radians        
        angleListInRadians = [ x * almath.TO_RAD for x in angleListInDegrees]

        # move
        self.move(chain, angleListInRadians, fractionMaxSpeed)

    def move_with_degrees_and_duration(self, jointName, angleInDegrees, durationInSeconds):
        # fraction of max speed
        fractionMaxSpeed = self.get_fraction_max_speed(jointName, angleInDegrees, durationInSeconds)

        # convert to radians
        angleInRadians = angleInDegrees * almath.TO_RAD

        # move
        self.move(jointName, [angleInRadians], fractionMaxSpeed)

    ###################################
    # helpers
    ###################################

    def get_target_angles_for_chain(self, chain, angle):
        # Get the Number of Joints
        numBodies = len(self.motionProxy.getJointNames(chain))
    
        # We prepare a collection of floats
        return [angle] * numBodies

    def get_max_degrees_per_second(self, jointName):
        limits = self.motionProxy.getLimits(jointName);
        minAngle = limits[0][0]
        maxAngle = limits[0][1]
        maxChange = limits[0][2]  # in rad.s-1

        #self.log("maxChange: " + str(maxChange) + " for " + jointName)
        return math.degrees(maxChange)

    def get_fraction_max_speed(self, jointName, desiredPositionInDegrees, executionTimeInSeconds):
        # current position in degrees
        useSensors = False;
        currentPositionInDegrees = math.degrees(self.motionProxy.getAngles(jointName, useSensors)[0]);
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
    import fluentnao.memory.eventModule
    import fluentnao.memory.sense

    reload(fluentnao.core.arms)
    reload(fluentnao.core.joints)
    reload(fluentnao.core.hands)
    reload(fluentnao.core.elbows)
    reload(fluentnao.core.wrists)
    reload(fluentnao.core.legs)
    reload(fluentnao.core.head)
    reload(fluentnao.core.feet)
    reload(fluentnao.core.leds)
    reload(fluentnao.memory.eventModule)
    reload(fluentnao.memory.sense)