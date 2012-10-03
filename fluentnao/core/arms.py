from joints import Joints

class Arms():

    # init method
    def __init__(self, nao, elbows, wrists, hands):
        
        self.elbows = elbows
        self.wrists = wrists
        self.hands = hands

        # jobs for threading
        self.nao = nao
        self.joints = nao.joints
        self.chains = nao.chains
        self.log = nao.log

    def go(self):
        self.nao.go()
        
    ###################################
    # Forward
    ###################################
    def forward(self, duration=0, offset=0):   
        self.right_forward(duration, offset)
        self.left_forward(duration, offset)
        return self;

    def left_forward(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)       
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, 0, duration)

        return self;
        
    def right_forward(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, 0, duration)
        return self;

    ###################################
    # Out
    ###################################
    def out(self, duration=0, offset=0):     
        self.right_out(duration, offset)
        self.left_out(duration, offset)
        return self;

    def left_out(self, duration=0, offset=0):     
        duration = self.nao.determine_duration(duration)  
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, 0, duration)
        return self;
        
    def right_out(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, 0, duration)
        return self;

    ###################################
    # Up
    ###################################
    def up(self, duration=0, offset=0):     
        self.right_up(duration, offset)
        self.left_up(duration, offset)
        return self;

    def left_up(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)    
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, 0, duration)
        return self;
        
    def right_up(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)   
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration) 
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, 0, duration)
        return self;

    ###################################
    # Down
    ###################################
    def down(self, duration=0, offset=0):     
        self.right_down(duration, offset)
        self.left_down(duration, offset)
        return self;

    def left_down(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)   
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, 0, duration)
        return self;
        
    def right_down(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)   
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration) 
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, 0, duration)
        return self;


    ###################################
    # Back
    ###################################
    def back(self, duration=0, offset=0):     
        self.right_back(duration, offset)
        self.left_back(duration, offset)
        return self;

    def left_back(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 119.5 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, 0, duration)
        return self;
        
    def right_back(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 119.5 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration) 
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, 0, duration)
        return self;