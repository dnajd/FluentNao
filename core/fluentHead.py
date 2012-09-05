from fluentJoints import FluentJoints
class FluentHead():

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
    # turn
    ###################################
    def left(self, duration=0, offset=0):  
        duration = self.fluentMotion.determineDuration(duration)  
        angle = 90 + offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadYaw, angle, duration)  
        return self;
        
    def right(self, duration=0, offset=0):   
        duration = self.fluentMotion.determineDuration(duration)   
        angle = -90 - offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadYaw, angle, duration)  
        return self;

    def forward(self, duration=0, offset=0):   
        duration = self.fluentMotion.determineDuration(duration)  
        angle = 0 + offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadYaw, angle, duration)  
        return self;


    ###################################
    # up / down
    ###################################

    def up(self, duration=0, offset=0):   
        duration = self.fluentMotion.determineDuration(duration)  
        angle = -38 - offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadPitch, angle, duration)  
        return self;

    def down(self, duration=0, offset=0):   
        duration = self.fluentMotion.determineDuration(duration)  
        angle = 29 + offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadPitch, angle, duration)  
        return self;

    def center(self, duration=0, offset=0):   
        duration = self.fluentMotion.determineDuration(duration)  
        angle = 0 + offset
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadPitch, angle, duration)  
        return self;