'''
FluentNao Legs Module -- controls leg chains (LLeg, RLeg) on the NAO robot.

This module provides the Legs class, which queues hip and knee joint
movements using a fluent chaining API. Many methods support optional
whole body balance via plane constraints to keep the robot stable.

Key Methods
-----------
Hip (left_ and right_ variants only -- no both-legs version):
    left_out / right_out(duration=0, offset=0, balance=True)
        -- move leg outward (HipRoll, 35 deg)
    left_in / right_in(duration=0, offset=0, offset2=0, balance=True)
        -- move leg inward (HipPitch + HipRoll, 0 deg)
    left_forward / right_forward(duration=0, offset=0, balance=True)
        -- move leg forward (HipPitch, -50 deg)
    left_back / right_back(duration=0, offset=0, balance=True)
        -- move leg back (HipPitch, 50 deg)
    left_up / right_up(duration=0, offset=0)
        -- raise leg (HipPitch, -90 deg); auto-balances on opposite leg
    left_down / right_down(duration=0, offset=0)
        -- lower leg (HipPitch, 0 deg)

Knee:
    left_knee_bent / right_knee_bent(duration=0, offset=0)
        -- bend knee (KneePitch, 90 deg)
    left_knee_straight / right_knee_straight(duration=0, offset=0)
        -- straighten knee (KneePitch, 0 deg)
    left_knee_up / right_knee_up(duration=0, offset=0)
        -- raise leg with bent knee (combines up + knee_bent + balance)

Balance:
    balance(duration=0)       -- balance on both legs
    left_balance(duration=0)  -- balance on left leg
    right_balance(duration=0) -- balance on right leg

Stiffness:
    stiff() / relax()         -- both legs
    left_stiff() / right_stiff() / left_relax() / right_relax()

Parameters:
    duration -- movement duration in seconds; 0 uses the nao default.
    offset   -- degrees added to the base angle for fine adjustment.
    balance  -- when True (default), enables whole body balance by
                constraining the support foot as Fixed and the moving
                foot as Plane, then releasing after go().

Execution:
    go() -- execute all queued moves and return the nao object.

Sub-objects (accessible for chaining):
    legs.feet -- Feet instance

Usage Examples
--------------
    # Move left leg out with balance
    nao.legs.left_out().go()

    # Right knee up (balances on left leg automatically)
    nao.legs.right_knee_up().go()

    # Move leg without balance
    nao.legs.left_forward(2, 10, balance=False).go()

Notes
-----
- This is Python 2.7 code.
- Most leg methods only have left_ and right_ variants (no both-legs version)
  because moving both legs simultaneously would cause the robot to fall.
- When balance=True, the method calls feet.left_plane_on() or
  feet.right_plane_on() before the move, and feet.plane_off() after,
  which stiffens the body and enables whole body balancing.
- All methods return self (the Legs instance) for chaining, except go()
  which returns the nao object.
'''

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
        return self.nao


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
        angle = 0 - offset
        angle2 = 0 + offset2        
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipRoll, angle2, duration)
        
        if balance:
            self.nao.feet.plane_off()

        return self;

    def right_in(self, duration=0, offset=0, offset2=0, balance=True):

        if balance:
            self.nao.feet.right_plane_on()

        # move leg out
        duration = self.nao.determine_duration(duration) 
        angle = 0 - offset
        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipRoll, angle2, duration)

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


