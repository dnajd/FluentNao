import math
from fluentJoints import FluentJoints

class FluentWrists():

    # init method
    def __init__(self, fluentMotion, joints, chains, log):
        
        # jobs for threading
        self.fluentMotion = fluentMotion
        self.joints = joints
        self.chains = chains
        self.log = log

    ###################################
    # Center
    ###################################
    def center(self, duration = 1):     
        self.lCenter(duration)
        self.rCenter(duration)
        return self.fluentMotion;

    def lCenter(self, duration = 1):     
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LWristYaw, 0.0, duration)
        return self.fluentMotion;
        
    def rCenter(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RWristYaw, 0.0, duration)
        return self.fluentMotion;

    ###################################
    # Out
    ###################################
    def turnOut(self, duration = 1):     
        self.lTurnOut(duration)
        self.rTurnOut(duration)
        return self.fluentMotion;

    def lTurnOut(self, duration = 1):     
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LWristYaw, 90, duration)
        return self.fluentMotion;
        
    def rTurnOut(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RWristYaw, -90, duration)
        return self.fluentMotion;

    ###################################
    # In
    ###################################
    def turnIn(self, duration = 1):     
        self.lTurnIn(duration)
        self.rTurnIn(duration)
        return self.fluentMotion;

    def lTurnIn(self, duration = 1):     
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LWristYaw, -90, duration)
        return self.fluentMotion;
        
    def rTurnIn(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RWristYaw, 90, duration)
        return self.fluentMotion;