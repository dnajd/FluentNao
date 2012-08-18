import math
from fluentJoints import FluentJoints
class FluentHands():

    # init method
    def __init__(self, fluentMotion):
        
        # jobs for threading
        self.fluentMotion = fluentMotion
        self.joints = fluentMotion.joints
        self.chains = fluentMotion.chains
        self.log = fluentMotion.log

    ###################################
    # Hands Open
    ###################################
    def open(self, duration = 1):     
        self.lOpen(duration)
        self.rOpen(duration)
        return self.fluentMotion;

    def lOpen(self, duration = 1):     
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LHand, math.degrees(1.0), duration)
        return self.fluentMotion;
        
    def rOpen(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RHand, math.degrees(1.0), duration)
        return self.fluentMotion;

    ###################################
    # Hands Close
    ###################################
    def close(self, duration = 1):     
        self.lClose(duration)
        self.rClose(duration)
        return self.fluentMotion;

    def lClose(self, duration = 1):     
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LHand, math.degrees(0.0), duration)
        return self.fluentMotion;
        
    def rClose(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RHand, math.degrees(0.0), duration)
        return self.fluentMotion;
