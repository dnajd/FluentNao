class Head():

    # init method
    def __init__(self, nao):
        
        # jobs for threading
        self.nao = nao
        self.joints = nao.joints
        self.chains = nao.chains
        self.log = nao.log

    def go(self):
        self.nao.go()
        
    ###################################
    # turn
    ###################################
    def left(self, duration=0, offset=0):  
        duration = self.nao.determine_duration(duration)  
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadYaw, angle, duration)  
        return self;
        
    def right(self, duration=0, offset=0):   
        duration = self.nao.determine_duration(duration)   
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadYaw, angle, duration)  
        return self;

    def forward(self, duration=0, offset=0):   
        duration = self.nao.determine_duration(duration)  
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadYaw, angle, duration)  
        return self;


    ###################################
    # up / down
    ###################################

    def up(self, duration=0, offset=0):   
        duration = self.nao.determine_duration(duration)  
        angle = -38 - offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadPitch, angle, duration)  
        return self;

    def down(self, duration=0, offset=0):   
        duration = self.nao.determine_duration(duration)  
        angle = 29 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadPitch, angle, duration)  
        return self;

    def center(self, duration=0, offset=0):   
        duration = self.nao.determine_duration(duration)  
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadPitch, angle, duration)  
        return self;