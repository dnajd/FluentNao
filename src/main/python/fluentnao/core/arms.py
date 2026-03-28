'''
FluentNao Arms Module -- controls both arm chains (LArm, RArm) on the NAO robot.

This module provides the Arms class, which queues shoulder joint movements
(ShoulderPitch and ShoulderRoll) using a fluent chaining API. Moves are
queued until go() is called, which executes them and returns the top-level
nao object so you can continue chaining other body parts.

Key Methods
-----------
Positional (both arms):
    up(duration=0, offset=0, offset2=0)       -- arms straight up (-90 deg pitch)
    down(duration=0, offset=0, offset2=0)     -- arms straight down (90 deg pitch)
    forward(duration=0, offset=0, offset2=0)  -- arms forward (0 deg pitch)
    out(duration=0, offset=0, offset2=0)      -- arms out to sides (90 deg roll)
    back(duration=0, offset=0, offset2=0)     -- arms behind (119.5 deg pitch)

Each positional method has left_ and right_ variants, e.g. left_up(), right_forward().

Parameters:
    duration -- movement duration in seconds; 0 uses the nao default duration.
    offset   -- degrees added to the primary angle (ShoulderPitch).
    offset2  -- degrees added to the secondary angle (ShoulderRoll).

Stiffness:
    stiff()       -- set both arms to full stiffness (1.0)
    relax()       -- release both arms (stiffness 0)
    left_stiff(), right_stiff(), left_relax(), right_relax() -- per-arm variants.

Execution:
    go() -- execute all queued moves and return the nao object.

Sub-objects (accessible for chaining):
    arms.elbows  -- Elbows instance
    arms.wrists  -- Wrists instance
    arms.hands   -- Hands instance

Usage Examples
--------------
    # Raise both arms
    nao.arms.up().go()

    # Left arm forward with 2-second duration and 15-degree pitch offset,
    # right arm out, then execute
    nao.arms.left_forward(2, 15).right_out().go()

    # Chain with sub-parts: arms up with elbows bent
    nao.arms.up().elbows.bent().go()

    # Relax both arms
    nao.arms.relax()

Notes
-----
- This is Python 2.7 code.
- All positional methods return self (the Arms instance) to enable chaining.
- go() returns the nao object (not self), allowing you to chain to other body parts.
- Left and right offsets are mirrored automatically (e.g. left roll is positive,
  right roll is negative) so the same offset value produces symmetric movement.
'''

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
        return self.nao


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