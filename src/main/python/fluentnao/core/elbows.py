'''
FluentNao Elbows Module -- controls elbow joints (ElbowRoll and ElbowYaw) on the NAO robot.

This module provides the Elbows class, which queues elbow flex (roll) and
rotation (yaw) movements using a fluent chaining API. Moves are queued
until go() is called.

Key Methods
-----------
Flex (ElbowRoll):
    bent(duration=0, offset=0)      -- bend both elbows to 89 degrees
    straight(duration=0, offset=0)  -- straighten both elbows to ~0.5 degrees

Rotation (ElbowYaw):
    turn_up(duration=0, offset=0)   -- rotate both elbows up (90 deg yaw)
    turn_down(duration=0, offset=0) -- rotate both elbows down (-90 deg yaw)
    turn_in(duration=0, offset=0)   -- rotate both elbows inward (0 deg yaw)

Each method has left_ and right_ variants, e.g. left_bent(), right_turn_up().

Parameters:
    duration -- movement duration in seconds; 0 uses the nao default duration.
    offset   -- degrees added to the base angle for fine adjustment.

Execution:
    go() -- execute all queued moves and return the nao object.

Sub-objects (accessible for chaining):
    elbows.wrists -- Wrists instance
    elbows.hands  -- Hands instance

Usage Examples
--------------
    # Bend both elbows
    nao.elbows.bent().go()

    # Arms up with elbows bent (chaining from arms)
    nao.arms.up().elbows.bent().go()

    # Right elbow bent with extra 10-degree offset
    nao.elbows.right_bent(0, 10).go()

Notes
-----
- This is Python 2.7 code.
- All methods return self (the Elbows instance) for chaining, except go()
  which returns the nao object.
- Left and right angles are automatically mirrored (left uses negative roll
  values, right uses positive) so the same offset produces symmetric movement.
'''

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
        return self.nao

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