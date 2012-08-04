from fluentJoints import FluentJoints
class FluentHands():

    # init method
    def __init__(self, fluentMotion, joints, chains, log):
        
        # jobs for threading
        self.fluentMotion = fluentMotion
        self.joints = joints
        self.chains = chains

    ###################################
    # Hands Open
    ###################################
    def open(self):     
        self.lOpen()
        self.rOpen()
        return self.fluentMotion;

    def lOpen(self):     
        self.fluentMotion.move(self.joints.LArm.LHand, [1], 0.3)
        return self.fluentMotion;
        
    def rOpen(self):
        self.fluentMotion.move(self.joints.RArm.RHand, [1], 0.3)  
        return self.fluentMotion;

    ###################################
    # Hands Close
    ###################################
    def close(self):     
        self.lClose()
        self.rClose()
        return self.fluentMotion;

    def lClose(self):     
        self.fluentMotion.move(self.joints.LArm.LHand, [0], 0.3)
        return self.fluentMotion;
        
    def rClose(self):
        self.fluentMotion.move(self.joints.RArm.RHand, [0], 0.3)  
        return self.fluentMotion;