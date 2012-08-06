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
    def bent(self):
        self.rBent()
        self.lBent()
        return self.fluentMotion

    def rBent(self):
        self.fluentMotion.moveWithDegrees(self.joints.RArm.RElbowRoll, [89], 0.3)
        return self.fluentMotion


    def lBent(self):
        self.fluentMotion.moveWithDegrees(self.joints.LArm.LElbowRoll, [-89], 0.3)
        return self.fluentMotion

    ###################################
    # Straight
    ###################################
    def straight(self):
        self.rStraight()
        self.lStraight()
        return self.fluentMotion

    def rStraight(self):
        self.fluentMotion.moveWithDegrees(self.joints.RArm.RElbowRoll, [0.5], 0.3)
        return self.fluentMotion


    def lStraight(self):
        self.fluentMotion.moveWithDegrees(self.joints.LArm.LElbowRoll, [0.5], 0.3)
        return self.fluentMotion
