'''
FluentNao Wrists Module -- controls wrist rotation (WristYaw) on the NAO robot.

This module provides the Wrists class, which queues wrist yaw movements
using a fluent chaining API. Moves are queued until go() is called.

Key Methods
-----------
    center(duration=0, offset=0)    -- rotate both wrists to center (0 deg)
    turn_out(duration=0, offset=0)  -- rotate both wrists outward (90 deg)
    turn_in(duration=0, offset=0)   -- rotate both wrists inward (-90 deg)

Each method has left_ and right_ variants, e.g. left_center(), right_turn_out().

Parameters:
    duration -- movement duration in seconds; 0 uses the nao default duration.
    offset   -- degrees added to the base angle for fine adjustment.

Execution:
    go() -- execute all queued moves and return the nao object.

Sub-objects (accessible for chaining):
    wrists.hands -- Hands instance

Usage Examples
--------------
    # Turn both wrists outward
    nao.wrists.turn_out().go()

    # Center left wrist only
    nao.wrists.left_center().go()

    # Chain from arms: arms forward, wrists turned in
    nao.arms.forward().wrists.turn_in().go()

Notes
-----
- This is Python 2.7 code.
- All methods return self (the Wrists instance) for chaining, except go()
  which returns the nao object.
- Left and right angles are mirrored automatically so the same offset
  produces symmetric movement.
'''

class Wrists():

    # init method
    def __init__(self, nao, hands):
        
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
    # Center
    ###################################
    def center(self, duration=0, offset=0):     
        self.left_center(duration, offset)
        self.right_center(duration, offset)
        return self;

    def left_center(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)       
        angle = 0.0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LWristYaw, angle, duration)
        return self;
        
    def right_center(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = 0.0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RWristYaw, angle, duration)
        return self;

    ###################################
    # Out
    ###################################
    def turn_out(self, duration=0, offset=0):     
        self.left_turn_out(duration, offset)
        self.right_turn_out(duration, offset)
        return self;

    def left_turn_out(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)       
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LWristYaw, angle, duration)
        return self;
        
    def right_turn_out(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RWristYaw, angle, duration)
        return self;

    ###################################
    # In
    ###################################
    def turn_in(self, duration=0, offset=0):     
        self.left_turn_in(duration, offset)
        self.right_turn_in(duration, offset)
        return self;

    def left_turn_in(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)      
        angle = -90 - offset   
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LWristYaw, angle, duration)
        return self;
        
    def right_turn_in(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)   
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RWristYaw, angle, duration)
        return self;