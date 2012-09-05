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
    def turnLeft(self, duration=0):  
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadYaw, 90, duration)  
        return self;
        
    def turnRight(self, duration=0):   
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadYaw, -90, duration)  
        return self;

    def forward(self, duration=0):   
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadYaw, 0, duration)  
        return self;


    ###################################
    # up / down
    ###################################

    def up(self, duration=0):   
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadPitch, -38, duration)  
        return self;

    def down(self, duration=0):   
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadPitch, 29, duration)  
        return self;

    def center(self, duration=0):   
        duration = self.fluentMotion.determineDuration(duration)  
        self.fluentMotion.moveWithDegreesAndDuration(self.joints.Head.HeadPitch, 0, duration)  
        return self;