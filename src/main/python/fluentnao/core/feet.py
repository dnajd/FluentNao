'''
FluentNao Feet Module -- controls ankle joints and plane constraints on the NAO robot.

This module provides the Feet class, which queues ankle pitch and roll
movements and manages whole body balance plane constraints using a
fluent chaining API.

Key Methods
-----------
Ankle Pitch:
    point_toes(duration=0, offset=0)  -- point toes down (AnklePitch, 52.8 deg)
    raise_toes(duration=0, offset=0)  -- raise toes up (AnklePitch, -68.0 deg)

Ankle Roll:
    turn_out(duration=0, offset=0)    -- tilt feet outward (AnkleRoll, +/-22 deg)
    turn_in(duration=0, offset=0)     -- tilt feet inward (AnkleRoll, +/-22.8 deg)

Center:
    center(duration=0, offset=0, offset2=0) -- center both ankles (roll and pitch to 0)

Each ankle method has left_ and right_ variants, e.g. left_point_toes(),
right_turn_out().

Parameters:
    duration -- movement duration in seconds; 0 uses the nao default.
    offset   -- degrees added to the primary angle (roll or pitch).
    offset2  -- degrees added to the secondary angle (used by center()).

Plane Constraints (used by Legs for whole body balance):
    left_plane_on()  -- stiffen body, enable whole body balance, set right
                        foot Fixed and left foot Plane (left foot can move).
    right_plane_on() -- stiffen body, enable whole body balance, set left
                        foot Fixed and right foot Plane (right foot can move).
    plane_off()      -- execute queued moves via go(), free both feet, and
                        disable whole body balance.

Execution:
    go() -- execute all queued moves and return the nao object.

Usage Examples
--------------
    # Point toes on both feet
    nao.feet.point_toes().go()

    # Turn right foot outward
    nao.feet.right_turn_out().go()

    # Center both feet
    nao.feet.center().go()

Notes
-----
- This is Python 2.7 code.
- The plane constraint methods (left_plane_on, right_plane_on, plane_off)
  do NOT return self -- they are typically called internally by Legs methods
  and are not meant for fluent chaining.
- plane_off() calls go() internally to execute queued moves before releasing
  the balance constraints.
- All ankle movement methods return self (the Feet instance) for chaining,
  except go() which returns the nao object.
'''

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
        return self.nao

    ###################################
    # plane
    ###################################
    def left_plane_on(self):

        # stiffen body & enable wb
        self.nao.stiff()
        self.nao.whole_body_enable()

        # constrain feet
        self.nao.foot_state(self.joints.SupportLeg.RLeg, self.joints.StateName.Fixed)
        self.nao.foot_state(self.joints.SupportLeg.LLeg, self.joints.StateName.Plane)

    def right_plane_on(self):

        # stiffen body & enable wb
        self.nao.stiff()
        self.nao.whole_body_enable()

        # constrain feet
        self.nao.foot_state(self.joints.SupportLeg.RLeg, self.joints.StateName.Plane)
        self.nao.foot_state(self.joints.SupportLeg.LLeg, self.joints.StateName.Fixed)

    def plane_off(self):

        # block call
        self.go()

        # free feet & disable wb
        self.nao.foot_state(self.joints.SupportLeg.Legs, self.joints.StateName.Free)
        self.nao.whole_body_disable()

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
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnklePitch, angle, duration)
        return self;
        
    def left_raise_toes(self, duration=0, offset=0):
        duration = self.nao.determine_duration(duration)  
        angle = -68.0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnklePitch, angle, duration)
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
    def center(self, duration=0, offset=0, offset2=0):   
        self.right_center(duration, offset, offset2)
        self.left_center(duration, offset, offset2)
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