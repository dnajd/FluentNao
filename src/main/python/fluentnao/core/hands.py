'''
FluentNao Hands Module -- controls hand open/close on the NAO robot.

This module provides the Hands class, which queues hand movements using
a fluent chaining API. Moves are queued until go() is called.

Key Methods
-----------
    open(duration=0)   -- open both hands fully (value 1.0)
    close(duration=0)  -- close both hands fully (value 0.0)

Each method has left_ and right_ variants, e.g. left_open(), right_close().

Parameters:
    duration -- movement duration in seconds; 0 uses the nao default duration.

Execution:
    go() -- execute all queued moves and return the nao object.

Usage Examples
--------------
    # Open both hands
    nao.hands.open().go()

    # Close right hand only
    nao.hands.right_close().go()

    # Chain from arms: arms out with hands open
    nao.arms.out().hands.open().go()

Notes
-----
- This is Python 2.7 code.
- Hand values are passed through math.degrees() -- 1.0 for open and 0.0 for
  close -- which converts radians to degrees as required by the motion API.
- All methods return self (the Hands instance) for chaining, except go()
  which returns the nao object.
'''

import math

class Hands():

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
    # Hands Open
    ###################################
    def open(self, duration=0):   
        self.right_open(duration)  
        self.left_open(duration)
        return self;

    def left_open(self, duration=0):
        duration = self.nao.determine_duration(duration)       
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LHand, math.degrees(1.0), duration)
        return self;
        
    def right_open(self, duration=0):
        duration = self.nao.determine_duration(duration)  
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RHand, math.degrees(1.0), duration)
        return self;

    ###################################
    # Hands Close
    ###################################
    def close(self, duration=0):    
        self.right_close(duration) 
        self.left_close(duration)
        return self;

    def left_close(self, duration=0):
        duration = self.nao.determine_duration(duration)       
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LHand, math.degrees(0.0), duration)
        return self;
        
    def right_close(self, duration=0):
        duration = self.nao.determine_duration(duration)  
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RHand, math.degrees(0.0), duration)
        return self;
