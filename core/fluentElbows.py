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

    ###################################
    # Bent
    ###################################
    def bent(self, duration=0):
        self.rBent(duration)
        self.lBent(duration)
        return self.fluentMotion

    def rBent(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowRoll, 89, duration)
        return self.fluentMotion


    def lBent(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowRoll, -89, duration)
        return self.fluentMotion

    ###################################
    # Straight
    ###################################
    def straight(self, duration=0):
        self.rStraight(duration)
        self.lStraight(duration)
        return self.fluentMotion

    def rStraight(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowRoll, 0.5, duration)
        return self.fluentMotion


    def lStraight(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowRoll, 0.5, duration)
        return self.fluentMotion


    ###################################
    # Up
    ###################################
    def turnUp(self, duration=0):
        self.rTurnUp(duration)
        self.lTurnUp(duration)
        return self.fluentMotion

    def rTurnUp(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowYaw, 90, duration)
        return self.fluentMotion


    def lTurnUp(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowYaw, -90, duration)
        return self.fluentMotion

    ###################################
    # Turn Down
    ###################################
    def turnDown(self, duration=0):
        self.rTurnDown(duration)
        self.lTurnDown(duration)
        return self.fluentMotion

    def rTurnDown(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowYaw, -90, duration)
        return self.fluentMotion


    def lTurnDown(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowYaw, 90, duration)
        return self.fluentMotion


    ###################################
    # In
    ###################################
    def turnIn(self, duration=0):
        self.rTurnIn(duration)
        self.lTurnIn(duration)
        return self.fluentMotion

    def rTurnIn(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowYaw, 0, duration)
        return self.fluentMotion

    def lTurnIn(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowYaw, 0, duration)
        return self.fluentMotion