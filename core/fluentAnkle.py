from fluentJoints import FluentJoints
class FluentAnkle():

    # init method
    def __init__(self, fluentMotion):
        
        # jobs for threading
        self.fluentMotion = fluentMotion
        self.joints = fluentMotion.joints
        self.chains = fluentMotion.chains
        self.log = fluentMotion.log

    def go(self):
        self.fluentMotion.go()
        
    ###################################
    # Point Toe
    ###################################
    def pointToes(self, duration=0, offset=0):   
        self.rPointToe(duration, offset)
        self.lPointToe(duration, offset)
        return self;

    def lPointToe(self, duration=0, offset=0):
        duration = self.fluentMotion.determineDuration(duration)       
        angle = 52.8 + offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.LLeg.LAnklePitch, angle, duration)
        return self;
        
    def rPointToe(self, duration=0, offset=0):
        duration = self.fluentMotion.determineDuration(duration)  
        angle = 52.8 + offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.RLeg.RAnklePitch, angle, duration)
        return self;