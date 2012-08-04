from fluentJoints import FluentJoints
class FluentArms():

    # init method
    def __init__(self, fluentMotion, joints, chains, log):
        
        # jobs for threading
        self.fluentMotion = fluentMotion
        self.joints = joints
        self.chains = chains

    ###################################
    # Arms Forward
    ###################################
    def forward(self):     
        self.rForward()
        self.lForward()
        return self.fluentMotion;

    def lForward(self):     
        self.fluentMotion.moveWithDegrees(self.joints.LArm.LShoulderRoll, [0], 0.3)
        self.fluentMotion.moveWithDegrees(self.joints.LArm.LShoulderPitch, [0], 0.3)
        return self.fluentMotion;
        
    def rForward(self):
        self.fluentMotion.moveWithDegrees(self.joints.RArm.RShoulderRoll, [0], 0.3)  
        self.fluentMotion.moveWithDegrees(self.joints.RArm.RShoulderPitch, [0], 0.3)  
        return self.fluentMotion;

    ###################################
    # Arms Out
    ###################################
    def out(self):     
        self.rOut()
        self.lOut()
        return self.fluentMotion;

    def lOut(self):     
        self.fluentMotion.moveWithDegrees(self.joints.LArm.LShoulderRoll, [90], 0.3)
        return self.fluentMotion;
        
    def rOut(self):
        self.fluentMotion.moveWithDegrees(self.joints.RArm.RShoulderRoll, [-90], 0.3)  
        return self.fluentMotion;

    ###################################
    # Arms Up
    ###################################
    def up(self):     
        self.rUp()
        self.lUp()
        return self.fluentMotion;

    def lUp(self):     
        self.fluentMotion.moveWithDegrees(self.joints.LArm.LShoulderPitch, [-90], 0.3)
        return self.fluentMotion;
        
    def rUp(self):
        self.fluentMotion.moveWithDegrees(self.joints.RArm.RShoulderPitch, [-90], 0.3)  
        return self.fluentMotion;

    ###################################
    # Arms Down
    ###################################
    def down(self):     
        self.rDown()
        self.lDown()
        return self.fluentMotion;

    def lDown(self):     
        self.fluentMotion.moveWithDegrees(self.joints.LArm.LShoulderPitch, [90], 0.3)
        return self.fluentMotion;
        
    def rDown(self):
        self.fluentMotion.moveWithDegrees(self.joints.RArm.RShoulderPitch, [90], 0.3)  
        return self.fluentMotion;