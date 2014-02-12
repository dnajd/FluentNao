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
    # Stiff
    ###################################
    def stiff(self):
        self.left_stiff()
        self.right_stiff()
        return self;
        
    def left_stiff(self):
        pNames = self.joints.Chains.LLeg
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    def right_stiff(self):
        pNames = self.joints.Chains.RLeg
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;


    ###################################
    # Relax
    ###################################
    def relax(self):
        self.left_relax()
        self.right_relax()
        return self;

    def left_relax(self):
        pNames = self.joints.Chains.LLeg
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    def right_relax(self):
        pNames = self.joints.Chains.RLeg
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

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
    def left_out(self, duration=0, offset=0, balance=True):

        if balance:
            self.nao.feet.left_plane_on()

        # move leg out
        duration = self.nao.determine_duration(duration)       
        angle = 35 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipRoll, angle, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;

    def right_out(self, duration=0, offset=0, balance=True):

        if balance:
            self.nao.feet.right_plane_on()

        # move leg out
        duration = self.nao.determine_duration(duration)       
        angle = -35 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipRoll, angle, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;

    ###################################
    # In
    ###################################
    def left_in(self, duration=0, offset=0, offset2=0, balance=True):

        if balance:
            self.nao.feet.left_plane_on()

        # move leg in
        duration = self.nao.determine_duration(duration)       
        
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipRoll, angle, duration)

        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle2, duration)
        
        if balance:
            self.nao.feet.plane_off()

        return self;

    def right_in(self, duration=0, offset=0, offset2=0, balance=True):

        if balance:
            self.nao.feet.right_plane_on()

        # move leg out
        duration = self.nao.determine_duration(duration) 

        angle = 0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipRoll, angle, duration)

        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle2, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;

    ###################################
    # Forward
    ###################################
    def left_forward(self, duration=0, offset=0, balance=True):

        if balance:
            self.nao.feet.left_plane_on()

        # move leg forward
        duration = self.nao.determine_duration(duration)       
        angle = -50 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;


    def right_forward(self, duration=0, offset=0, balance=True):

        if balance:
            self.nao.feet.right_plane_on()

        # move leg forward
        duration = self.nao.determine_duration(duration)       
        angle = -50 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle, duration)

        if balance:
            self.nao.feet.plane_off()
        
        return self;

    ###################################
    # Back
    ###################################
    def left_back(self, duration=0, offset=0, balance=True):

        if balance:
            self.nao.feet.left_plane_on()

        # move leg forward
        duration = self.nao.determine_duration(duration)       
        angle = 50 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;


    def right_back(self, duration=0, offset=0, balance=True):

        if balance:
            self.nao.feet.right_plane_on()

        # move leg forward
        duration = self.nao.determine_duration(duration)       
        angle = 50 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle, duration)

        if balance:
            self.nao.feet.plane_off()
        
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
    # Knee Bent
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
    # Knee Straight
    ###################################

    def left_knee_straight(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration) 
        angle = 0 - offset      
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LKneePitch, angle, duration)
        return self;
        
    def right_knee_straight(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RKneePitch, angle, duration)
        return self;


