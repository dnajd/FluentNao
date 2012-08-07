import almath
import math
from multiprocessing import Process
from fluentJoints import FluentJoints
from fluentArms import FluentArms
from fluentHands import FluentHands
from fluentElbows import FluentElbows
from fluentWrists import FluentWrists

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

        # arms & hands
        self.arms = FluentArms(self, self.joints, self.chains, log) 
        self.hands = FluentHands(self, self.joints, self.chains, log) 
        self.elbows = FluentElbows(self, self.joints, self.chains, log) 
        self.wrists = FluentWrists(self, self.joints, self.chains, log) 

    ###################################
    # wait for tasks to finish
    ###################################
    def go(self):
        for taskId in self.jobs:
            self.motionProxy.wait(taskId, 0)   
        return self         
            
    ###################################
    # move
    ###################################
    def move(self, chain, angleListInRadians, fractionMaxSpeed = 0.3):
        # motion w/ blocking call
        taskId = self.motionProxy.post.angleInterpolationWithSpeed(chain, angleListInRadians, fractionMaxSpeed)    

        # save task id
        self.jobs.append(taskId)
        self.log("setting " + chain + " to " + str(angleListInRadians))

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
        maxChange = limits[0][2]  #what does this mean: rad.s-1

        self.log("maxChange: " + str(maxChange) + " for " + jointName)
        return math.degrees(maxChange)

    def getFractionMaxSpeed(self, jointName, desiredPositionInDegrees, executionTimeInSeconds):
        # current position in degrees
        useSensors = False;
        currentPositionInDegrees = math.degrees(self.motionProxy.getAngles(jointName, useSensors)[0]);
        self.log("pos in deg: " + str(currentPositionInDegrees))

        # distance
        distanceInDegrees = abs(currentPositionInDegrees - desiredPositionInDegrees)
        self.log("distance: " + str(distanceInDegrees))

        # max speed
        maxDegreesPerSecond = self.getMaxDegreesPerSecond(jointName)

        # fractionOfMaxSpeed = (distanceInDegrees) / (maxDegreesPerSecond * executionTimeInSeconds)
        return (distanceInDegrees) / (maxDegreesPerSecond * executionTimeInSeconds)

    @staticmethod
    def initModulesForDevelopment(pathToCore):
        try:
            import fluentMotion
            import fluentArms
            import fluentJoints
            import fluentHands
            import fluentElbows
            import fluentWrists
        except:
            import sys
            sys.path.append(pathToCore)
            import fluentMotion
            import fluentArms
            import fluentJoints
            import fluentHands
            import fluentElbows
            import fluentWrists

        reload(fluentMotion)
        reload(fluentArms)
        reload(fluentJoints)
        reload(fluentHands)
        reload(fluentElbows)
        reload(fluentWrists)

    ###################################
    # Whole Body
    ###################################
    def zero(self):
        # MoveChain(chain, angle, speed)
        chain = self.chains.Body
        angleInDegrees = 0.0
        self.moveWithDegrees(chain, self.getTargetAnglesForChain(chain, angleInDegrees))
        return self;

    # example of chain
    #angleList = [0.0, -60, 0.0, 0.0, 0.0, 0.0]
    #self.moveWithDegrees(self.Chains.RArm, angleList, 0.3)