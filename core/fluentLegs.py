from fluentJoints import FluentJoints
class FluentLegs():

    # init method
    def __init__(self, fluentMotion):
        
        # jobs for threading
        self.fluentMotion = fluentMotion
        self.joints = fluentMotion.joints
        self.chains = fluentMotion.chains
        self.log = fluentMotion.log

    ###################################
    # Balance
    ###################################
    def balanceOnLeft(self, duration=0):
        self.fluentMotion.balance("LLeg", duration)

    def balanceOnRight(self, duration=0):
        self.fluentMotion.balance("RLeg", duration)

    def balanceCenter(self, duration=0):
        self.fluentMotion.balance("Legs", duration)

    ###################################
    # Forward
    ###################################
    def forward(self, duration=0):   
        self.rForward(duration)
        self.lForward(duration)
        return self;

    def lForward(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)       
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LLeg.LHipPitch, -90, duration)
        return self;
        
    def rForward(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RLeg.RHipPitch, -90, duration)
        return self;

    ###################################
    # Down
    ###################################
    def down(self, duration=0):   
        self.rDown(duration)
        self.lDown(duration)
        return self;

    def lDown(self, duration=0):
        self.lStraight(duration)
        duration = self.fluentMotion.determineDuration(duration)       
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LLeg.LHipPitch, 0, duration)
        return self;
        
    def rDown(self, duration=0):
        self.rStraight(duration)
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RLeg.RHipPitch, 0, duration)
        return self;


    ###################################
    # Bent
    ###################################
    def bent(self, duration=0):   
        self.rBent(duration)
        self.lBent(duration)
        return self;

    def lBent(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)       
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LLeg.LKneePitch, 90, duration)
        return self;
        
    def rBent(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RLeg.RKneePitch, 90, duration)
        return self;


    ###################################
    # Straight
    ###################################
    def straight(self, duration=0):   
        self.rStraight(duration)
        self.lStraight(duration)
        return self;

    def lStraight(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)       
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LLeg.LKneePitch, 0, duration)
        return self;
        
    def rStraight(self, duration=0):
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RLeg.RKneePitch, 0, duration)
        return self;


    ###################################
    # KneeUp
    ###################################
    def lKneeUp(self, duration=0):
        self.lForward(duration)
        self.lBent(duration)
        return self;
        
    def rKneeUp(self, duration=0):
        self.rForward(duration)
        self.rBent(duration)
        return self;
