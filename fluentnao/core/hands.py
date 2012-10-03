import math
from joints import Joints
class Hands():

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
    # Hands Open
    ###################################
    def open(self, duration=0):   
        self.right_open(duration)  
        self.left_open(duration)
        return self;

    def left_open(self, duration=0):
        duration = self.nao.determine_duration(duration)       
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LHand, math.degrees(1.0), duration)
        return self;
        
    def right_open(self, duration=0):
        duration = self.nao.determine_duration(duration)  
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RHand, math.degrees(1.0), duration)
        return self;

    ###################################
    # Hands Close
    ###################################
    def close(self, duration=0):    
        self.right_close(duration) 
        self.left_close(duration)
        return self;

    def left_close(self, duration=0):
        duration = self.nao.determine_duration(duration)       
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LHand, math.degrees(0.0), duration)
        return self;
        
    def right_close(self, duration=0):
        duration = self.nao.determine_duration(duration)  
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RHand, math.degrees(0.0), duration)
        return self;
