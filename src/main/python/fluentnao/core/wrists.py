import math
from joints import Joints

class Wrists():

    # init method
    def __init__(self, nao, hands):
        
        self.hands = hands

        # jobs for threading
        self.nao = nao
        self.joints = nao.joints
        self.chains = nao.chains
        self.log = nao.log

    def go(self):
        self.nao.go()
        
    ###################################
    # Center
    ###################################
    def center(self, duration=0, offset=0):     
        self.left_center(duration, offset)
        self.right_center(duration, offset)
        return self;

    def left_center(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)       
        angle = 0.0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LWristYaw, angle, duration)
        return self;
        
    def right_center(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0.0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RWristYaw, angle, duration)
        return self;

    ###################################
    # Out
    ###################################
    def turn_out(self, duration=0, offset=0):     
        self.left_turn_out(duration, offset)
        self.right_turn_out(duration, offset)
        return self;

    def left_turn_out(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)       
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LWristYaw, angle, duration)
        return self;
        
    def right_turn_out(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RWristYaw, angle, duration)
        return self;

    ###################################
    # In
    ###################################
    def turn_in(self, duration=0, offset=0):     
        self.left_turn_in(duration, offset)
        self.right_turn_in(duration, offset)
        return self;

    def left_turn_in(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)      
        angle = -90 - offset   
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LWristYaw, angle, duration)
        return self;
        
    def right_turn_in(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)   
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RWristYaw, angle, duration)
        return self;