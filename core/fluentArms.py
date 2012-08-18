from fluentJoints import FluentJoints
class FluentArms():

    # init method
    def __init__(self, fluentMotion):
        
        # jobs for threading
        self.fluentMotion = fluentMotion
        self.joints = fluentMotion.joints
        self.chains = fluentMotion.chains
        self.log = fluentMotion.log

    ###################################
    # Forward
    ###################################
    def forward(self, duration = 1):     
        self.rForward(duration)
        self.lForward(duration)
        return self.fluentMotion;

    def lForward(self, duration = 1):     
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LShoulderRoll, 0, duration)
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LShoulderPitch, 0, duration)
        return self.fluentMotion;
        
    def rForward(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RShoulderRoll, 0, duration)
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RShoulderPitch, 0, duration)
        return self.fluentMotion;

    ###################################
    # Out
    ###################################
    def out(self, duration = 1):     
        self.rOut(duration)
        self.lOut(duration)
        return self.fluentMotion;

    def lOut(self, duration = 1):     
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LShoulderRoll, 90, duration)
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LShoulderPitch, 0, duration)
        return self.fluentMotion;
        
    def rOut(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RShoulderRoll, -90, duration)
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RShoulderPitch, 0, duration)
        return self.fluentMotion;

    ###################################
    # Up
    ###################################
    def up(self, duration = 1):     
        self.rUp(duration)
        self.lUp(duration)
        return self.fluentMotion;

    def lUp(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LShoulderPitch, -90, duration)
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LShoulderRoll, 0, duration)
        return self.fluentMotion;
        
    def rUp(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RShoulderPitch, -90, duration) 
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RShoulderRoll, 0, duration)
        return self.fluentMotion;

    ###################################
    # Down
    ###################################
    def down(self, duration = 1):     
        self.rDown(duration)
        self.lDown(duration)
        return self.fluentMotion;

    def lDown(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LShoulderPitch, 90, duration)
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LShoulderRoll, 0, duration)
        return self.fluentMotion;
        
    def rDown(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RShoulderPitch, 90, duration) 
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RShoulderRoll, 0, duration)
        return self.fluentMotion;


    ###################################
    # Back
    ###################################
    def back(self, duration = 1):     
        self.rBack(duration)
        self.lBack(duration)
        return self.fluentMotion;

    def lBack(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LShoulderPitch, 119.5, duration)
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LArm.LShoulderRoll, 0, duration)
        return self.fluentMotion;
        
    def rBack(self, duration = 1):
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RShoulderPitch, 119.5, duration) 
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RArm.RShoulderRoll, 0, duration)
        return self.fluentMotion;