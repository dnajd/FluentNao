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
        self.lOpen(duration)
        self.rOpen(duration)
        return self;

    def lOpen(self, duration=0):
        duration = self.nao.determineDuration(duration)       
        self.nao.moveWithDegreesAndDuration(self.joints.LArm.LHand, math.degrees(1.0), duration)
        return self;
        
    def rOpen(self, duration=0):
        duration = self.nao.determineDuration(duration)  
        self.nao.moveWithDegreesAndDuration(self.joints.RArm.RHand, math.degrees(1.0), duration)
        return self;

    ###################################
    # Hands Close
    ###################################
    def close(self, duration=0):     
        self.lClose(duration)
        self.rClose(duration)
        return self;

    def lClose(self, duration=0):
        duration = self.nao.determineDuration(duration)       
        self.nao.moveWithDegreesAndDuration(self.joints.LArm.LHand, math.degrees(0.0), duration)
        return self;
        
    def rClose(self, duration=0):
        duration = self.nao.determineDuration(duration)  
        self.nao.moveWithDegreesAndDuration(self.joints.RArm.RHand, math.degrees(0.0), duration)
        return self;
