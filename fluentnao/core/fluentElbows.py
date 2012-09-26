from fluentJoints import FluentJoints
class FluentElbows():

    # init method
    def __init__(self, fluentNao, wrists, hands):
        
        self.wrists = wrists
        self.hands = hands
        
        # jobs for threading
        self.fluentNao = fluentNao
        self.joints = fluentNao.joints
        self.chains = fluentNao.chains
        self.log = fluentNao.log

    def go(self):
        self.fluentNao.go()
        
    ###################################
    # Bent
    ###################################
    def bent(self, duration=0, offset=0):
        self.rBent(duration, offset)
        self.lBent(duration, offset)
        return self;

    def rBent(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)  
        angle = 89 + offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.RArm.RElbowRoll, angle, duration)
        return self;


    def lBent(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)  
        angle = -89 - offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.LArm.LElbowRoll, angle, duration)
        return self;

    ###################################
    # Straight
    ###################################
    def straight(self, duration=0, offset=0):
        self.rStraight(duration, offset)
        self.lStraight(duration, offset)
        return self;

    def rStraight(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)  
        angle = 0.5 - offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.RArm.RElbowRoll, angle, duration)
        return self;


    def lStraight(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)  
        angle = 0.5 + offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.LArm.LElbowRoll, angle, duration)
        return self;


    ###################################
    # Up
    ###################################
    def turnUp(self, duration=0, offset=0):
        self.rTurnUp(duration, offset)
        self.lTurnUp(duration, offset)
        return self;

    def rTurnUp(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration) 
        angle = 90 + offset 
        self.fluentNao.moveWithDegreesAndDuration(self.joints.RArm.RElbowYaw, angle, duration)
        return self;


    def lTurnUp(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)  
        angle = -90 - offset 
        self.fluentNao.moveWithDegreesAndDuration(self.joints.LArm.LElbowYaw, angle, duration)
        return self;

    ###################################
    # Turn Down
    ###################################
    def turnDown(self, duration=0, offset=0):
        self.rTurnDown(duration, offset)
        self.lTurnDown(duration, offset)
        return self;

    def rTurnDown(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)  
        angle = -90 - offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.RArm.RElbowYaw, angle, duration)
        return self;

    def lTurnDown(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)  
        angle = 90 + offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.LArm.LElbowYaw, angle, duration)
        return self;


    ###################################
    # In
    ###################################
    def turnIn(self, duration=0, offset=0):
        self.rTurnIn(duration, offset)
        self.lTurnIn(duration, offset)
        return self;

    def rTurnIn(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)  
        angle = 0 - offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.RArm.RElbowYaw, angle, duration)
        return self;

    def lTurnIn(self, duration=0, offset=0):
        duration = self.fluentNao.determineDuration(duration)  
        angle = 0 + offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.LArm.LElbowYaw, angle, duration)
        return self;