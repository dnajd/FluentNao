from joints import Joints
class Legs():

    # init method
    def __init__(self, nao, feet):
        
        self.feet = feet

        # jobs for threading
        self.nao = nao
        self.joints = nao.joints
        self.chains = nao.chains
        self.log = nao.log

    def go(self):
        self.nao.go()
        
    ###################################
    # Balance
    ###################################
    def left_balance(self, duration=0):
        self.nao.balance(self.joints.SupportLeg.LLeg, duration)
        return self;

    def right_balance(self, duration=0):
        self.nao.balance(self.joints.SupportLeg.RLeg, duration)
        return self;

    def balance(self, duration=0):
        self.nao.balance(self.joints.SupportLeg.Legs, duration)
        return self;


    ###################################
    # Out
    ###################################
    def left_out(self, duration=0, offset=0):

        # move leg out
        duration = self.nao.determine_duration(duration)       
        angle = 35 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipRoll, angle, duration)

        # turn feet in
        self.feet.lTurnIn()
        self.feet.rTurnIn(0, -15)

        return self;

    def right_out(self, duration=0, offset=0):

        # move leg out
        duration = self.nao.determine_duration(duration)       
        angle = -35 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipRoll, angle, duration)

        # turn feet in
        self.feet.rTurnIn()
        self.feet.lTurnIn(0, -15)

        return self;

    ###################################
    # Forward
    ###################################
    def left_forward(self, duration=0, offset=0):

        # stiffen body & enable wb
        self.nao.stiff()
        self.nao.whole_body_enable()

        # constrain feet
        self.nao.foot_state(self.joints.SupportLeg.RLeg, self.joints.StateName.Fixed)
        self.nao.foot_state(self.joints.SupportLeg.LLeg, self.joints.StateName.Plane)

        # move leg forward
        duration = self.nao.determine_duration(duration)       
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle, duration)

        # block call
        self.go()

        # free feet & disable wb
        self.nao.foot_state(self.joints.SupportLeg.Legs, self.joints.StateName.Free)
        self.nao.whole_body_disable()

        return self;


    def right_forward(self, duration=0, offset=0):

        # stiffen body & enable wb
        self.nao.stiff()
        self.nao.whole_body_enable()

        # constrain feet
        self.nao.foot_state(self.joints.SupportLeg.LLeg, self.joints.StateName.Fixed)
        self.nao.foot_state(self.joints.SupportLeg.RLeg, self.joints.StateName.Plane)

        # move leg forward
        duration = self.nao.determine_duration(duration)       
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle, duration)

        # block call
        self.go()

        # free feet & disable wb
        self.nao.foot_state(self.joints.SupportLeg.Legs, self.joints.StateName.Free)
        self.nao.whole_body_disable()
        
        return self;

    ###################################
    # Up
    ###################################
    def left_up(self, duration=0, offset=0):
        self.right_balance(duration)
        duration = self.nao.determine_duration(duration)       
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle, duration)
        return self;
        
    def right_up(self, duration=0, offset=0):
        self.left_balance(duration)
        duration = self.nao.determine_duration(duration)  
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle, duration)
        return self;


    ###################################
    # KneeUp
    ###################################
    def left_knee_up(self, duration=0, offset=0):
        self.right_balance(duration)
        self.left_up(duration, offset)
        self.left_knee_bent(duration, offset)
        return self;
        
    def right_knee_up(self, duration=0, offset=0):
        self.left_balance(duration)
        self.right_up(duration, offset)
        self.right_knee_bent(duration, offset)
        return self;

    ###################################
    # Down
    ###################################

    def left_down(self, duration=0, offset=0):
        self.left_balance(duration)
        duration = self.nao.determine_duration(duration)       
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle, duration)
        return self;
        
    def right_down(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle, duration)
        return self;


    ###################################
    # Bent
    ###################################
    
    def left_knee_bent(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)       
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LKneePitch, angle, duration)
        return self;
        
    def right_knee_bent(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RKneePitch, angle, duration)
        return self;


    ###################################
    # Straight
    ###################################

    def left_straight(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration) 
        angle = 0 - offset      
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LKneePitch, angle, duration)
        return self;
        
    def right_straight(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RKneePitch, angle, duration)
        return self;


