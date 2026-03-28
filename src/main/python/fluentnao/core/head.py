'''
FluentNao Head Module -- controls head yaw and pitch joints on the NAO robot.

This module provides the Head class, which queues head movements using
a fluent chaining API. Moves are queued until go() is called.

Key Methods
-----------
Yaw (horizontal rotation):
    left(duration=0, offset=0)    -- turn head left (90 deg yaw)
    right(duration=0, offset=0)   -- turn head right (-90 deg yaw)
    forward(duration=0, offset=0) -- face forward (0 deg yaw)

Pitch (vertical tilt):
    up(duration=0, offset=0)      -- tilt head up (-38 deg pitch)
    down(duration=0, offset=0)    -- tilt head down (29 deg pitch)
    center(duration=0, offset=0)  -- center head pitch (0 deg)

Stiffness:
    stiff() -- set head to full stiffness (1.0)
    relax() -- release head (stiffness 0)

Parameters:
    duration -- movement duration in seconds; 0 uses the nao default duration.
    offset   -- degrees added to the base angle for fine adjustment.
                For up(), a positive offset tilts further up (more negative pitch).
                For down(), a positive offset tilts further down.

Execution:
    go() -- execute all queued moves and return the nao object.

Usage Examples
--------------
    # Turn head left
    nao.head.left().go()

    # Tilt head up with offset
    nao.head.up(0, -15).go()

    # Look forward and slightly down
    nao.head.forward().down(0, 5).go()

Notes
-----
- This is Python 2.7 code.
- The head has no left/right sub-variants since there is only one head.
- All methods return self (the Head instance) for chaining, except go()
  which returns the nao object.
'''

class Head():

    # init method
    def __init__(self, nao):
        
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
        pNames = self.joints.Chains.Head
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    ###################################
    # Relax
    ###################################
    def relax(self):
        pNames = self.joints.Chains.Head
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    ###################################
    # turn
    ###################################
    def left(self, duration=0, offset=0):  
        duration = self.nao.determine_duration(duration)  
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadYaw, angle, duration)  
        return self;
        
    def right(self, duration=0, offset=0):   
        duration = self.nao.determine_duration(duration)   
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadYaw, angle, duration)  
        return self;

    def forward(self, duration=0, offset=0):   
        duration = self.nao.determine_duration(duration)  
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadYaw, angle, duration)  
        return self;


    ###################################
    # up / down
    ###################################

    def up(self, duration=0, offset=0):   
        duration = self.nao.determine_duration(duration)  
        angle = -38 - offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadPitch, angle, duration)  
        return self;

    def down(self, duration=0, offset=0):   
        duration = self.nao.determine_duration(duration)  
        angle = 29 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadPitch, angle, duration)  
        return self;

    def center(self, duration=0, offset=0):   
        duration = self.nao.determine_duration(duration)  
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadPitch, angle, duration)  
        return self;