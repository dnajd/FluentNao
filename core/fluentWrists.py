import math
from fluentJoints import FluentJoints

class FluentWrists():

    # init method
    def __init__(self, fluentMotion, hands):
        
        self.hands = hands

        # jobs for threading
        self.fluentMotion = fluentMotion
        self.joints = fluentMotion.joints
        self.chains = fluentMotion.chains
        self.log = fluentMotion.log

    ###################################
    # Center
    ###################################
    def center(self, duration=0):     
        self.lCenter(duration)
        self.rCenter(duration)
        return self;

    def lCenter(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)       
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LWristYaw, 0.0, duration)
        return self;
        
    def rCenter(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RWristYaw, 0.0, duration)
        return self;

    ###################################
    # Out
    ###################################
    def turnOut(self, duration=0):     
        self.lTurnOut(duration)
        self.rTurnOut(duration)
        return self;

    def lTurnOut(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)       
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LWristYaw, 90, duration)
        return self;
        
    def rTurnOut(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RWristYaw, -90, duration)
        return self;

    ###################################
    # In
    ###################################
    def turnIn(self, duration=0):     
        self.lTurnIn(duration)
        self.rTurnIn(duration)
        return self;

    def lTurnIn(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)       
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LWristYaw, -90, duration)
        return self;
        
    def rTurnIn(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RWristYaw, 90, duration)
        return self;