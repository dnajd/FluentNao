import almath
import math
from fluentJoints import FluentJoints
from fluentArms import FluentArms
from fluentHands import FluentHands
from fluentElbows import FluentElbows
from fluentWrists import FluentWrists
from fluentLegs import FluentLegs

class FluentMotion():

    # init method
    def __init__(self, motionProxy, log):
        
        # jobs for threading
        self.jobs = []
        
        # set motion proxy & log
        self.motionProxy = motionProxy
        self.log = log

        # joints
        self.joints = FluentJoints()
        self.chains = self.joints.Chains

        # body parts
        self.hands = FluentHands(self) 
        self.wrists = FluentWrists(self, self.hands) 
        self.elbows = FluentElbows(self, self.wrists, self.hands) 
        self.arms = FluentArms(self, self.elbows, self.wrists, self.hands) 
        self.legs = FluentLegs(self)

        # global duration
        self.setDuration(1)

    ###################################
    # Motion
    ###################################
    def stiff(self):
        pNames = "Body"
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

    def wbDisable(self):
        isEnabled  = False
        self.motionProxy.wbEnable(isEnabled)

    def wbEndable(self):
        isEnabled  = True
        self.motionProxy.wbEnable(isEnabled)

    def zero(self):
        # MoveChain(chain, angle, speed)
        chain = self.chains.Body
        angleInDegrees = 0.0
        self.moveWithDegrees(chain, self.getTargetAnglesForChain(chain, angleInDegrees))
        return self;

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

    def move(self, chain, angleListInRadians, fractionMaxSpeed = 0.3):
        # motion w/ blocking call
        taskId = self.motionProxy.post.angleInterpolationWithSpeed(chain, angleListInRadians, fractionMaxSpeed)    

        # save task id
        self.jobs.append(taskId)
        #self.log("%s: %s" % (chain, taskId))
        self.log("setting %s to %s" % (chain, angleListInRadians))

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

        reload(fluentMotion)
        reload(fluentArms)
        reload(fluentJoints)
        reload(fluentHands)
        reload(fluentElbows)
        reload(fluentWrists)
        reload(fluentLegs)


    # example of chain
    #angleList = [0.0, -60, 0.0, 0.0, 0.0, 0.0]
    #self.moveWithDegrees(self.Chains.RArm, angleList, 0.3)