from fluentJoints import FluentJoints
class FluentHead():

    # init method
    def __init__(self, fluentNao):
        
        # jobs for threading
        self.fluentNao = fluentNao
        self.joints = fluentNao.joints
        self.chains = fluentNao.chains
        self.log = fluentNao.log

    def go(self):
        self.fluentNao.go()
        
    ###################################
    # turn
    ###################################
    def left(self, duration=0, offset=0):  
        duration = self.fluentNao.determineDuration(duration)  
        angle = 90 + offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.Head.HeadYaw, angle, duration)  
        return self;
        
    def right(self, duration=0, offset=0):   
        duration = self.fluentNao.determineDuration(duration)   
        angle = -90 - offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.Head.HeadYaw, angle, duration)  
        return self;

    def forward(self, duration=0, offset=0):   
        duration = self.fluentNao.determineDuration(duration)  
        angle = 0 + offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.Head.HeadYaw, angle, duration)  
        return self;


    ###################################
    # up / down
    ###################################

    def up(self, duration=0, offset=0):   
        duration = self.fluentNao.determineDuration(duration)  
        angle = -38 - offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.Head.HeadPitch, angle, duration)  
        return self;

    def down(self, duration=0, offset=0):   
        duration = self.fluentNao.determineDuration(duration)  
        angle = 29 + offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.Head.HeadPitch, angle, duration)  
        return self;

    def center(self, duration=0, offset=0):   
        duration = self.fluentNao.determineDuration(duration)  
        angle = 0 + offset
        self.fluentNao.moveWithDegreesAndDuration(self.joints.Head.HeadPitch, angle, duration)  
        return self;