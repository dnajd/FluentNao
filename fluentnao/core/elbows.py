from joints import Joints
class Elbows():

    # init method
    def __init__(self, nao, wrists, hands):
        
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
    # Bent
    ###################################
    def bent(self, duration=0, offset=0):
        self.right_bent(duration, offset)
        self.left_bent(duration, offset)
        return self;

    def right_bent(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 89 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RElbowRoll, angle, duration)
        return self;


    def left_bent(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = -89 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LElbowRoll, angle, duration)
        return self;

    ###################################
    # Straight
    ###################################
    def straight(self, duration=0, offset=0):
        self.right_straight(duration, offset)
        self.left_straight(duration, offset)
        return self;

    def right_straight(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0.5 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RElbowRoll, angle, duration)
        return self;


    def left_straight(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0.5 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LElbowRoll, angle, duration)
        return self;


    ###################################
    # Up
    ###################################
    def turn_up(self, duration=0, offset=0):
        self.right_turn_up(duration, offset)
        self.left_turn_up(duration, offset)
        return self;

    def right_turn_up(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration) 
        angle = 90 + offset 
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RElbowYaw, angle, duration)
        return self;


    def left_turn_up(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = -90 - offset 
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LElbowYaw, angle, duration)
        return self;

    ###################################
    # Turn Down
    ###################################
    def turn_down(self, duration=0, offset=0):
        self.right_turn_down(duration, offset)
        self.left_turn_down(duration, offset)
        return self;

    def right_turn_down(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RElbowYaw, angle, duration)
        return self;

    def left_turn_down(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LElbowYaw, angle, duration)
        return self;


    ###################################
    # In
    ###################################
    def turn_in(self, duration=0, offset=0):
        self.right_turn_in(duration, offset)
        self.left_turn_in(duration, offset)
        return self;

    def right_turn_in(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RElbowYaw, angle, duration)
        return self;

    def left_turn_in(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LElbowYaw, angle, duration)
        return self;