from fluentJoints import FluentJoints
class FluentElbows():

    # init method
    def __init__(self, fluentMotion, wrists, hands):
        
        self.wrists = wrists
        self.hands = hands
        
        # jobs for threading
        self.fluentMotion = fluentMotion
        self.joints = fluentMotion.joints
        self.chains = fluentMotion.chains
        self.log = fluentMotion.log

    def go(self):
        self.fluentMotion.go()
        
    ###################################
    # Bent
    ###################################
    def bent(self, duration=0):
        self.rBent(duration)
        self.lBent(duration)
        return self;

    def rBent(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowRoll, 89, duration)
        return self;


    def lBent(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowRoll, -89, duration)
        return self;

    ###################################
    # Straight
    ###################################
    def straight(self, duration=0):
        self.rStraight(duration)
        self.lStraight(duration)
        return self;

    def rStraight(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowRoll, 0.5, duration)
        return self;


    def lStraight(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowRoll, 0.5, duration)
        return self;


    ###################################
    # Up
    ###################################
    def turnUp(self, duration=0):
        self.rTurnUp(duration)
        self.lTurnUp(duration)
        return self;

    def rTurnUp(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowYaw, 90, duration)
        return self;


    def lTurnUp(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowYaw, -90, duration)
        return self;

    ###################################
    # Turn Down
    ###################################
    def turnDown(self, duration=0):
        self.rTurnDown(duration)
        self.lTurnDown(duration)
        return self;

    def rTurnDown(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowYaw, -90, duration)
        return self;


    def lTurnDown(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowYaw, 90, duration)
        return self;


    ###################################
    # In
    ###################################
    def turnIn(self, duration=0):
        self.rTurnIn(duration)
        self.lTurnIn(duration)
        return self;

    def rTurnIn(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowYaw, 0, duration)
        return self;

    def lTurnIn(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowYaw, 0, duration)
        return self;