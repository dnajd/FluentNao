import almath
import math
from fluentJoints import FluentJoints
from fluentArms import FluentArms
from fluentHands import FluentHands
from fluentElbows import FluentElbows
from fluentWrists import FluentWrists
from fluentLegs import FluentLegs
from fluentHead import FluentHead
from fluentAnkle import FluentAnkle

class FluentMotion():

    # init method
    def __init__(self, alProxy, log):
        
        # jobs for threading
        self.jobs = []
        
        # set motion proxy & log
        #self.postureProxy = alProxy("ALRobotPosture")

        self.motionProxy = alProxy("ALMotion")
        self.textToSpeechProxy = alProxy("ALTextToSpeech")
        self.log = log

        # joints
        self.joints = FluentJoints()
        self.chains = self.joints.Chains

        # head
        self.head = FluentHead(self)
        
        # arms
        self.hands = FluentHands(self) 
        self.wrists = FluentWrists(self, self.hands) 
        self.elbows = FluentElbows(self, self.wrists, self.hands) 
        self.arms = FluentArms(self, self.elbows, self.wrists, self.hands) 
        
        # legs
        self.ankles = FluentAnkle(self)
        self.legs = FluentLegs(self, self.ankles)

        # global duration
        self.setDuration(1)

    ###################################
    # text to speech
    ###################################        
    def say(self, text):
        self.textToSpeechProxy.post.say(text)

    ###################################
    # Postures
    ###################################
    def standInit(self, duration=1):
        postureProxy.goToPosture("StandInit", duration)
    
    def sitRelax(self, duration=1):
        postureProxy.goToPosture("SitRelax", duration)
    
    def standZero(self, duration=1):
        postureProxy.goToPosture("StandZero", duration)
    
    def lyingBelly(self, duration=1):
        postureProxy.goToPosture("LyingBelly", duration)
    
    def lyingBack(self, duration=1):
        postureProxy.goToPosture("LyingBack", duration)
    
    def stand(self, duration=1):
        postureProxy.goToPosture("Stand", duration)
    
    def crouch(self, duration=1):
        postureProxy.goToPosture("Crouch", duration)
    
    def sit(self, duration=1):
        postureProxy.goToPosture("Sit", duration)


    ###################################
    # Motion
    ###################################
    def stiff(self):
        pNames = "Body"
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

    def relax(self):
        pNames = "Body"
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

    def wbDisable(self):
        isEnabled  = False
        self.motionProxy.wbEnable(isEnabled)

    def wbEndable(self):
        isEnabled  = True
        self.motionProxy.wbEnable(isEnabled)

    def fixLegs(self, supportLeg="Legs", stateName="Fixed"):
        # Legs are constrained fixed
        # supportLeg: Legs, LLeg or RLeg
        # stateName: Fixed, Plane or Free
        self.motionProxy.wbFootState(stateName, supportLeg)

    def constrainMotion(self, supportLeg="Legs"):
        # Constraint Balance Motion / Support Polygon
        # supportLeg: Legs, LLeg or RLeg
        isEnable   = True
        self.motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)

    def balance(self, leg, duration):

        duration = self.determineDuration(duration)  

        # stiffen body
        self.stiff()
        self.wbEndable()

        self.fixLegs()
        self.constrainMotion()

        # Com go to LLeg
        supportLeg = leg
        self.motionProxy.wbGoToBalance(supportLeg, duration)

        self.wbDisable()

    def setDuration(self, durationInSeconds):
        self.globalDuration = durationInSeconds
        return self;

    def determineDuration(self, durationInSeconds):
        if durationInSeconds > 0:
            return durationInSeconds

        return self.globalDuration

    ###################################
    # wait for tasks to finish
    ###################################
    
    def go(self):
        for taskId in self.jobs:
            #self.log("trying: %s" % (taskId))
            self.motionProxy.wait(taskId, 5000)   
            #self.log("released: %s" % (taskId))

        self.jobs[:] = []
        #self.log("done")
        
        return self         
            
    ###################################
    # move
    ###################################

    def zero(self):
        # MoveChain(chain, angle, speed)
        chain = self.chains.Body
        angleInDegrees = 0.0
        self.moveWithDegrees(chain, self.getTargetAnglesForChain(chain, angleInDegrees))
        return self;

    def move(self, chain, angleListInRadians, fractionMaxSpeed = 0.3):
        
        self.log("setting %s to %s" % (chain, angleListInRadians))

        # motion w/ blocking call
        taskId = self.motionProxy.post.angleInterpolationWithSpeed(chain, angleListInRadians, fractionMaxSpeed)    

        # save task id
        self.jobs.append(taskId)
        

    def moveWithDegrees(self, chain, angleListInDegrees, fractionMaxSpeed = 0.3):
        # convert to radians        
        angleListInRadians = [ x * almath.TO_RAD for x in angleListInDegrees]

        # move
        self.move(chain, angleListInRadians, fractionMaxSpeed)

    def moveWithDegreesAndDuration(self, jointName, angleInDegrees, durationInSeconds):
        # fraction of max speed
        fractionMaxSpeed = self.getFractionMaxSpeed(jointName, angleInDegrees, durationInSeconds)

        # convert to radians
        angleInRadians = angleInDegrees * almath.TO_RAD

        # move
        self.move(jointName, [angleInRadians], fractionMaxSpeed)

    ###################################
    # helpers
    ###################################

    def getTargetAnglesForChain(self, chain, angle):
        # Get the Number of Joints
        numBodies = len(self.motionProxy.getJointNames(chain))
    
        # We prepare a collection of floats
        return [angle] * numBodies

    def getMaxDegreesPerSecond(self, jointName):
        limits = self.motionProxy.getLimits(jointName);
        minAngle = limits[0][0]
        maxAngle = limits[0][1]
        maxChange = limits[0][2]  # in rad.s-1

        #self.log("maxChange: " + str(maxChange) + " for " + jointName)
        return math.degrees(maxChange)

    def getFractionMaxSpeed(self, jointName, desiredPositionInDegrees, executionTimeInSeconds):
        # current position in degrees
        useSensors = False;
        currentPositionInDegrees = math.degrees(self.motionProxy.getAngles(jointName, useSensors)[0]);
        #self.log("pos in deg: " + str(currentPositionInDegrees))

        # distance
        distanceInDegrees = abs(currentPositionInDegrees - desiredPositionInDegrees)
        #self.log("distance: " + str(distanceInDegrees))

        # max speed
        maxDegreesPerSecond = self.getMaxDegreesPerSecond(jointName)

        # fractionOfMaxSpeed = (distanceInDegrees) / (maxDegreesPerSecond * executionTimeInSeconds)
        fractionOfMaxSpeed = (distanceInDegrees) / (maxDegreesPerSecond * executionTimeInSeconds)

        if fractionOfMaxSpeed > maxDegreesPerSecond:
            return maxDegreesPerSecond
        return fractionOfMaxSpeed

    @staticmethod
    def initModulesForDevelopment(pathToCore):
        try:
            import fluentMotion
            import fluentArms
            import fluentJoints
            import fluentHands
            import fluentElbows
            import fluentWrists
            import fluentLegs
            import fluentHead
            import fluentAnkle
        except:
            import sys
            sys.path.append(pathToCore)
            import fluentMotion
            import fluentArms
            import fluentJoints
            import fluentHands
            import fluentElbows
            import fluentWrists
            import fluentLegs
            import fluentHead
            import fluentAnkle

        reload(fluentMotion)
        reload(fluentArms)
        reload(fluentJoints)
        reload(fluentHands)
        reload(fluentElbows)
        reload(fluentWrists)
        reload(fluentLegs)
        reload(fluentHead)
        reload(fluentAnkle)

    # example of chain
    #angleList = [0.0, -60, 0.0, 0.0, 0.0, 0.0]
    #self.moveWithDegrees(self.Chains.RArm, angleList, 0.3)