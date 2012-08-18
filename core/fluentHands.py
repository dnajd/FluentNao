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
    def open(self, duration=0):     
        self.lOpen(duration)
        self.rOpen(duration)
        return self;

    def lOpen(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)       
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LHand, math.degrees(1.0), duration)
        return self;
        
    def rOpen(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RHand, math.degrees(1.0), duration)
        return self;

    ###################################
    # Hands Close
    ###################################
    def close(self, duration=0):     
        self.lClose(duration)
        self.rClose(duration)
        return self;

    def lClose(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)       
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LHand, math.degrees(0.0), duration)
        return self;
        
    def rClose(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RHand, math.degrees(0.0), duration)
        return self;
