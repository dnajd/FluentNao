import almath
from multiprocessing import Process
from fluentJoints import FluentJoints
from fluentArms import FluentArms
from fluentHands import FluentHands

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
        self.arms = FluentArms(self, self.joints, self.chains, self.log) 
        self.hands = FluentHands(self, self.joints, self.chains, self.log) 


    ###################################
    # wait for tasks to finish
    ###################################
    def go(self):
        for taskId in self.jobs:
            self.motionProxy.wait(taskId, 0)   
        return self         
            
    ###################################
    # helpers
    ###################################
    def getTargetAnglesForChain(self, chain, angle):
        # Get the Number of Joints
        numBodies = len(self.motionProxy.getJointNames(chain))
    
        # We prepare a collection of floats
        return [angle] * numBodies
          
    def moveWithDegrees(self, chain, angleList, speed):
        # convert to radians        
        angleList = [ x * almath.TO_RAD for x in angleList]
        self.move(chain, angleList, speed)

    def move(self, chain, angleList, speed):
        
        # Ask motion to do this with a blocking call
        taskId = self.motionProxy.post.angleInterpolationWithSpeed(chain, angleList, speed)    
        self.jobs.append(taskId)
        self.log("setting " + chain + " to " + str(angleList))

    ###################################
    # Whole Body
    ###################################
    def zero(self):
        # MoveChain(chain, angle, speed)
        chain = self.chains.Body
        self.moveWithDegrees(chain, self.getTargetAnglesForChain(chain,0.0), 0.3)
        return self;

    # example of chain
    #angleList = [0.0, -60, 0.0, 0.0, 0.0, 0.0]
    #self.moveWithDegrees(self.Chains.RArm, angleList, 0.3)