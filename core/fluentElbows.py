from fluentJoints import FluentJoints
class FluentElbows():

    # init method
    def __init__(self, fluentMotion, joints, chains, log):
        
        # jobs for threading
        self.fluentMotion = fluentMotion
        self.joints = joints
        self.chains = chains
        self.log = log

    ###################################
    # Bent
    ###################################
    def bent(self, duration = 1):
        self.rBent(duration)
        self.lBent(duration)
        return self.fluentMotion

    def rBent(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowRoll, 89, duration)
        return self.fluentMotion


    def lBent(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowRoll, -89, duration)
        return self.fluentMotion

    ###################################
    # Straight
    ###################################
    def straight(self, duration = 1):
        self.rStraight(duration)
        self.lStraight(duration)
        return self.fluentMotion

    def rStraight(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RElbowRoll, 0.5, duration)
        return self.fluentMotion


    def lStraight(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LElbowRoll, 0.5, duration)
        return self.fluentMotion
