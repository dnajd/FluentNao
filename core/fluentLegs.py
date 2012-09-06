from fluentJoints import FluentJoints
class FluentLegs():

    # init method
    def __init__(self, fluentMotion, ankles):
        
        self.ankles = ankles

        # jobs for threading
        self.fluentMotion = fluentMotion
        self.joints = fluentMotion.joints
        self.chains = fluentMotion.chains
        self.log = fluentMotion.log

    def go(self):
        self.fluentMotion.go()
        
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
    # Up
    ###################################
    def up(self, duration=0, offset=0):   
        self.rForward(duration, offset)
        self.lForward(duration, offset)
        return self;

    def lUp(self, duration=0, offset=0):
        self.balanceOnRight(duration)
        duration = self.fluentMotion.determineDuration(duration)       
        angle = -90 - offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LLeg.LHipPitch, angle, duration)
        return self;
        
    def rUp(self, duration=0, offset=0):
        self.balanceOnLeft(duration)
        duration = self.fluentMotion.determineDuration(duration)  
        angle = -90 - offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RLeg.RHipPitch, angle, duration)
        return self;


    ###################################
    # KneeUp
    ###################################
    def lKneeUp(self, duration=0, offset=0):
        self.balanceOnRight(duration)
        self.lUp(duration, offset)
        self.lKneeBent(duration, offset)
        return self;
        
    def rKneeUp(self, duration=0, offset=0):
        self.balanceOnLeft(duration)
        self.rUp(duration, offset)
        self.rKneeBent(duration, offset)
        return self;

    ###################################
    # Down
    ###################################
    def down(self, duration=0, offset=0):   
        self.rDown(duration, offset)
        self.lDown(duration, offset)
        return self;

    def lDown(self, duration=0, offset=0):
        self.balanceOnLeft(duration)
        duration = self.fluentMotion.determineDuration(duration)       
        angle = 0 + offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LLeg.LHipPitch, angle, duration)
        return self;
        
    def rDown(self, duration=0, offset=0):
        duration = self.fluentMotion.determineDuration(duration)  
        angle = 0 + offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RLeg.RHipPitch, angle, duration)
        return self;


    ###################################
    # Bent
    ###################################
    def kneesBent(self, duration=0, offset=0):   
        self.rKneeBent(duration, offset)
        self.lKneeBent(duration, offset)
        return self;

    def lKneeBent(self, duration=0, offset=0):
        duration = self.fluentMotion.determineDuration(duration)       
        angle = 90 + offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LLeg.LKneePitch, angle, duration)
        return self;
        
    def rKneeBent(self, duration=0, offset=0):
        duration = self.fluentMotion.determineDuration(duration)  
        angle = 90 + offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RLeg.RKneePitch, angle, duration)
        return self;


    ###################################
    # Straight
    ###################################
    def straight(self, duration=0, offset=0):   
        self.rStraight(duration, offset)
        self.lStraight(duration, offset)
        return self;

    def lStraight(self, duration=0, offset=0):
        duration = self.fluentMotion.determineDuration(duration) 
        angle = 0 - offset      
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LLeg.LKneePitch, angle, duration)
        return self;
        
    def rStraight(self, duration=0, offset=0):
        duration = self.fluentMotion.determineDuration(duration)  
        angle = 0 - offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RLeg.RKneePitch, angle, duration)
        return self;


