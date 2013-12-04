class Feet():

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
    # point
    ###################################
    def point_toes(self, duration=0, offset=0):   
        self.left_point_toes(duration, offset)
        self.right_point_toes(duration, offset)
        return self;

    def left_point_toes(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)       
        angle = 52.8 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnklePitch, angle, duration)
        return self;
        
    def right_point_toes(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 52.8 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnklePitch, angle, duration)
        return self;

   
    ###################################
    # raise
    ###################################
    def raise_toes(self, duration=0, offset=0):   
        self.right_raise_toes(duration, offset)
        self.left_raise_toes(duration, offset)
        return self;

    def right_raise_toes(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)       
        angle = -68.0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnklePitch, angle, duration)
        return self;
        
    def left_raise_toes(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = -68.0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnklePitch, angle, duration)
        return self;


    ###################################
    # out
    ###################################
    def turn_out(self, duration=0, offset=0):   
        self.right_turn_out(duration, offset)
        self.left_turn_out(duration, offset)
        return self;

    def left_turn_out(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)       
        angle = 22 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnkleRoll, angle, duration)
        return self;
        
    def right_turn_out(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)        
        angle = -22 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnkleRoll, angle, duration)
        return self;


    ###################################
    # in
    ###################################
    def turn_in(self, duration=0, offset=0):   
        self.right_turn_in(duration, offset)
        self.left_turn_in(duration, offset)
        return self;

    def left_turn_in(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)       
        angle = -22.8 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnkleRoll, angle, duration)
        return self;
        
    def right_turn_in(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)        
        angle = 22.8 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnkleRoll, angle, duration)
        return self;


    ###################################
    # center
    ###################################
    def center(self, duration=0, offset=0):   
        self.right_center(duration, offset)
        self.left_center(duration, offset)
        return self;

    def left_center(self, duration=0, offset=0, offset2=0):
        angle = 0 - offset
        angle2 = 0 - offset2

        duration = self.nao.determine_duration(duration)       
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnkleRoll, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnklePitch, angle2, duration)
        return self;
        
    def right_center(self, duration=0, offset=0, offset2=0):
        duration = self.nao.determine_duration(duration)      
        angle = 0 + offset
        angle2 = 0 - offset2  
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnkleRoll, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnklePitch, angle2, duration)
        return self;