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
    # Stiff
    ###################################
    def stiff(self):
        self.left_stiff()
        self.right_stiff()
        return self;
        
    def left_stiff(self):
        pNames = self.joints.Chains.LArm
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    def right_stiff(self):
        pNames = self.joints.Chains.RArm
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
        pNames = self.joints.Chains.LArm
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    def right_relax(self):
        pNames = self.joints.Chains.RArm
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    ###################################
    # Forward
    ###################################
    def forward(self, duration=0, offset=0, offset2=0):   
        self.right_forward(duration, offset, offset2)
        self.left_forward(duration, offset, offset2)
        return self;

    def left_forward(self, duration=0, offset=0, offset2=0):
        duration = self.nao.determine_duration(duration)       
        angle = 0 - offset
        angle2 = 0 + offset2
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, angle2, duration)

        return self;
        
    def right_forward(self, duration=0, offset=0, offset2=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0 - offset
        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, angle2, duration)
        return self;

    ###################################
    # Out
    ###################################
    def out(self, duration=0, offset=0, offset2=0):     
        self.right_out(duration, offset, offset2)
        self.left_out(duration, offset, offset2)
        return self;

    def left_out(self, duration=0, offset=0, offset2=0):     
        duration = self.nao.determine_duration(duration)  
        angle = 0 - offset
        angle2 = 90 + offset2
        
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, angle2, duration)
        return self;
        
    def right_out(self, duration=0, offset=0, offset2=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0 - offset
        angle2 = -90 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, angle2, duration)
        return self;

    ###################################
    # Up
    ###################################
    def up(self, duration=0, offset=0, offset2=0):     
        self.right_up(duration, offset, offset2)
        self.left_up(duration, offset, offset2)
        return self;

    def left_up(self, duration=0, offset=0, offset2=0):
        duration = self.nao.determine_duration(duration)    
        angle = -90 - offset
        angle2 = 0 + offset2
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, angle2, duration)
        return self;
        
    def right_up(self, duration=0, offset=0, offset2=0):
        duration = self.nao.determine_duration(duration)   
        angle = -90 - offset
        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration) 
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, angle2, duration)
        return self;

    ###################################
    # Down
    ###################################
    def down(self, duration=0, offset=0, offset2=0):     
        self.right_down(duration, offset, offset2)
        self.left_down(duration, offset, offset2)
        return self;

    def left_down(self, duration=0, offset=0, offset2=0):
        duration = self.nao.determine_duration(duration)   
        angle = 90 - offset
        angle2 = 0 + offset2
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, angle2, duration)
        return self;
        
    def right_down(self, duration=0, offset=0, offset2=0):
        duration = self.nao.determine_duration(duration)   
        angle = 90 - offset
        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration) 
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, angle2, duration)
        return self;


    ###################################
    # Back
    ###################################
    def back(self, duration=0, offset=0, offset2=0):     
        self.right_back(duration, offset, offset2)
        self.left_back(duration, offset, offset2)
        return self;

    def left_back(self, duration=0, offset=0, offset2=0):
        duration = self.nao.determine_duration(duration)  
        angle = 119.5 - offset
        angle2 = 0 + offset2
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, angle2, duration)
        return self;
        
    def right_back(self, duration=0, offset=0, offset2=0):
        duration = self.nao.determine_duration(duration)  
        angle = 119.5 - offset
        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration) 
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, angle2, duration)
        return self;