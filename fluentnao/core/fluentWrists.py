import math
from fluentJoints import FluentJoints

class FluentWrists():

    # init method
    def __init__(self, fluentNao, hands):
        
        self.hands = hands

        # jobs for threading
        self.fluentNao = fluentNao
        self.joints = fluentNao.joints
        self.chains = fluentNao.chains
        self.log = fluentNao.log

    def go(self):
        self.fluentNao.go()
        
    ###################################
    # Center
    ###################################
    def center(self, duration=0, offset=0):     
        self.lCenter(duration, offset)
        self.rCenter(duration, offset)
        return self;

    def lCenter(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)       
        angle = 0.0 + offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.LArm.LWristYaw, angle, duration)
        return self;
        
    def rCenter(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)  
        angle = 0.0 - offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.RArm.RWristYaw, angle, duration)
        return self;

    ###################################
    # Out
    ###################################
    def turnOut(self, duration=0, offset=0):     
        self.lTurnOut(duration, offset)
        self.rTurnOut(duration, offset)
        return self;

    def lTurnOut(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)       
        angle = 90 + offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.LArm.LWristYaw, angle, duration)
        return self;
        
    def rTurnOut(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)  
        angle = -90 - offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.RArm.RWristYaw, angle, duration)
        return self;

    ###################################
    # In
    ###################################
    def turnIn(self, duration=0, offset=0):     
        self.lTurnIn(duration, offset)
        self.rTurnIn(duration, offset)
        return self;

    def lTurnIn(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)      
        angle = -90 - offset   
        self.fluentNao.moveWithDegreesAndDuration(self.joints.LArm.LWristYaw, angle, duration)
        return self;
        
    def rTurnIn(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)   
        angle = 90 + offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.RArm.RWristYaw, angle, duration)
        return self;